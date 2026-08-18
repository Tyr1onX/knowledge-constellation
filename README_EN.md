# Knowledge Constellation

[中文版](README.md)

> Turn the traces of what you have actually done into a personal knowledge universe that can be explored, explained, and refined over time.

Knowledge Constellation is a personal knowledge visualization project. It reads real material such as project READMEs, resumes, learning notes, pull requests, reviews, and other records, then organizes the evidence into an explorable constellation instead of flattening everything into a list of skills.

The goal is not to answer only “What technologies appear in these files?” It is to show **what you have really worked with, where that knowledge came from, how different areas relate to each other, and which parts are still emerging.**

## What it looks like

A generated constellation is built around several product-level elements:

- **Knowledge Stars** — individual knowledge areas represented as stars rather than badges or score bars.
- **Galaxies** — related knowledge areas grouped into larger themes.
- **Identity Core** — the center of the personal universe, giving the constellation a clear owner without turning it into a profile card.
- **Project Anchors** — real projects, courses, collaborations, or long-term experiences that explain where knowledge came from.
- **Semantic Zoom** — zooming reveals more detail naturally instead of showing every node at once.
- **Evidence disclosure** — the default view stays clean, while deeper evidence can be inspected when needed.

The visual system uses force-based spatial relationships, dynamic star rendering, ambient space, gradual detail reveal, and a personal core so the result feels like a living map rather than a static technology graph.

## What you can use it for

Knowledge Constellation is useful when you want to:

- turn scattered project and learning records into one visual knowledge map;
- understand which knowledge areas are repeatedly supported by real work;
- see how projects, tools, languages, frameworks, and concepts connect;
- present your technical growth without reducing everything to arbitrary skill percentages;
- keep a personal knowledge map that can grow as new evidence is added.

## How to use it

The current version is a runnable generation pipeline plus a reusable renderer baseline. It is not yet a one-click hosted app.

### 1. Prepare your source material

Create an input file based on [`examples/input.example.json`](examples/input.example.json).

```json
{
  "subject": {
    "id": "your-id",
    "label": "Your Name",
    "language": "en",
    "scope": "software-development"
  },
  "sources": [
    {
      "id": "S1",
      "kind": "project",
      "title": "Project README",
      "content": "Paste real project, resume, learning, PR, or other evidence here."
    }
  ]
}
```

Good sources include:

- project READMEs and documentation;
- resumes or self-introductions;
- learning notes;
- pull requests and code review records;
- issue discussions;
- course or project summaries;
- debugging and implementation notes.

More material is not automatically better. Independent, concrete records are more useful than repeated claims about the same thing.

### 2. Install the minimal dependencies

Python 3.10+ is required.

```bash
pip install -r requirements.txt
```

### 3. Create a run

```bash
cp examples/input.example.json input.json
python harness/pipeline.py init --input input.json --run runs/my-constellation
```

Replace the example content in `input.json` with your own material before continuing.

### 4. Let Codex process the constellation step by step

```bash
python harness/pipeline.py next --run runs/my-constellation
```

The command creates an isolated workspace for the current step. Codex reads the task and writes the requested `output.json`.

Then validate the result:

```bash
python harness/pipeline.py validate --run runs/my-constellation
```

Repeat `next` and `validate` until the pipeline completes.

The process gradually turns raw sources into:

```text
Evidence
  ↓
Knowledge model
  ↓
Relations, galaxies and anchors
  ↓
Personal visual model
```

### 5. Render the result

The accepted visual model is consumed by the modules in [`renderer/`](renderer/). The renderer already contains the current visual and interaction baseline for stars, physics, semantic zoom, identity core, project anchors, detail presentation, and ambient background.

The full end-to-end product runtime is still being assembled, so the repository currently focuses on the generation pipeline and reusable rendering system rather than shipping a hosted web app.

## What makes the result different

Knowledge Constellation deliberately avoids several common shortcuts:

- a dependency does not automatically become personal knowledge;
- appearing in a project does not automatically mean mastery;
- participating in a task is not treated as independently implementing every part of it;
- one self-description is not treated as multiple independent confirmations;
- more stars do not mean a “stronger” person;
- uncertainty is allowed to remain uncertainty.

This is why the constellation is built from evidence first, then turned into structure and visuals.

## Example data

A minimal input is available at [`examples/input.example.json`](examples/input.example.json).

The repository also keeps an early real-world sample under [`examples/tyr1onx/`](examples/tyr1onx/) so you can inspect how raw material becomes evidence, knowledge nodes, relations, and structure.

## Current status

The core recognition pipeline and the main visual language are already in place. Current work focuses on making recognition more reliable across unfamiliar users and assembling the existing renderer modules into a more complete end-user runtime.

For implementation details, model contracts, evaluation notes, and research history, see [`docs/`](docs/) and [`SKILL.md`](SKILL.md).
