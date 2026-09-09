import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("completion", Path(__file__).resolve().parents[1] / "scripts/completion_check.py")
completion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(completion)


class CompletionTests(unittest.TestCase):
    def fixture(self, root):
        source = root / "stage.do"; source.write_text("display 1\n")
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        token = "a" * 32
        log = ("___VERIFIED_CLIENT_" + token + "___\n___CODEX_RUN_DONE_run1___\n").encode()
        (root / "run.log").write_bytes(log)
        file = {"path": str(source), "sha256": sha}
        frozen = {"program": str(source), "sha256": sha, "arguments": [], "files": [{"source": file, "execution": file}]}
        compilation = {"program":str(source), "sha256":sha, "inputProgram":str(source), "inputSha256":sha, "stable":True}
        compatibility = {"referencedDoCopies":[], "sourceMode":"agent", "runId":"req1"}
        (root / "runtime-execution.do").write_bytes(source.read_bytes())
        result = {"postCount": 1, "retryCount": 0, "http": 200, "executionVerdict": "PASS_CONFIRMED",
            "sourceExecutionVerdict": "NO_REFERENCED_COPY_REWRITE_REPORTED",
            "request": {"cowork": frozen, "cwd":str(root)}, "clientToken": token,
            "runtimeSource":file, "sourceCompilation":compilation,
            "response": {"ok": True, "rc": 0, "runId": "run1", "requestId": "req1", "lifecycle": {"runId": "run1", "requestId": "req1"}},
            "before": {"status": {"runId": "old", "ownedBackendPids": [123]}},
            "after": {"status": {"ownedBackendPids": [123], "sourceCompatibility":compatibility, "lastCompletedRun": {"runId": "run1", "requestId": "req1"}}},
            "log": {"sha256": hashlib.sha256(log).hexdigest()}}
        ticket = {"program": str(source), "sha256": sha, "phase": "finished", "visibilityInterrupted": False,
            "inputProgram":str(source), "inputSha256":sha, "sourceCompilation":compilation, "arguments":[], "cwd":str(root),
            "evidenceOverflow": False, "visibilityVerdict": "OBSERVED_VISIBLE", "events": [{"ok": True}] * 3}
        values = {"result.json": result, "visibility-finish.json": {"http": 200, "body": {"ok": True, "ticket": ticket}},
            "execution-source.json": {"diagnostics": compatibility},
            "wire-request.json": {"coworkToken": "ticket", "cwd":str(root), "coworkMarker":"___VERIFIED_CLIENT_"+token+"___",
                "code":'display as text "___VERIFIED_CLIENT_'+token+'___START"\ndo "'+str(source)+'"\n#delimit cr\ndisplay as text "___VERIFIED_CLIENT_'+token+'___"\n'},
            "visibility-prepare.json": {"body": {"token": "ticket", "ticket":copy.deepcopy(ticket)}}}
        return values

    def write(self, root, values):
        for name, value in values.items(): (root / name).write_text(json.dumps(value))

    def test_positive_has_narrow_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); values = self.fixture(root); self.write(root, values)
            out = completion.check_stage(root)
            self.assertEqual(out["verdict"], "PASS_EXECUTION_AND_OBSERVED_VISIBILITY")
            self.assertEqual(out["replay"], "NOT_PROVEN_BY_ONE_RECEIPT")
            self.assertEqual(out["humanWatched"], "NOT_MEASURABLE")

    def test_transformed_execution_archive_is_bound_separately_from_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); values=self.fixture(root)
            archive=root/"runtime-execution.do"; archive.write_text("* compiled variant\ndisplay 1\n")
            digest=hashlib.sha256(archive.read_bytes()).hexdigest()
            compiled_path=str(root/"compiled-temporary.do")
            for name in ("visibility-prepare.json", "visibility-finish.json"):
                t=values[name]["body"]["ticket"]
                t.update(program=compiled_path,sha256=digest)
                t["sourceCompilation"].update(program=compiled_path,sha256=digest,changed=True)
            values["result.json"]["runtimeSource"]={"path":compiled_path,"sha256":digest}
            wire=values["wire-request.json"]
            wire["code"]=wire["code"].replace(str(root/"stage.do"),compiled_path)
            self.write(root,values)
            self.assertEqual(completion.check_stage(root)["verdict"],"PASS_EXECUTION_AND_OBSERVED_VISIBILITY")
            archive.write_text("tampered")
            self.assertFalse(completion.check_stage(root)["checks"]["executionProgramBound"])

    def test_all_measurements_are_required_no_absence_as_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); base = self.fixture(root)
            mutations = [
                ("result.json", ("postCount",), True),
                ("result.json", ("retryCount",), None),
                ("result.json", ("response", "rc"), False),
                ("result.json", ("response", "lifecycle", "requestId"), "wrong"),
                ("result.json", ("after", "status", "ownedBackendPids"), [124]),
                ("result.json", ("log", "sha256"), "wrong"),
                ("visibility-finish.json", ("body", "ticket", "events"), []),
                ("visibility-finish.json", ("body", "ticket", "visibilityInterrupted"), True),
                ("visibility-finish.json", ("body", "ticket", "phase"), "running"),
                ("wire-request.json", ("coworkToken",), "wrong"),
                ("wire-request.json", ("cwd",), "/wrong"),
                ("wire-request.json", ("code",), "clear all"),
                ("visibility-prepare.json", ("body", "ticket", "sha256"), "wrong"),
                ("result.json", ("sourceCompilation", "stable"), False),
                ("execution-source.json", ("diagnostics", "runId"), "stale"),
                ("execution-source.json", ("diagnostics", "referencedDoCopies"), [{"tempPath": "hidden.do"}]),
            ]
            for name, keys, value in mutations:
                with self.subTest(keys=keys):
                    data = copy.deepcopy(base); obj = data[name]
                    for key in keys[:-1]: obj = obj[key]
                    obj[keys[-1]] = value; self.write(root, data)
                    self.assertEqual(completion.check_stage(root)["verdict"], "FAIL")

    def test_echoed_marker_is_not_executed_marker_and_file_drift_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); values = self.fixture(root)
            raw = b'. display "___CODEX_RUN_DONE_run1___"\n'
            (root / "run.log").write_bytes(raw)
            values["result.json"]["log"]["sha256"] = hashlib.sha256(raw).hexdigest()
            self.write(root, values)
            out = completion.check_stage(root)
            self.assertFalse(out["checks"]["runMarkerInRawLog"])
            (root / "stage.do").write_text("changed")
            self.assertFalse(completion.check_stage(root)["checks"]["frozenFilesExact"])

    def test_real_smcl_style_prefixes_are_not_mistaken_for_missing_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); values = self.fixture(root)
            raw = b"".join(b"{res}{txt}" + line + b"\n" for line in (root / "run.log").read_bytes().splitlines())
            (root / "run.log").write_bytes(raw)
            values["result.json"]["log"]["sha256"] = hashlib.sha256(raw).hexdigest()
            self.write(root, values)
            self.assertEqual(completion.check_stage(root)["verdict"], "PASS_EXECUTION_AND_OBSERVED_VISIBILITY")


if __name__ == "__main__": unittest.main()
