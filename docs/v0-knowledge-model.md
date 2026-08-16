# V0 Knowledge Model

The V0 model is intentionally small. Its goal is not to describe every possible form of human knowledge; it is to test whether passive evidence can produce a conservative, explainable first constellation.

## Pipeline

```text
Source
  ↓
Evidence
  ↓
Claim
  ↓
Knowledge Node
```

`Attribution`, `Confidence`, and `State` are fields rather than standalone objects in V0.

---

## 1. Source

A Source identifies where an observation came from.

```yaml
id: source_egc_pr_1271
type: github_pr
locator: https://github.com/Fmarzochi/EGC/pull/1271
observed_at: 2026-08-16
```

### Initial source types

- `github_profile`
- `github_repository`
- `github_pr`
- `github_issue`
- `github_review`
- `resume`
- `portfolio`
- `learning_record`
- `document`

Source type does not determine truth by itself. A learning record and an external review provide different kinds of evidence and should be interpreted differently.

---

## 2. Evidence

Evidence records what was actually observed before making a capability judgment.

```yaml
id: evidence_egc_1271_merged
source: source_egc_pr_1271
kind: external_validation
observation: >-
  A pull request introducing a concurrency fix and multi-process chaos harness
  was merged after maintainer review.
attribution:
  level: external
  note: The maintainer validates the accepted contribution, not the user's
        independent mastery of every underlying concept.
confidence: high
```

### Evidence kinds

V0 starts with a small vocabulary:

- `artifact` — a repository, file, feature, pull request, document, etc. exists;
- `activity` — the person repeatedly participated in an observable workflow;
- `learning_record` — a structured record says a topic was studied or explained;
- `external_validation` — a maintainer, reviewer, evaluator, or accepted outcome validates something;
- `self_report` — the person explicitly states something about their own experience;
- `behavioral` — a direct answer, explanation, task, or demonstrated behavior is observed.

### Evidence rule

Evidence should describe an event or trace, not a flattering interpretation.

Bad:

```text
The user is strong at concurrency.
```

Better:

```text
The user authored a merged PR whose accepted change involved a cursor CAS and a
multi-process concurrency harness.
```

---

## 3. Attribution

Attribution answers a narrower question:

> How much of this evidence can safely be attributed to the person?

V0 uses four levels:

### `direct`

The observed action itself is directly tied to the person, for example authoring a PR, writing a public explanation, or answering a calibration question.

`direct` does **not** mean the entire underlying artifact was independently produced without assistance.

### `assisted`

There is explicit evidence that AI tools, collaborators, templates, or other assistance were materially involved, while the person still participated in the activity.

### `uncertain`

The artifact is associated with the person, but contribution depth or authorship cannot be established from available evidence.

### `external`

The evidence is a third-party judgment or outcome, such as a maintainer accepting a pull request.

### Critical rule

If the system knows only that a repository belongs to someone, implementation-level attribution defaults to `uncertain`, not `direct`.

---

## 4. Claim

A Claim is a statement about the person that the available evidence actually supports.

```yaml
id: claim_open_source_participation
statement: Has sustained experience participating in real open-source workflows.
supported_by:
  - evidence_egc_1271_merged
  - evidence_other_merged_prs
confidence: high
limits:
  - Does not imply independent mastery of every technology touched by those PRs.
```

Every claim should be able to answer:

1. What do we believe?
2. Why do we believe it?
3. Which evidence supports it?
4. What part can be attributed to the person?
5. Where does the evidence stop?

If these questions cannot be answered, the claim should be weakened, marked unresolved, or omitted.

---

## 5. Knowledge Node

A Knowledge Node is a distilled concept that may become visible in the constellation.

A node does not necessarily mean "mastered skill". It means the concept has a meaningful place in the person's observed knowledge or practice world.

```yaml
id: rust
label: Rust
state: observed
confidence: low
signals:
  exposure: high
  capability: unresolved
claims:
  - claim_rust_exposure
```

This allows a technology to be visible without falsely claiming proficiency.

---

## Node states

V0 uses four states only.

### `established`

Multiple strong signals support a stable claim about meaningful knowledge or practice.

### `developing`

There is clear learning or practice evidence, but the knowledge or capability is still forming or only partially established.

### `observed`

The concept clearly appears in the person's experience, but depth, understanding, or independence remains unresolved.

### `unresolved`

There are hints worth retaining internally, but not enough evidence for a stable visible node.

`unresolved` nodes should normally be omitted from the main constellation or represented only as peripheral uncertainty.

---

## Confidence

V0 deliberately avoids fake precision.

Allowed values:

- `high`
- `medium`
- `low`

Do not generate values such as `0.783` unless a future evaluation method can justify them.

---

## Exposure and capability must remain separate

A recurring problem in passive evidence is that technology exposure is easy to observe while independent capability is not.

Example:

```yaml
id: typescript
label: TypeScript
state: observed
confidence: low
signals:
  exposure: high
  capability: unresolved
```

This is preferable to inventing a numeric proficiency score.

---

## Claim boundary rules

### Repository uses X

May support:

- X is present in the person's project environment;
- the person has exposure to X.

Does not automatically support:

- the person can independently implement with X;
- the person understands X deeply.

### Merged PR involving X

May support:

- real participation in an accepted contribution;
- exposure to the relevant problem domain;
- open-source workflow experience;
- external validation of the delivered change.

Does not automatically support:

- independent authorship of every line;
- mastery of every concept involved.

### Learning record says `understood`

May support:

- the topic was deliberately studied;
- there is structured evidence of claimed understanding;
- the node may be `developing` or stronger depending on corroboration.

Does not automatically support:

- durable retention;
- independent performance under fresh conditions;
- `interview-ready` or expert status.

---

## V0 stopping condition

The V0 model is sufficient when it can produce a useful first constellation while preserving uncertainty honestly.

It does **not** need to know the whole person.

A successful V0 should be able to say both:

- "This clearly belongs in your constellation."
- "This appears in your experience, but I cannot yet justify a stronger claim."
