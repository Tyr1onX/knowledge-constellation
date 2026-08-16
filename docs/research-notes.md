# Research Notes

This file records ideas worth borrowing, the problem they solve, and how Knowledge Constellation should reinterpret them rather than copy them mechanically.

## Research rule

For every external idea, ask:

```text
What problem are they solving?
↓
Do we actually have the same problem?
↓
Why does their solution work?
↓
Which principle is transferable?
↓
What should our own solution look like?
```

Do not collect features for their own sake.

---

## Personal Skill Graph

Useful idea:

- skills should form a graph rather than a flat list;
- evidence can be attached to skills;
- the graph can evolve over time.

What we should not inherit blindly:

- career-first framing;
- simple proficiency levels as the main representation;
- the assumption that a skill node must already be a proven capability.

Our reinterpretation:

A Knowledge Node can represent meaningful exposure, active learning, established practice, or an unresolved area. The person is the subject, not an occupational taxonomy.

---

## lucidRESUME

Useful ideas:

- evidence provenance;
- recency and repeated evidence;
- skill claims should be traceable back to actual artifacts;
- avoid inventing skills that are absent from evidence.

Our extension:

Modern AI-assisted work makes attribution a first-class problem. A technically sophisticated artifact may not measure the user's independent implementation depth. We therefore separate artifact existence, user participation, external validation, and capability claims.

---

## GoMeasure / evidence-based assessment systems

Useful ideas:

- inference and verification are different stages;
- confidence and freshness matter;
- assessment can progressively become stronger as new evidence arrives.

Our reinterpretation:

Verification is optional rather than a prerequisite for the first result. The default product should produce a conservative constellation from passive evidence, then offer low-friction calibration only when the user wants greater resolution.

---

## Adaptive knowledge assessment

Useful idea:

When only a few questions can be asked, choose questions with high information value rather than administering a fixed questionnaire.

Potential future use:

- identify the most consequential uncertain nodes;
- ask at most a small number of questions;
- update multiple related claims from each answer;
- stop when additional questions are unlikely to materially change the constellation.

Not part of V0.

---

## Mind-map / artifact-generation skills

Useful idea:

A Skill can generate a self-contained interactive artifact rather than requiring a full SaaS application.

Potential future use:

Knowledge Constellation may eventually render as HTML/SVG/React or another portable artifact with zoom, hover, evidence inspection, and optional calibration.

The rendering format remains deliberately undecided in V0.

---

## ESCO / O*NET and taxonomies

Useful idea:

Established taxonomies can help normalize synonyms and prevent duplicate nodes.

Potential future use:

Use taxonomies as background reference, not as the visible shape of the person's constellation.

The product must not become a checklist of how much of a standardized syllabus the user has completed.

---

# Current original hypotheses

These are the ideas this project currently treats as its own product direction and still needs to validate experimentally.

## 1. Passive-first, calibration-later

A useful result should appear before the user is asked to explain themselves deeply.

## 2. Attribution is central in the AI coding era

The system must distinguish:

```text
Artifact exists
≠
User independently produced it
≠
User understands every concept involved
```

## 3. Uncertainty belongs in the product

Unknown information should be represented rather than silently completed.

The first constellation can be lower-resolution without being considered incorrect.

## 4. Exposure and capability are different axes

A person may repeatedly encounter a technology while still having limited independent capability, or may understand a concept well without using it frequently in projects.

## 5. The constellation represents the person, not a curriculum

The system should surface what is structurally important in the person's actual learning and practice history, not everything that exists in a domain.

## 6. Assessment can be detailed while visualization remains restrained

Fine-grained evidence can support coarse, meaningful visible nodes. Detailed facts such as a single API or syntax rule may remain evidence underneath a larger node instead of becoming a star in the global view.

---

# Open research questions

1. Which passive GitHub signals are useful for estimating participation without over-attributing capability?
2. When should repeated exposure be promoted from `observed` to `developing`?
3. What minimum evidence is required for `established`?
4. How should contradictory evidence be handled?
5. How should assisted work contribute to nodes such as requirement framing, review, validation, and debugging?
6. How should the visual layer distinguish high exposure / low capability from low exposure / high understanding?
7. What is the minimum visible node granularity at each zoom level?
8. How can micro-calibration use multiple-choice answers without encouraging self-inflation?
