"""Tests for the deep-research skill's bookkeeping script.

Covers the behaviors the adversarial review flagged: tag validation
(path traversal), step validation, manifest locking under parallel
step recording, and the init -> step -> finish flow.
"""
import importlib.util
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import pytest

SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "deep-research", "scripts", "research_run.py"
)

spec = importlib.util.spec_from_file_location("research_run", SCRIPT)
rr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rr)


def run_cli(*argv):
    return subprocess.run(
        [sys.executable, SCRIPT, *argv], capture_output=True, text=True
    )


def init_project(tmp_path, tier="light"):
    result = run_cli(
        "init", "--project", str(tmp_path), "--query", "a test question", "--tier", tier
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_slugify_basic():
    assert rr.slugify("What Is The Best EV?") == "what-is-the-best-ev"
    assert rr.slugify("") == "research"
    assert rr.slugify("!!!") == "research"


def test_check_tag_rejects_traversal():
    for bad in ("../../etc/evil", "..", "a/b", "UPPER", "", "-leading-dash", "has space"):
        with pytest.raises(SystemExit):
            rr.check_tag(bad)


def test_check_tag_accepts_generated_shape():
    assert rr.check_tag("a-test-question-1f154b") == "a-test-question-1f154b"


def test_step_rejects_unplanned_step(tmp_path):
    tag = init_project(tmp_path)
    result = run_cli("step", "--project", str(tmp_path), "--tag", tag, "--step", "bogus")
    assert result.returncode == 1
    assert "not in this run's plan" in result.stdout


def test_step_rejects_traversal_tag(tmp_path):
    init_project(tmp_path)
    result = run_cli(
        "step", "--project", str(tmp_path), "--tag", "../../etc/evil", "--step", "1-decompose"
    )
    assert result.returncode == 2
    assert "invalid tag format" in result.stdout


def test_finish_requires_all_steps_and_report(tmp_path):
    tag = init_project(tmp_path)
    result = run_cli("finish", "--project", str(tmp_path), "--tag", tag)
    assert result.returncode == 1
    assert "Missing steps" in result.stdout
    for step in rr.TIER_STEPS["light"]:
        assert run_cli("step", "--project", str(tmp_path), "--tag", tag, "--step", step).returncode == 0
    result = run_cli("finish", "--project", str(tmp_path), "--tag", tag)
    assert result.returncode == 1
    assert "Report missing" in result.stdout
    report = tmp_path / "research" / "notes" / f"final_report_{tag}.md"
    report.write_text("# report\n")
    result = run_cli("finish", "--project", str(tmp_path), "--tag", tag)
    assert result.returncode == 0
    assert "passed: true" in result.stdout


def test_parallel_step_recording_loses_nothing(tmp_path):
    tag = init_project(tmp_path, tier="full")
    steps = rr.TIER_STEPS["full"][:8]

    def record(step):
        return run_cli("step", "--project", str(tmp_path), "--tag", tag, "--step", step)

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(record, steps))
    assert all(r.returncode == 0 for r in results), [r.stdout + r.stderr for r in results]
    manifest = json.loads((tmp_path / "research" / "runs" / tag / "run.json").read_text())
    assert {s["step"] for s in manifest["steps_done"]} == set(steps)
