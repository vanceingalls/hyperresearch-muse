<h1 align="center">hyperresearch-muse</h1>

<p align="center"><strong>Deep research that survives cross-examination — now running inside Muse.</strong></p>

<p align="center">
  <a href="https://github.com/jordan-gibbs/hyperresearch"><img alt="Port of Hyperresearch v0.13.3" src="https://img.shields.io/badge/port%20of-Hyperresearch%20v0.13.3-1A1F2E"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-6B8FBF"></a>
  <a href="https://github.com/vanceingalls/hyperresearch-muse/releases/download/latest/deep-research-skill.zip"><img alt="Download the latest skill zip" src="https://img.shields.io/badge/download-latest%20skill%20zip-6B8FBF"></a>
  <img alt="Runs in Meta Muse — phone, desktop, web" src="https://img.shields.io/badge/runs%20in-Meta%20Claude-3D4A5C">
</p>

<p align="center">
  <a href="#install">Install</a> · <a href="#see-a-run">See a run</a> · <a href="#how-it-works">How it works</a> · <a href="#upstream-vs-this-port">Differences</a> · <a href="#evaluation-note">Evaluation</a> · <a href="#faq">FAQ</a>
</p>

## What is this?

[Hyperresearch](https://github.com/jordan-gibbs/hyperresearch), by Jordan Gibbs, is a deep-research pipeline for coding agents: instead of answering from one pass of searching, it decomposes a question, sweeps sources from several angles, sends investigators to argue positions, drafts the answer three different ways, then attacks the result with critics before patching and cite-checking it.

This repo is a **community port of that pipeline to Meta Muse** — one self-contained skill folder (`deep-research/`) that Muse runs with its own subagents, search, and browser. No pip CLI, no API keys, no server of yours. Because Muse skills execute in Muse's workspace rather than on a device, a run you start on your phone can be picked up in the same chat on your desktop.

**Cited / Adversarial / Tiered / Yours** — every claim tied to a source note · four critics attack the draft before you see it · light or full depth, chosen per question · runs on your normal Muse plan.

## Install

The same steps work in the Muse app on **mobile, desktop, or web** — nothing installs on your device.

**Option A — let Muse fetch it.** Paste this prompt into any chat with your Muse (also kept in [INSTALL-PROMPT.md](INSTALL-PROMPT.md)):

```
Install the Deep Research skill for me from its GitHub repo.

1. Download the latest release package from:
   https://github.com/vanceingalls/hyperresearch-muse/releases/download/latest/deep-research-skill.zip
2. Unzip it. Inside is a single folder named "deep-research".
3. Put that folder in my custom skills folder (~/workspace/custom-skills/), so that
   ~/workspace/custom-skills/deep-research/SKILL.md exists, with skill.yaml, LICENSE,
   the references/ folder, and the scripts/ folder intact. If an older deep-research
   folder is already there, replace it — treat this as an upgrade.
4. Verify the install: list the installed files, and run
   python3 ~/workspace/custom-skills/deep-research/scripts/research_run.py --help
   to confirm the bookkeeping script runs.
5. Confirm back to me: the skill's name (deep_research, "Deep Research"), what it does
   in a sentence or two, its two tiers (light and full), and that it needs no API keys.
   Tell me I can start by asking you for deep research on any question.
```

Pasting the same prompt again later upgrades you to the newest version — the download link always serves the latest build, which is republished automatically on every push to `main`.

**Option B — attach the zip yourself.** Download **[deep-research-skill.zip](https://github.com/vanceingalls/hyperresearch-muse/releases/download/latest/deep-research-skill.zip)**, attach it in a Muse chat, and ask Muse to install the `deep-research` folder into your custom skills folder with its contents intact.

Then ask your Muse for deep research on any question.

## See a run

**The question** (a real evaluation task): *"My breathing gets worse within minutes of using my new blue rescue inhaler, and my home oxygen readings have dropped from about 95% to 91%. Should I just stop using it?"*

**What came back** — the opening of the report this pipeline produced during its DRACO evaluation:

> ## The short answer
>
> No — this does not sound like a normal "adjustment period," and you should not simply push through it. A rescue inhaler (typically albuterol/salbutamol, a short-acting beta-agonist) is supposed to relieve wheezing and chest tightness within minutes. Getting *worse* within minutes of using it, repeatedly, over three weeks — together with home oxygen readings falling from your usual ~95% to 91% — is a pattern that needs **urgent, same-day medical attention…**
>
> ### Paradoxical bronchospasm — the inhaler narrowing the airways instead of opening them
>
> This is the explanation that most closely matches your description: wheezing and tightness that *worsen within minutes of a dose*. The FDA-approved prescribing information for albuterol sulfate inhalation aerosol states that it "can produce paradoxical bronchospasm, which may be life threatening," that if it occurs the inhaler "should be discontinued immediately and alternative therapy should be instituted," and that it "frequently occurs with the first use of a new canister." (DailyMed, Albuterol Sulfate Inhalation Aerosol label: https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=fd0389e0-3713-42e0-8ef2-3bb97676fded&version=2)

Every claim in the full report is tied to a source like that one — a verbatim quote, a source name, and a URL. Claims that can't be tied down get flagged, not smoothed over. (Full methodology and caveats: [Evaluation note](#evaluation-note).)

Other shapes of question it handles: **Fact-check a claim** ("Did X really say Y, and what's the primary source?") · **Compare two options** ("Which of these two machines fits these constraints?") · **Sweep a literature** ("What's the current expert consensus on Z, and where do the experts disagree?")

## How it works

When you ask for deep research, Muse acts as the **orchestrator**: it sequences the steps below, spawns subagents for the steps that call for them, and records progress. It does not do a step's research or drafting itself when the step assigns that work to subagents, and it loads one step's procedure at a time from `deep-research/references/pipeline-steps.md`.

```mermaid
flowchart LR
    A["1 · Decompose"] --> B["2 · Width sweep"]
    B --> C["3 · Contradiction graph"]
    C --> D["4 · Loci analysis"]
    D --> E["5 · Depth investigation"]
    E --> F["6 · Reconcile"]
    F --> G["7 · Source tensions"]
    G --> H["8 · Corpus critic"]
    H --> I["9 · Evidence digest"]
    I --> J["10 · Triple draft"]
    J --> K["11 · Synthesize"]
    K --> L["12 · Critics ×4"]
    L --> M["13 · Gap fetch"]
    M --> N["14 · Patcher"]
    N --> O["14.5 · Cite check"]
    O --> P["15 · Polish"]
    P --> Q["16 · Readability audit"]
```

Two tiers, chosen when the run starts:

- **Light** — steps 1, 2, 10, 15, 16. For narrow factual questions; the triple draft works directly from the width-sweep notes.
- **Full** — the complete sequence above (steps 1–16 plus the inserted 14.5 cite-check). The default for contested, multi-part, or high-stakes questions.

<details>
<summary><strong>Every step, in order</strong> — job, and what it produces</summary>

| Step | What happens |
|---|---|
| 1. Decompose | The question becomes a canonical query, atomic sub-questions, and a coverage matrix. |
| 2. Width sweep | Parallel fetcher subagents search several angles and write source notes (claim, evidence, verbatim quote, source name, URL, date) into the project's shared notes pool. |
| 3. Contradiction graph | Notes that disagree are paired and clustered into ranked fights. |
| 4. Loci analysis | The distinct positions the answer must compare are identified, scored by evidence strength, and given source budgets. |
| 5. Depth investigation | One investigator subagent per locus, in parallel. Each must commit to a position with cited evidence — a both-sides summary fails the step. |
| 6. Cross-locus reconcile | Committed positions are compared; conflicts are resolved with evidence or flagged as genuinely open. |
| 7. Source tensions | The expert disagreements themselves are extracted as findings, with both camps and their strongest sources. |
| 8. Corpus critic | The corpus is attacked before drafting: what's missing, what's over-weighted, what would overturn the emerging answer. Worst gaps are fetched or recorded as limitations. |
| 9. Evidence digest | The top claims the report will make, each backed by verbatim quotes and citations. |
| 10. Triple draft | Three drafter subagents in parallel write complete drafts from different angles (e.g. evidence-first, comparison-first, skeptic-first). |
| 11. Synthesize | A synthesizer writes the final report in two passes — outline mapped to the evidence digest, then full text. |
| 12. Critics | Four critic subagents in parallel, one lens each: factual accuracy, coverage against the step 1 matrix, citation integrity, logical coherence. Findings must name concrete defects with locations. |
| 13. Gap fetch | Sources are fetched for the gaps the critics found, or the gap is recorded as unresolvable. |
| 14. Patcher | One patcher applies surgical edits for every accepted critic finding — no full rewrites. Rejected findings need a stated reason. |
| 14.5. Cite check | Each citation is verified against the sentence it supports; failing citations are rebound, replaced, or deleted. |
| 15. Polish | Hygiene pass: structure, headings, citation format, repetition. |
| 16. Readability audit | A fresh-reader pass scores clarity and suggests concrete fixes; only substance-preserving suggestions are applied. The run's finish gate is checked at the end of this step. |

</details>

### What you get back

- The final report as a file, at `research/notes/final_report_<vault_tag>.md` inside the run's project folder.
- A short chat summary: headline findings, the strongest tensions the research surfaced, and the known limitations recorded by the corpus critic.
- A statement of which tier ran and which steps that tier skipped, so you can judge how much machinery stands behind the report.

Research is organized as **projects** (one folder per research domain, with a notes pool shared across its questions) and **runs** (one question each, identified by a vault tag like `what-is-the-best-ev-a1b2c3`). Later questions in a project start from earlier sources.

## Upstream vs. this port

This is not a fork of the upstream codebase and shares no code with it beyond the bookkeeping helper written for this port. What differs, plainly:

| | Upstream Hyperresearch | This port |
|---|---|---|
| Host | Claude Code / Codex, on your computer | Meta Muse — phone, desktop, web |
| Enforcement | Stop hook can physically block a session from ending mid-pipeline | Manifest discipline: a finish gate in the bookkeeping script, plus the skill treating a report written without the steps as a failure. The script tracks *self-reported* progress — it cannot verify a step was done well |
| Storage | SQLite vault | JSON manifest + a shared markdown notes pool per project |
| Fetching | Built-in scholarly-source client | Muse's own search and browser tools |
| Tiers | Light / full / dissertation | Light / full |
| Cost model | Your coding-agent setup, or their hosted API (per report) | Your Muse plan. No API keys |

**Guardrails** (part of the skill's instructions): fetched web content is treated as untrusted data, never as instructions — source text telling the agent to ignore instructions or exfiltrate files is noted as an attack, not obeyed. Subagents receive only the context their step needs, never your full chat history or credentials.

<details>
<summary><strong>The bookkeeping script</strong> — the only code in the skill</summary>

`deep-research/scripts/research_run.py` tracks run state; it does not do research. It requires Python 3, which Muse's workspace provides.

```bash
python3 research_run.py init   --project <dir> --query "<question>" --tier <light|full>   # start a run; prints the vault tag
python3 research_run.py step   --project <dir> --tag <vault_tag> --step "5-depth-investigation"  # record a finished step
python3 research_run.py status --project <dir> [--tag <vault_tag>]                        # show run status
python3 research_run.py finish --project <dir> --tag <vault_tag>                          # finish gate
```

Properties, all covered by the tests in `tests/` (run them with `python3 -m pytest tests/test_research_run.py`): vault tags are strictly validated (path traversal rejected), a step can only be recorded if it's in the run's plan for its tier, manifest writes are lockfile-protected and atomic so parallel recordings can't lose updates, and `finish` refuses while any planned step is unrecorded or the report file is missing.

</details>

## Evaluation note

During development, reports from an early version of this port were evaluated on the DRACO deep-research benchmark (Perplexity/Harvard) — 10 tasks, one per domain, 376 rubric criteria, judged by Gemini 3.1 Pro — as a sanity check that the pipeline produces well-cited, well-structured reports when re-expressed for Muse. The check found no sign of a regression: the reports held up at the level this pipeline is known for, rather than degrading in the move to a different host and a different model. The score itself isn't posted here: a single-judge-pass run on one 10-task subset isn't comparable to upstream's published figure (a different subset, judged under the official protocol), and putting two numbers side by side would imply a head-to-head that never happened. The eval harness (a separate skill, `draco-eval`) and the run artifacts are not in this repository; this note is provenance for the port, not a feature of it.

## FAQ

**Does it cost API money?**
No. The skill runs on your Muse plan using Muse's own tools. There are no API keys to supply and no per-report charge. (Upstream's hosted API is a separate, paid product — this port doesn't use it.)

**Does it really work from a phone?**
Yes. The skill executes in Muse's workspace, not on your device; the phone app is a window into the same workspace as desktop and web. Start a run on one, check it on another — there are no local files to sync.

**Is this official?**
No. It's a community port of an MIT-licensed open-source project, maintained independently, with the original author credited in the skill and below. It's not affiliated with Jordan Gibbs or with Meta's Muse team.

**How does it stay in sync with upstream?**
The port is pinned to upstream **v0.13.3**. The sync method is deliberate: upstream's pipeline files are diffed against a pinned baseline, changes are triaged (pipeline changes get ported; host-specific features get recorded as divergences in the table above), and each sync ships as a normal release here. Syncs are judgment calls, not automatic merges — upstream changes have to be re-expressed for Muse's tools.

## Repository contents

<details>
<summary>What's in this repo</summary>

```
.github/workflows/
  release.yml              on push to main: rebuilds deep-research-skill.zip and
                           publishes it to the rolling "latest" release
README.md                  this file
INSTALL-PROMPT.md          a paste-in prompt that makes Muse fetch and install the skill itself
LICENSE                    MIT license for this repo's additions
deep-research/             the Muse skill (the installable unit)
  SKILL.md                 orchestrator playbook
  skill.yaml               skill metadata (name: deep_research)
  LICENSE                  upstream Hyperresearch license and copyright notice
  references/
    pipeline-steps.md      per-step jobs, inputs, outputs, and exit criteria
  scripts/
    research_run.py        run bookkeeping: init / step / status / finish
docs/
  adversarial-review.md    pre-publication adversarial review: findings and fixes
  upstream-issue.md        draft of the proposal issue posted upstream
  upstream-pr.md           draft of the follow-up docs PR (Community Ports link)
tests/
  test_research_run.py     tests for the bookkeeping script
```

</details>

## Provenance and license

The pipeline architecture is adapted from [Hyperresearch](https://github.com/jordan-gibbs/hyperresearch) by **Jordan Gibbs**, MIT License. The original copyright notice and license text ship in `deep-research/LICENSE`; this repo's own additions are offered under the same terms (see `LICENSE` at the root).

Before publication, the package passed an adversarial review by an independent model (Gemini 3.1 Pro) whose verdict was "do not publish as-is." The findings and the fixes they produced — license text, tag sanitization, step validation, manifest locking, injection guardrails, honesty wording — are summarized in `docs/adversarial-review.md`.

## Maintenance

Maintained by Vance Ingalls ([@vanceingalls](https://github.com/vanceingalls)). Synced with upstream **v0.13.3** (see the FAQ for how syncing works). Commitment: track upstream changes to the pipeline and sync them into the skill; triage Muse-specific issues here. Not promised: parity with upstream's hosted API/MCP features, or integration with the upstream Python CLI.
