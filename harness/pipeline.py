#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ["evidence", "model", "structure", "visual"]
STAGE_META = {
    "evidence": {"prompt": ROOT / "prompts" / "pass-a-evidence.md", "schema": ROOT / "contracts" / "evidence.schema.json", "output": "evidence.json", "needs": ["input"]},
    "model": {"prompt": ROOT / "prompts" / "pass-b-model.md", "schema": ROOT / "contracts" / "model.schema.json", "output": "model.json", "needs": ["input", "evidence"]},
    "structure": {"prompt": ROOT / "prompts" / "pass-c-structure.md", "schema": ROOT / "contracts" / "structure.schema.json", "output": "structure.json", "needs": ["evidence", "model"]},
    "visual": {"prompt": ROOT / "prompts" / "pass-d-visual.md", "schema": ROOT / "contracts" / "visual.schema.json", "output": "visual.json", "needs": ["model", "structure"]},
}
MAX_REPAIRS = 2

def read_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def now(): return datetime.now(timezone.utc).isoformat()
def state_path(run: Path) -> Path: return run / "state.json"
def load_state(run: Path): return read_json(state_path(run))
def save_state(run: Path, state):
    state["updated_at"] = now(); write_json(state_path(run), state)
def accepted_path(run: Path, name: str) -> Path: return run / "accepted" / f"{name}.json"
def candidate_path(run: Path, stage: str) -> Path: return run / "candidate" / STAGE_META[stage]["output"]
def workspace_path(run: Path, stage: str, attempt: int) -> Path: return run / "workspaces" / f"{stage}-attempt-{attempt}"
def current_stage(state):
    idx = state.get("stage_index", 0)
    return None if idx >= len(STAGES) else STAGES[idx]

def cmd_init(args):
    run = Path(args.run).resolve(); input_file = Path(args.input).resolve()
    check = subprocess.run([sys.executable, str(ROOT / "harness" / "validate.py"), "--stage", "input", "--file", str(input_file), "--schema", str(ROOT / "contracts" / "input.schema.json")], capture_output=True, text=True)
    if check.returncode != 0: raise SystemExit("Invalid input contract:\n" + check.stdout + check.stderr)
    if run.exists() and any(run.iterdir()): raise SystemExit(f"Run directory is not empty: {run}")
    for d in ["accepted","candidate","validation","packets","rejected","workspaces"]: (run / d).mkdir(parents=True, exist_ok=True)
    shutil.copy2(input_file, accepted_path(run, "input"))
    state={"version":"kc.skill-run.v1","status":"running","stage_index":0,"repair_attempts":{s:0 for s in STAGES},"created_at":now(),"updated_at":now(),"history":[{"event":"init","at":now(),"input":str(input_file)}]}
    save_state(run,state); print(json.dumps({"run":str(run),"stage":current_stage(state),"status":"running"},ensure_ascii=False,indent=2))

def build_packet(run: Path, state):
    stage=current_stage(state)
    if not stage: return {"status":"complete"}
    meta=STAGE_META[stage]; repair_count=state["repair_attempts"].get(stage,0)
    validation_file=run/"validation"/f"{stage}.json"; last_errors=read_json(validation_file).get("errors",[]) if validation_file.exists() else []
    files={"skill":str(ROOT/"SKILL.md"),"orchestration":str(ROOT/"skill"/"ORCHESTRATION.md"),"prompt":str(meta["prompt"]),"schema":str(meta["schema"]),"output":str(candidate_path(run,stage))}
    for need in meta["needs"]: files[need]=str(accepted_path(run,need))
    if repair_count:
        previous=run/"rejected"/f"{stage}-attempt-{repair_count}.json"
        if previous.exists(): files["previous_candidate"]=str(previous)
    return {"version":"kc.codex-packet.v1","stage":stage,"mode":"repair" if repair_count else "generate","repair_attempt":repair_count,"max_repairs":MAX_REPAIRS,"instruction":"Read SKILL.md, the stage prompt, schema, and only the accepted upstream artifacts listed below. Perform the semantic work yourself. Write ONLY valid JSON to the output path. Do not read tests/baselines or manufacture semantic content from validator rules.","files":files,"validation_errors":last_errors if repair_count else [],"forbidden_runtime_inputs":[str(ROOT/"tests"),str(ROOT/"examples"),str(ROOT/"fixtures"),"any test expectation, baseline, prior example output, other-subject fixture, gold answer, or prior expected intermediate answer"]}

def materialize_workspace(run: Path, state, packet):
    stage=packet["stage"]; attempt=packet["repair_attempt"]; ws=workspace_path(run,stage,attempt)
    if ws.exists(): shutil.rmtree(ws)
    ws.mkdir(parents=True,exist_ok=True)
    copy_map={"skill":(ROOT/"SKILL.md","SKILL.md"),"orchestration":(ROOT/"skill"/"ORCHESTRATION.md","ORCHESTRATION.md"),"prompt":(STAGE_META[stage]["prompt"],"PROMPT.md"),"schema":(STAGE_META[stage]["schema"],"schema.json")}
    for need in STAGE_META[stage]["needs"]: copy_map[need]=(accepted_path(run,need),f"{need}.json")
    if attempt:
        prev=run/"rejected"/f"{stage}-attempt-{attempt}.json"
        if prev.exists(): copy_map["previous_candidate"]=(prev,"previous_candidate.json")
    safe_files={}
    for key,(src,name) in copy_map.items():
        dst=ws/name; shutil.copy2(src,dst); safe_files[key]=str(dst)
    if packet.get("validation_errors"):
        err_path=ws/"validation_errors.json"; write_json(err_path,{"errors":packet["validation_errors"]}); safe_files["validation_errors"]=str(err_path)
    output=ws/"output.json"; safe_files["output"]=str(output)
    (ws/"TASK.md").write_text(f"# Knowledge Constellation semantic pass\n\nStage: {stage}\nMode: {packet['mode']}\nRepair attempt: {attempt}/{MAX_REPAIRS}\n\nRead only the files in this workspace. Start with `SKILL.md` and `PROMPT.md`.\nWrite only valid JSON matching `schema.json` to `output.json`.\nDo not search parent directories for examples, fixtures, tests, baselines, or prior answers.\n",encoding="utf-8")
    safe_files["task"]=str(ws/"TASK.md")
    packet=dict(packet); packet["workspace"]=str(ws); packet["files"]=safe_files; packet["instruction"]="Work only inside the isolated workspace. Read SKILL.md, PROMPT.md, schema.json, and the copied accepted upstream artifacts. Perform the semantic work yourself and write ONLY JSON to output.json. Do not inspect parent/project directories."
    return packet

def cmd_next(args):
    run=Path(args.run).resolve(); state=load_state(run)
    if state["status"] in {"failed","complete"}: print(json.dumps({"status":state["status"],"run":str(run)},ensure_ascii=False,indent=2)); return
    packet=materialize_workspace(run,state,build_packet(run,state)); stage=packet["stage"]; packet_path=run/"packets"/f"{stage}-attempt-{packet['repair_attempt']}.json"; write_json(packet_path,packet); packet["packet_path"]=str(packet_path); print(json.dumps(packet,ensure_ascii=False,indent=2))

def validator_command(run: Path, stage: str):
    meta=STAGE_META[stage]; cmd=[sys.executable,str(ROOT/"harness"/"validate.py"),"--stage",stage,"--file",str(candidate_path(run,stage)),"--schema",str(meta["schema"])]
    mapping={"input":"--input","evidence":"--evidence","model":"--model","structure":"--structure"}
    for need in meta["needs"]:
        if need in mapping: cmd += [mapping[need],str(accepted_path(run,need))]
    return cmd

def cmd_validate(args):
    run=Path(args.run).resolve(); state=load_state(run); stage=current_stage(state)
    if not stage: raise SystemExit("Run is already complete")
    candidate=candidate_path(run,stage); attempt=state["repair_attempts"].get(stage,0); isolated_output=workspace_path(run,stage,attempt)/"output.json"
    if isolated_output.exists(): shutil.copy2(isolated_output,candidate)
    if not candidate.exists(): raise SystemExit(f"Candidate output not found. Expected isolated output at {isolated_output} or compatibility candidate at {candidate}")
    proc=subprocess.run(validator_command(run,stage),capture_output=True,text=True)
    try: result=json.loads(proc.stdout)
    except Exception: result={"pass":False,"errors":["validator returned non-JSON output",proc.stdout,proc.stderr]}
    write_json(run/"validation"/f"{stage}.json",result)
    if result.get("pass"):
        shutil.copy2(candidate,accepted_path(run,stage)); state["history"].append({"event":"accepted","stage":stage,"at":now()}); state["stage_index"] += 1
        if state["stage_index"] >= len(STAGES): state["status"]="complete"; state["history"].append({"event":"complete","at":now()})
        save_state(run,state); print(json.dumps({"pass":True,"accepted":stage,"next":current_stage(state),"status":state["status"]},ensure_ascii=False,indent=2)); return
    attempts=state["repair_attempts"].get(stage,0)+1; state["repair_attempts"][stage]=attempts; rejected_path=run/"rejected"/f"{stage}-attempt-{attempts}.json"; shutil.copy2(candidate,rejected_path)
    state["history"].append({"event":"rejected","stage":stage,"attempt":attempts,"at":now(),"candidate":str(rejected_path),"errors":result.get("errors",[])})
    if attempts > MAX_REPAIRS: state["status"]="failed"; state["failure"]={"stage":stage,"reason":"repair_budget_exhausted","errors":result.get("errors",[])}
    save_state(run,state); print(json.dumps({"pass":False,"stage":stage,"repair_attempt":attempts,"status":state["status"],"errors":result.get("errors",[])},ensure_ascii=False,indent=2)); sys.exit(2 if state["status"]=="failed" else 1)

def cmd_status(args):
    run=Path(args.run).resolve(); state=load_state(run); print(json.dumps({"run":str(run),"status":state["status"],"current_stage":current_stage(state),"repair_attempts":state["repair_attempts"],"accepted":[p.stem for p in sorted((run/"accepted").glob("*.json"))],"candidate":[p.name for p in sorted((run/"candidate").glob("*.json"))]},ensure_ascii=False,indent=2))

def cmd_reset_candidate(args):
    run=Path(args.run).resolve(); stage=current_stage(load_state(run));
    if not stage: raise SystemExit("Run is complete")
    p=candidate_path(run,stage); p.unlink(missing_ok=True); print(json.dumps({"cleared":str(p),"stage":stage},ensure_ascii=False,indent=2))

def cmd_render(args):
    run=Path(args.run).resolve(); state=load_state(run)
    if state.get("status") != "complete": raise SystemExit("Semantic pipeline must be complete before renderer handoff")
    out=Path(args.out).resolve() if args.out else (run/"renderer")
    cmd=[sys.executable,str(ROOT/"harness"/"build_renderer_input.py"),"--input",str(accepted_path(run,"input")),"--evidence",str(accepted_path(run,"evidence")),"--model",str(accepted_path(run,"model")),"--structure",str(accepted_path(run,"structure")),"--visual",str(accepted_path(run,"visual")),"--out",str(out)]
    proc=subprocess.run(cmd,capture_output=True,text=True)
    if proc.returncode != 0: raise SystemExit(proc.stderr or proc.stdout)
    state["history"].append({"event":"renderer_handoff","at":now(),"out":str(out)}); save_state(run,state); print(proc.stdout.strip())

def main():
    ap=argparse.ArgumentParser(description="Knowledge Constellation Codex-in-the-loop pipeline"); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("init"); p.add_argument("--input",required=True); p.add_argument("--run",required=True); p.set_defaults(func=cmd_init)
    p=sub.add_parser("next"); p.add_argument("--run",required=True); p.set_defaults(func=cmd_next)
    p=sub.add_parser("validate"); p.add_argument("--run",required=True); p.set_defaults(func=cmd_validate)
    p=sub.add_parser("status"); p.add_argument("--run",required=True); p.set_defaults(func=cmd_status)
    p=sub.add_parser("render"); p.add_argument("--run",required=True); p.add_argument("--out"); p.set_defaults(func=cmd_render)
    p=sub.add_parser("reset-candidate"); p.add_argument("--run",required=True); p.set_defaults(func=cmd_reset_candidate)
    args=ap.parse_args(); args.func(args)

if __name__ == "__main__": main()
