# Draft: upstream issue (post FIRST, before any PR)

**Title:** Proposal: Meta Muse port — request for a "Community Ports" link

**Body:**

Hi Jordan — I've ported the 16-step pipeline to Meta Muse (Meta's personal agent; skills run server-side in its workspace, so runs work from mobile clients). Because Muse skills can't ship a pip CLI, SQLite vault, or Stop hook, the port is a self-contained skill folder: SKILL.md orchestrator, step references, and a small bookkeeping script using a JSON manifest + shared markdown notes pool. Enforcement is manifest discipline, documented as such — I followed your Codex section's lead on stating plainly what differs.

I maintain it in my own repo so it adds zero maintenance or CI burden here: https://github.com/vanceingalls/hyperresearch-muse

Would you be open to a small docs PR adding a "Community Ports" note (README or docs) linking to it? Happy to match whatever wording you prefer, and to keep the port synced with upstream pipeline changes.

Either way, thanks for building this — the method ported cleanly, which says a lot about the design.
