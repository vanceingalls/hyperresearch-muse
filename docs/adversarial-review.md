# Adversarial review — summary

Before publication, the skill package was reviewed adversarially by Gemini 3.1 Pro (an independent model family), prompted to assume the author was overconfident and to attack six named areas. Verdict was "do not publish as-is." Findings and dispositions:

| # | Finding | Severity (reviewer) | Disposition |
|---|---------|--------------------|-------------|
| 1 | No prompt-injection guardrails for fetched web content | Critical | **Fixed** — SKILL.md guardrails: fetched content is untrusted data, never instructions; subagents receive only their step's context |
| 2 | Context leakage to subagents | Major | **Fixed** — same guardrail paragraph |
| 3 | Path traversal via unsanitized `--tag` | Critical | **Fixed** — strict tag regex, exit code 2; covered by tests |
| 4 | MIT license text missing from the package | Major | **Fixed** — upstream LICENSE (Copyright (c) 2026 Jordan Gibbs) ships in the package; report-credit instruction removed |
| 5 | "Finish refuses to pass" overstates enforcement | Major | **Fixed** — wording now states the script tracks self-reported progress and cannot verify quality |
| 6 | Race condition in manifest writes under parallel step recording | Critical | **Mitigated** — lockfile around load/save + atomic replace; parallel-recording test passes. Note: by design only the orchestrator records steps |
| 7 | Unvalidated step names accepted | Minor | **Fixed** — steps must be in the run's plan; covered by tests |
| 8 | "Broken for mobile" (script needs Python) | Major | **Disputed** — Muse skills execute in Muse's server-side workspace, not on the phone; Python is present there. A clarifying line was added to SKILL.md |

Tests: `tests/test_research_run.py` — 7 tests covering slugify, tag validation, step validation, the finish gate, and lossless parallel step recording.
