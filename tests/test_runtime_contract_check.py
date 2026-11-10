import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("runtime_contract_check", ROOT / "scripts/runtime_contract_check.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
RUNTIME = os.environ.get("STATA_WORKBENCH_RUNTIME")

TOOL = '''import argparse
VERSION = "9.9.9"
BUNDLE_SHA256 = "{sha}"
p = argparse.ArgumentParser()
p.add_argument("--code"); p.add_argument("--file"); p.add_argument("--busy-policy")
'''


def make_runtime(root, sha_override=None):
    (root / "dist").mkdir(parents=True)
    (root / "tools").mkdir()
    bundle = b"synthetic bundle"
    (root / "dist/extension.js").write_bytes(bundle)
    sha = sha_override or hashlib.sha256(bundle).hexdigest()
    (root / "tools/shared_stata.py").write_text(TOOL.format(sha=sha))
    (root / "tools/verified_workbench.py").write_text(TOOL.format(sha=sha).replace("--code", "--status"))
    (root / "package.json").write_text(json.dumps({"version": "9.9.9", "contributes": {"commands": [
        {"command": "stata-workbench.runFile"}]}}))
    return hashlib.sha256(bundle).hexdigest()


def make_skill(root, body, bundle_sha, allow=None):
    (root / "skills/x").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "skills/x/SKILL.md").write_text(body)
    (root / "README.md").write_text("readme\n")
    (root / "scripts/known_external_flags.json").write_text(json.dumps({"options": allow or {}}))
    (root / "runtime-compatibility.json").write_text(json.dumps({"runtime": {
        "version": "9.9.9", "tag": "v9.9.9", "bundleSha256": bundle_sha}}))


GOOD = "Run `stata-workbench.runFile`.\n\n```sh\npython3 tools/shared_stata.py --file a.do --busy-policy wait\n```\n"


class ContractGate(unittest.TestCase):
    def run_gate(self, body, allow=None, sha_override=None, compat_sha=None):
        with tempfile.TemporaryDirectory() as tmp:
            runtime, skill = Path(tmp, "runtime"), Path(tmp, "skill")
            sha = make_runtime(runtime, sha_override)
            make_skill(skill, body, compat_sha or sha, allow)
            return gate.check(skill, runtime)

    def problems(self, out):
        return {p["problem"] for p in out["problems"]}

    def test_valid_skill_passes(self):
        out = self.run_gate(GOOD)
        self.assertEqual(out["verdict"], "PASS", out["problems"])
        self.assertEqual(out["optionsChecked"], 2)
        self.assertEqual(out["commandsChecked"], 1)

    def test_unknown_option_in_command_block_fails(self):
        out = self.run_gate(GOOD + "```sh\nfoo --resume-from x\n```\n")
        self.assertIn("UNKNOWN_OPTION", self.problems(out))

    def test_option_must_belong_to_named_script(self):
        out = self.run_gate(GOOD + "`verified_workbench.py --code x`\n")
        self.assertIn("OPTION_NOT_IN_NAMED_SCRIPT", self.problems(out))

    def test_prose_mentions_are_not_checked(self):
        self.assertEqual(self.run_gate(GOOD + "Older clients had --task in prose.\n")["verdict"], "PASS")

    def test_historical_option_allowed_inline_but_not_in_command_block(self):
        allow = {"--task": {"category": "historical"}}
        self.assertEqual(self.run_gate(GOOD + "No `--task` in rc.7.45.\n", allow)["verdict"], "PASS")
        out = self.run_gate(GOOD + "```sh\npython3 tools/shared_stata.py --task t.json\n```\n", allow)
        self.assertIn("HISTORICAL_OPTION_IN_COMMAND_BLOCK", self.problems(out))

    def test_unknown_command_fails(self):
        out = self.run_gate(GOOD + "Use `stata-workbench.runEverything`.\n")
        self.assertIn("UNKNOWN_COMMAND", self.problems(out))

    def test_vacuous_skill_fails(self):
        out = self.run_gate("No options or commands here.\n")
        self.assertIn("VACUOUS_SKILL", self.problems(out))

    def test_stale_bundle_pin_fails(self):
        out = self.run_gate(GOOD, compat_sha="0" * 64)
        self.assertIn("PIN_MISMATCH", self.problems(out))
        self.assertFalse(out["pins"]["bundleSha256MatchesCheckout"])

    def test_client_constant_mismatch_fails(self):
        out = self.run_gate(GOOD, sha_override="1" * 64)
        self.assertFalse(out["pins"]["clientPinsMatch"])

    def test_translated_readme_and_agents_md_are_checked(self):
        for name, extra, problem in (("README.zh-TW.md", "```sh\nfoo --nonexistent-audit-flag\n```\n", "UNKNOWN_OPTION"),
                                     ("README.zh-CN.md", "`shared_stata.py --status`\n", "OPTION_NOT_IN_NAMED_SCRIPT"),
                                     ("AGENTS.md", "Use `stata-workbench.nonexistentAuditCommand`.\n", "UNKNOWN_COMMAND")):
            with self.subTest(name), tempfile.TemporaryDirectory() as tmp:
                runtime, skill = Path(tmp, "runtime"), Path(tmp, "skill")
                make_skill(skill, GOOD, make_runtime(runtime))
                (skill / name).write_text(extra, encoding="utf-8")
                out = gate.check(skill, runtime)
                self.assertIn(name, out["markdownFiles"])
                self.assertIn(problem, self.problems(out))
                self.assertTrue(any(p.get("where", "").startswith(name) for p in out["problems"]), out["problems"])

    def test_commit_pin_compared_only_with_a_git_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime, skill = Path(tmp, "runtime"), Path(tmp, "skill")
            make_skill(skill, GOOD, make_runtime(runtime))
            out = gate.check(skill, runtime)
            self.assertEqual(out["verdict"], "PASS", out["problems"])
            self.assertIn("runtime.commit", out["notChecked"])
            git = ["git", "-C", str(runtime), "-c", "user.name=t", "-c", "user.email=t@example.invalid"]
            subprocess.run(git[:3] + ["init", "-q"], check=True)
            subprocess.run(git + ["add", "-A"], check=True)
            subprocess.run(git + ["commit", "-q", "-m", "synthetic"], check=True)
            head = subprocess.run(git[:3] + ["rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
            compat = json.loads((skill / "runtime-compatibility.json").read_text())
            compat["runtime"]["commit"] = "0" * 40
            (skill / "runtime-compatibility.json").write_text(json.dumps(compat))
            out = gate.check(skill, runtime)
            self.assertFalse(out["pins"]["commitMatchesCheckout"])
            self.assertIn("PIN_MISMATCH", self.problems(out))
            compat["runtime"]["commit"] = head
            (skill / "runtime-compatibility.json").write_text(json.dumps(compat))
            out = gate.check(skill, runtime)
            self.assertEqual(out["verdict"], "PASS", out["problems"])
            self.assertNotIn("runtime.commit", out["notChecked"])

    def test_vsix_pin_compared_only_with_a_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime, skill = Path(tmp, "runtime"), Path(tmp, "skill")
            make_skill(skill, GOOD, make_runtime(runtime))
            vsix = Path(tmp, "x.vsix")
            vsix.write_bytes(b"synthetic vsix")
            self.assertIn("runtime.vsixSha256", gate.check(skill, runtime)["notChecked"])
            out = gate.check(skill, runtime, vsix)
            self.assertFalse(out["pins"]["vsixSha256MatchesFile"])
            compat = json.loads((skill / "runtime-compatibility.json").read_text())
            compat["runtime"]["vsixSha256"] = hashlib.sha256(b"synthetic vsix").hexdigest()
            (skill / "runtime-compatibility.json").write_text(json.dumps(compat))
            out = gate.check(skill, runtime, vsix)
            self.assertEqual(out["verdict"], "PASS", out["problems"])
            self.assertNotIn("runtime.vsixSha256", out["notChecked"])

    @unittest.skipUnless(RUNTIME, "set STATA_WORKBENCH_RUNTIME to a v0.1.3-rc.7.45 checkout")
    def test_this_repository_against_pinned_runtime(self):
        out = gate.check(ROOT, RUNTIME)
        self.assertEqual(out["verdict"], "PASS", json.dumps(out["problems"], indent=1))
        self.assertGreater(out["optionsChecked"], 20)
        self.assertGreater(out["commandsChecked"], 3)


if __name__ == "__main__":
    unittest.main()
