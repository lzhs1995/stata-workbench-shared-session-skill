"""Bind rc745_receipt_check to receipts written by the real rc.7.45 client.

Needs a checkout of the runtime at tag v0.1.3-rc.7.45 in STATA_WORKBENCH_RUNTIME
(CI provides it). The client runs with mocked bridge and observation only; no
Stata, VS Code or network is touched.
"""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = os.environ.get("STATA_WORKBENCH_RUNTIME")
spec = importlib.util.spec_from_file_location("rc745_receipt_check", ROOT / "scripts/rc745_receipt_check.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


def state(rid):
    s = {"busy": False, "postRunBusy": False, "trueReady": True, "recovery": {"required": False},
         "runId": rid, "requestId": "req-" + rid, "ownedBackendPids": [14], "lifecycleVersion": "rc7.27",
         "completionMarkerVerified": True, "perRunCompletionMarkerVerified": True, "perRunEvidenceFailure": None}
    s["lastCompletedRun"] = dict(s)
    return {"identityOk": True, "axWindowCount": 1, "launcherPid": 12,
            "windowObservation": {"ok": True, "count": 1, "status": "OK"},
            "owner": {"pid": 13, "ppid": 12}, "status": s}


@unittest.skipUnless(RUNTIME, "set STATA_WORKBENCH_RUNTIME to a v0.1.3-rc.7.45 checkout")
class RealClientReceipt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(Path(RUNTIME) / "tools"))
        import shared_stata
        cls.client = shared_stata

    def run_client(self, root, source=None, log_text=None):
        log = root / "bridge.log"
        log.write_bytes((log_text or "___VERIFIED_CLIENT_tok___\n___CODEX_RUN_DONE_new___\n").encode())
        body = {"ok": True, "rc": 0, "runId": "new", "requestId": "req-new", "logPath": str(log),
                "lifecycle": {"requestId": "req-new", "runId": "new", "sourceMode": "agent"}}
        d = SimpleNamespace(w=SimpleNamespace(http_post=Mock(return_value=(200, body))))
        with patch.object(self.client.uuid, "uuid4", return_value=SimpleNamespace(hex="tok")):
            return self.client.execute_once(d, {"code": "display 1"}, root / "receipt",
                                            observe=Mock(side_effect=[state("old"), state("new")]),
                                            source_path=source)

    def test_real_pass_receipt_rechecks_as_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "author.do"
            source.write_bytes(b"display 1\n")
            result = self.run_client(root, source=source)
            self.assertEqual(result["verdict"], rc.PASS)
            out = rc.check(root / "receipt")
            self.assertEqual(out["failedChecks"], [])
            self.assertIn("executedBytesMatch", out["checks"])

    def test_real_unconfirmed_receipt_rechecks_as_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_client(root, log_text="no markers\n")
            self.assertEqual(result["verdict"], "EXECUTION_UNCONFIRMED_NO_RETRY")
            out = rc.check(root / "receipt")
            self.assertEqual(out["verdict"], "FAIL")
            self.assertIn("verdictPass", out["failedChecks"])


if __name__ == "__main__":
    unittest.main()
