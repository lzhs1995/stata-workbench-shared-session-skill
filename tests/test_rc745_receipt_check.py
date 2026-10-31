import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rc745_receipt_check", ROOT / "scripts/rc745_receipt_check.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


def write(path, value):
    path.write_bytes(value if isinstance(value, bytes) else json.dumps(value).encode())


def build(root, with_file=True):
    """Synthetic receipt in the exact rc.7.45 shared_stata.py layout (no Stata)."""
    token, rid = "a" * 32, "codex_1_x"
    marker = "___VERIFIED_CLIENT_" + token + "___"
    wire = {"code": 'do "x.do"\n#delimit cr\ndisplay as text "' + marker + '"\n', "cwd": "/w",
            "source": "agent", "agentId": "verified-shared-session-client", "label": "t"}
    body = {"ok": True, "rc": 0, "runId": rid, "requestId": "req1", "logPath": "/tmp/x.log"}
    log = ("display 1\n" + marker + "\n___CODEX_RUN_DONE_" + rid + "___\n").encode()
    status = {"ownedBackendPids": [4242]}
    result = {"verdict": rc.PASS, "postCount": 1, "retryCount": 0, "clientToken": token,
              "wireRequest": wire, "response": body, "http": 200,
              "checks": {"http200": True, "sameStataBackend": True}, "failedChecks": [],
              "before": {"status": status}, "after": {"status": dict(status)},
              "log": {"sha256": hashlib.sha256(log).hexdigest(), "bytes": len(log)}}
    if with_file:
        source = b"display 1\n"
        meta = {"authorPath": "/w/x.do", "path": str(root / "runtime-execution.do"),
                "bytes": len(source), "sha256": hashlib.sha256(source).hexdigest()}
        result["executionSource"] = meta
        write(root / "runtime-execution.do", source)
        write(root / "execution-source.json", meta)
    write(root / "wire-request.json", wire)
    write(root / "response.json", {"http": 200, "body": body})
    write(root / "run.log", log)
    write(root / "result.json", result)
    return result


class ReceiptCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def mutate_result(self, **changes):
        result = json.loads((self.root / "result.json").read_bytes())
        result.update(changes)
        write(self.root / "result.json", result)

    def test_pass_with_file_and_inline_code(self):
        build(self.root)
        self.assertEqual(rc.check(self.root)["verdict"], "PASS")
        with tempfile.TemporaryDirectory() as other:
            build(Path(other), with_file=False)
            out = rc.check(other)
            self.assertEqual(out["verdict"], "PASS")
            self.assertNotIn("executedBytesMatch", out["checks"])

    def test_non_pass_verdict_fails(self):
        build(self.root)
        self.mutate_result(verdict="EXECUTION_UNCONFIRMED_NO_RETRY")
        self.assertIn("verdictPass", rc.check(self.root)["failedChecks"])

    def test_retry_or_second_post_fails(self):
        build(self.root)
        self.mutate_result(postCount=2)
        self.assertIn("onePost", rc.check(self.root)["failedChecks"])

    def test_tampered_log_fails(self):
        build(self.root)
        write(self.root / "run.log", b"display 1\n")
        failed = rc.check(self.root)["failedChecks"]
        self.assertIn("logHashMatches", failed)
        self.assertIn("runMarkerInLog", failed)
        self.assertIn("clientMarkerInLog", failed)

    def test_changed_executed_bytes_fail(self):
        build(self.root)
        write(self.root / "runtime-execution.do", b"display 2\n")
        self.assertIn("executedBytesMatch", rc.check(self.root)["failedChecks"])

    def test_backend_change_fails(self):
        build(self.root)
        self.mutate_result(after={"status": {"ownedBackendPids": [5151]}})
        self.assertIn("sameBackend", rc.check(self.root)["failedChecks"])

    def test_failed_client_check_fails(self):
        build(self.root)
        self.mutate_result(checks={"http200": True, "sameStataBackend": False}, failedChecks=["sameStataBackend"])
        self.assertIn("allClientChecksTrue", rc.check(self.root)["failedChecks"])

    def test_nonzero_rc_fails(self):
        result = build(self.root)
        body = dict(result["response"], rc=603)
        write(self.root / "response.json", {"http": 200, "body": body})
        self.mutate_result(response=body)
        self.assertIn("rcZero", rc.check(self.root)["failedChecks"])


if __name__ == "__main__":
    unittest.main()
