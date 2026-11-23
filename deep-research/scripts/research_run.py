#!/usr/bin/env python3
"""Bookkeeping for deep-research runs.

A project is a folder with a shared notes vault. A run is one research
question inside a project, identified by a vault tag (slug + 6 hex chars).

Usage:
  research_run.py init --project DIR --query "the research question" [--tier light|full]
  research_run.py step --project DIR --tag TAG --step "5-depth-investigation" [--note "..."]
  research_run.py status --project DIR [--tag TAG]
  research_run.py finish --project DIR --tag TAG

Layout:
  <project>/research/notes/                 shared pool of source notes + final reports
  <project>/research/runs/<tag>/run.json    the run manifest (steps, counts)
  <project>/research/runs/<tag>/temp/       scratch for the run
  <project>/research/raw/                   fetched source text
"""
import argparse
import json
import os
import re
import secrets
import sys
import time
from datetime import datetime, timezone

TAG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def check_tag(tag):
    if not TAG_RE.match(tag or ""):
        print(f"Error: invalid tag format: {tag!r} (expected lowercase slug + hex suffix)")
        sys.exit(2)
    return tag


class ManifestLock:
    """Simple cross-process lockfile so parallel step recordings cannot
    interleave a load/save and lose each other's updates."""

    def __init__(self, project, tag):
        self.lock_path = os.path.join(project, "research", "runs", tag, ".lock")
        self.fd = None

    def __enter__(self):
        deadline = time.time() + 30
        while True:
            try:
                self.fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.time() > deadline:
                    print("Error: timed out waiting for the run manifest lock")
                    sys.exit(3)
                time.sleep(0.05)

    def __exit__(self, *exc):
        if self.fd is not None:
            os.close(self.fd)
        try:
            os.unlink(self.lock_path)
        except FileNotFoundError:
            pass

TIER_STEPS = {
    "light": ["1-decompose", "2-width-sweep", "10-triple-draft", "15-polish", "16-readability-audit"],
    "full": ["1-decompose", "2-width-sweep", "3-contradiction-graph", "4-loci-analysis",
             "5-depth-investigation", "6-cross-locus-reconcile", "7-source-tensions",
             "8-corpus-critic", "9-evidence-digest", "10-triple-draft", "11-synthesize",
             "12-critics", "13-gap-fetch", "14-patcher", "14.5-cite-check",
             "15-polish", "16-readability-audit"],
}


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return "-".join(slug.split("-")[:5]) or "research"


def run_path(project, tag):
    return os.path.join(project, "research", "runs", check_tag(tag), "run.json")


def load_manifest(project, tag):
    with open(run_path(project, tag)) as f:
        return json.load(f)


def save_manifest(project, manifest):
    path = run_path(project, manifest["vault_tag"])
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w") as f:
        json.dump(manifest, f, indent=1)
    os.replace(tmp, path)


def now():
    return datetime.now(timezone.utc).isoformat()


def cmd_init(args):
    project = os.path.expanduser(args.project)
    tag = f"{slugify(args.query)}-{secrets.token_hex(3)}"
    for sub in ("research/notes", "research/raw", f"research/runs/{tag}/temp"):
        os.makedirs(os.path.join(project, sub), exist_ok=True)
    manifest = {
        "vault_tag": tag,
        "query": args.query,
        "tier": args.tier,
        "status": "running",
        "created": now(),
        "steps_planned": TIER_STEPS[args.tier],
        "steps_done": [],
        "notes": [],
    }
    save_manifest(project, manifest)
    print(tag)


def cmd_step(args):
    project = os.path.expanduser(args.project)
    check_tag(args.tag)
    with ManifestLock(project, args.tag):
        manifest = load_manifest(project, args.tag)
        if args.step not in manifest["steps_planned"]:
            print(f"Error: step {args.step!r} is not in this run's plan ({', '.join(manifest['steps_planned'])})")
            sys.exit(1)
        manifest["steps_done"].append({"step": args.step, "at": now(), "note": args.note or ""})
        save_manifest(project, manifest)
    done = {s["step"] for s in manifest["steps_done"]}
    left = [s for s in manifest["steps_planned"] if s not in done]
    print(f"{args.step} recorded. {len(done)}/{len(manifest['steps_planned'])} steps done. Remaining: {', '.join(left) or 'none'}")


def cmd_status(args):
    project = os.path.expanduser(args.project)
    runs_dir = os.path.join(project, "research", "runs")
    tags = [args.tag] if args.tag else sorted(os.listdir(runs_dir)) if os.path.exists(runs_dir) else []
    for tag in tags:
        m = load_manifest(project, tag)
        done = {s["step"] for s in m["steps_done"]}
        print(f"{tag}  [{m['tier']}]  {m['status']}  steps {len(done)}/{len(m['steps_planned'])}")
        print(f"  query: {m['query'][:100]}")


def cmd_finish(args):
    project = os.path.expanduser(args.project)
    manifest = load_manifest(project, args.tag)
    done = {s["step"] for s in manifest["steps_done"]}
    missing = [s for s in manifest["steps_planned"] if s not in done]
    report = os.path.join(project, "research", "notes", f"final_report_{args.tag}.md")
    if missing:
        print(f"NOT FINISHED. Missing steps: {', '.join(missing)}")
        sys.exit(1)
    if not os.path.exists(report):
        print(f"NOT FINISHED. Report missing: {report}")
        sys.exit(1)
    with ManifestLock(project, args.tag):
        manifest = load_manifest(project, args.tag)
        manifest["status"] = "complete"
        manifest["finished"] = now()
        save_manifest(project, manifest)
    print(f"passed: true  report: {report}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("--project", required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--tier", choices=["light", "full"], default="full")
    p = sub.add_parser("step")
    p.add_argument("--project", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--step", required=True)
    p.add_argument("--note", default="")
    p = sub.add_parser("status")
    p.add_argument("--project", required=True)
    p.add_argument("--tag")
    p = sub.add_parser("finish")
    p.add_argument("--project", required=True)
    p.add_argument("--tag", required=True)
    args = ap.parse_args()
    {"init": cmd_init, "step": cmd_step, "status": cmd_status, "finish": cmd_finish}[args.cmd](args)


if __name__ == "__main__":
    main()
