# Pass B — Claims and Knowledge Nodes

Read `SKILL.md`, accepted `input.json`, accepted `evidence.json`, and `contracts/model.schema.json`. Produce only `model.json` matching the schema.

Create bounded, dimension-specific Claims such as exposure, understanding, implementation, independence, judgment, troubleshooting, transfer, participation, learning-state, recency, and representativeness. Do not compress them into one skill score. Stronger Claims require stronger and more independent Evidence.

Create a node only when the concept is stable enough to help describe this person. Preserve product-usable `summary`, `known`, `unknown`, `reason`, `boundary`, and `next_step`. Representativeness and capability are not the same thing. Do not complete a standard technology taxonomy or read test baselines/prior expected answers.

Treat the node label itself as part of the attribution contract. Do not bundle activities with materially different attribution into one human-sounding label merely because they occur in the same artifact. For example, if sources support human reproduction/re-verification while explicitly crediting an AI agent for reduction or drafting, prefer a node that names the supported human behavior and keep the assisted activity in bounded claims/evidence. AI-assisted/collaborative/generated/templated are usually provenance or working-mode facts, not standalone Knowledge Nodes unless the evidence supports an actual stable knowledge concept beyond the mode itself.
