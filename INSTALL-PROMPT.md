# Install prompt

Don't want to download and attach files yourself? Paste the prompt below into any chat with your Muse — on phone, desktop, or web — and Muse will fetch the latest package from this repo and install it for you. It works from mobile because the download and install happen inside Muse's workspace, not on your device.

To upgrade an existing install to the newest version, paste the same prompt again — it replaces the old folder.

---

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

---

What Muse should do with it, in short: download → unzip → place the `deep-research/` folder in the custom skills folder → verify → confirm. If any step fails (for example, the download is blocked), Muse should say which step failed rather than reporting success.
