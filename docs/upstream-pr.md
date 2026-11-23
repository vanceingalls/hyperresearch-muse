# Draft: upstream docs PR (only after the issue gets a warm response)

**Title:** docs: add Meta Muse community port

**PR description:**

Adds a short "Community Ports" entry pointing to the Meta Muse port of the pipeline, maintained outside this repo:

- **hyperresearch-muse** — https://github.com/vanceingalls/hyperresearch-muse — the 16-step pipeline as a self-contained Muse skill (no CLI/vault/Stop hook; JSON manifest + markdown notes pool; enforcement is manifest discipline, documented in the port's "What differs on Muse" section).

No code changes; no new maintenance surface for this repo. The port's maintainer (me) tracks upstream pipeline changes and syncs them. Wording is yours to adjust — happy to move this wherever it fits best, or drop it entirely if you'd rather not list ports.

**README text to add (suggested placement: end of the Install section):**

### Community ports

- **Meta Muse** — [hyperresearch-muse](https://github.com/vanceingalls/hyperresearch-muse): the pipeline as a self-contained Muse skill, runnable from mobile clients. Community-maintained; differs from the official targets (no CLI, vault, or Stop hook — see its README).
