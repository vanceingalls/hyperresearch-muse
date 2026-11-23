# Pipeline steps in detail

The pipeline architecture is adapted from Hyperresearch by Jordan Gibbs (MIT), reworked here for Muse's own subagents and tools. Each step lists its job, its inputs, what it writes, and its exit criterion. The orchestrator loads only the current step's section into focus, runs it, records it, and moves on.

## Step 1. Decompose

- Job: turn the user's question into a canonical research query, a set of atomic sub-questions, and a coverage matrix of what a complete answer must touch.
- Writes: the run scaffold and manifest (via `research_run.py init`), plus `temp/decomposition.md` with the sub-questions and coverage matrix.
- Classify the tier here. Light for a narrow factual question, full for anything contested, multi-part, or high-stakes.
- Exit: every part of the original question maps to at least one sub-question.

## Step 2. Width sweep

- Job: broad multi-perspective search before depth. Write a search plan with several distinct angles (definitions, primary data, expert consensus, dissent, recent developments, primary documents).
- Spawn fetcher subagents in parallel, one per angle. Each fetches sources with the browser tools and writes source notes into the shared notes pool: claim, evidence, verbatim quote, source name, URL, date.
- Prefer primary and authoritative sources. Note source quality in each note.
- Exit: every sub-question has at least two independent sources, or a note recording that the search came up empty.

## Step 3. Contradiction graph (full tier)

- Job: pair up notes that disagree and cluster the disagreements into ranked fights, ordered by how much the answer depends on resolving them.
- Writes: `temp/contradictions.md`.
- Exit: every material disagreement in the corpus appears in a cluster with both sides cited.

## Step 4. Loci analysis (full tier)

- Job: identify the loci, the distinct positions or approaches the answer must compare, and score each by evidence strength. Assign each locus a source budget for depth work.
- Writes: `temp/loci.json`.
- Exit: each locus has named sources behind it and a budget.

## Step 5. Depth investigation (full tier)

- Job: one investigator subagent per locus or sub-question, working in parallel. Each reads its sources deeply, follows citations, and writes an interim note that commits to a position with the evidence for it.
- Investigators must commit. A note that lists both sides without a position fails this step.
- Exit: an interim note per locus, each with a committed position and cited evidence.

## Step 6. Cross-locus reconcile (full tier)

- Job: reconcile the committed positions into a comparison: where investigators agree, where they conflict, and which conflicts the evidence settles.
- Writes: `temp/comparisons.md`.
- Exit: every pair of conflicting positions is either resolved with evidence or flagged as genuinely open.

## Step 7. Source tensions (full tier)

- Job: extract the expert disagreements themselves as findings. Who disagrees with whom, about what, and on what evidence.
- Writes: `temp/source-tensions.json`.
- Exit: the major tensions are named with both camps and their strongest sources.

## Step 8. Corpus critic (full tier)

- Job: attack the corpus before drafting. Ask what source would overturn the emerging answer, what is missing, and what is over-weighted. Fetch targeted gap-fill sources for the worst holes.
- Exit: the top gaps are either filled or written down as known limitations for the report.

## Step 9. Evidence digest (full tier)

- Job: distill the corpus into the top claims the report will make, each with its strongest verbatim quotes and citations.
- Writes: `temp/evidence-digest.md`.
- Exit: every planned claim has at least one verbatim quote behind it.

## Step 10. Triple draft (all tiers)

- Job: three drafter subagents in parallel, each writing a complete draft from a different angle (for example evidence-first, comparison-first, and skeptic-first), each curating its own source subset.
- In the light tier this step drafts directly from the width-sweep notes.
- Exit: three complete drafts on disk in `temp/drafts/`.

## Step 11. Synthesize (full tier)

- Job: a synthesizer subagent writes the final report in two passes, first an outline that maps claims to the evidence digest, then the full text, taking the strongest material from each draft.
- Writes: `research/notes/final_report_<vault_tag>.md`.
- Exit: the report answers every sub-question from step 1.

## Step 12. Critics (full tier)

- Job: four critic subagents in parallel, each with one lens: factual accuracy, coverage against the step 1 matrix, citation integrity, and logical coherence. Each writes findings as a list of concrete defects with locations.
- Exit: four findings files in `temp/critics/`.

## Step 13. Gap fetch (full tier)

- Job: fetch sources for the gaps the critics found, using fetcher subagents as in step 2.
- Exit: each critic gap is either sourced or recorded as unresolvable.

## Step 14. Patcher (full tier)

- Job: one patcher subagent applies surgical edits to the final report for every accepted critic finding. No full rewrites.
- Exit: every accepted finding is patched or explicitly rejected with a reason.

## Step 14.5. Cite check (full tier)

- Job: verify that each citation actually supports the sentence it is attached to. Rebind, replace, or delete citations that fail.
- Exit: a sampled pass over the report finds no unsupported citation bindings.

## Step 15. Polish (all tiers)

- Job: hygiene pass. Remove filler, fix structure and headings, standardize citation format, cut repetition.
- Exit: the report reads clean start to finish.

## Step 16. Readability audit (all tiers)

- Job: a fresh reader pass that scores clarity for the intended audience and writes concrete suggestions. The orchestrator applies only the suggestions that improve clarity without changing substance.
- Exit: suggestions reviewed, applied ones recorded, and `research_run.py finish` passes.
