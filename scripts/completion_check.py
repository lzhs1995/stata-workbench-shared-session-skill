"""Read-only independent receipt gate. Never executes, retries or alters Stata."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def read(path):
    return json.loads(Path(path).read_bytes())


def check_stage(directory):
    root = Path(directory).resolve(strict=True)
    result = read(root / "result.json")
    before, after = result.get("before", {}), result.get("after", {})
    response = result.get("response") or {}
    wire = read(root / "wire-request.json")
    frozen = (result.get("request") or {}).get("cowork") or {}
    finish = read(root / "visibility-finish.json")
    ticket = (finish.get("body") or {}).get("ticket") or {}
    prepared = (read(root / "visibility-prepare.json").get("body") or {}).get("ticket") or {}
    compilation = ticket.get("sourceCompilation") or {}
    executed = (root / "runtime-execution.do").read_bytes()
    executed_sha = hashlib.sha256(executed).hexdigest()
    compatibility = read(root / "execution-source.json").get("diagnostics") or {}
    log = (root / "run.log").read_bytes()
    token = result.get("clientToken")
    rid = response.get("runId")
    backend = (before.get("status") or {}).get("ownedBackendPids")
    lifecycle = response.get("lifecycle") or {}
    completed = (after.get("status") or {}).get("lastCompletedRun") or {}
    request_id = response.get("requestId")
    arguments = frozen.get("arguments", [])
    marker = "___VERIFIED_CLIENT_" + str(token) + "___"
    expected_code = 'display as text "' + marker + 'START"\ndo "' + str(ticket.get("program")) + '"'
    if isinstance(arguments, list) and all(isinstance(x, str) for x in arguments):
        expected_code += ''.join(' "' + x + '"' for x in arguments)
    expected_code += '\n#delimit cr\ndisplay as text "' + marker + '"\n'
    def marker_line(marker):
        lines = [re.sub(r"^(?:\{(?:res|txt|com|err|sf|bf|reset)\})+", "", line.strip()).strip()
                 for line in log.decode("utf8", errors="replace").splitlines()]
        return marker in lines
    checks = {
        "oneExecutionRequest": type(result.get("postCount")) is int and result["postCount"] == 1,
        "zeroRetries": type(result.get("retryCount")) is int and result["retryCount"] == 0,
        "executionConfirmed": result.get("executionVerdict") == "PASS_CONFIRMED",
        "runtimeSourceNotRewritten": result.get("sourceExecutionVerdict") == "NO_REFERENCED_COPY_REWRITE_REPORTED"
            and compatibility.get("referencedDoCopies") == [] and not compatibility.get("error")
            and compatibility.get("sourceMode") == "agent" and compatibility.get("runId") == request_id
            and compatibility == (after.get("status") or {}).get("sourceCompatibility"),
        "httpSuccess": type(result.get("http")) is int and result["http"] == 200 and response.get("ok") is True,
        "strictRc": type(response.get("rc")) is int and response["rc"] == 0,
        "backendMeasured": isinstance(backend, list) and bool(backend) and all(type(p) is int and p > 0 for p in backend) and len(set(backend)) == len(backend),
        "backendUnchanged": backend == (after.get("status") or {}).get("ownedBackendPids"),
        "independentCompletionBound": isinstance(rid, str) and rid == ((after.get("status") or {}).get("lastCompletedRun") or {}).get("runId"),
        "requestRunBinding": isinstance(request_id, str) and bool(request_id) and request_id == lifecycle.get("requestId") == completed.get("requestId") and lifecycle.get("runId") == rid,
        "newRun": isinstance(rid, str) and bool(rid) and rid != (before.get("status") or {}).get("runId"),
        "runMarkerInRawLog": isinstance(rid, str) and marker_line("___CODEX_RUN_DONE_" + rid + "___"),
        "clientMarkerInRawLog": isinstance(token, str) and bool(re.fullmatch("[a-f0-9]{32}", token)) and marker_line("___VERIFIED_CLIENT_" + token + "___"),
        "rawLogHash": hashlib.sha256(log).hexdigest() == (result.get("log") or {}).get("sha256"),
        "visibilityFinishOk": type(finish.get("http")) is int and finish["http"] == 200 and (finish.get("body") or {}).get("ok") is True,
        "ticketFinished": ticket.get("phase") == "finished",
        "ticketBound": wire.get("coworkToken") is not None and wire.get("coworkToken") == (read(root / "visibility-prepare.json").get("body") or {}).get("token"),
        "visibilityUninterrupted": ticket.get("visibilityInterrupted") is False and ticket.get("evidenceOverflow") is False,
        "visibilityVerdict": ticket.get("visibilityVerdict") == "OBSERVED_VISIBLE",
        "inputProgramBound": ticket.get("inputProgram") == frozen.get("program") and ticket.get("inputSha256") == frozen.get("sha256"),
        "executionProgramBound": isinstance(ticket.get("program"), str) and ticket.get("sha256") == executed_sha
            and (result.get("runtimeSource") or {}).get("sha256") == executed_sha
            and (result.get("runtimeSource") or {}).get("path") == ticket.get("program"),
        "compilationBound": compilation.get("stable") is True and compilation.get("inputProgram") == frozen.get("program")
            and compilation.get("inputSha256") == frozen.get("sha256") and compilation.get("program") == ticket.get("program")
            and compilation.get("sha256") == executed_sha and result.get("sourceCompilation") == compilation,
        "preparedExecutionUnchanged": all(prepared.get(k) == ticket.get(k) for k in
            ("program", "sha256", "inputProgram", "inputSha256", "sourceCompilation", "arguments", "cwd")),
        "wireBytesBound": wire.get("code") == expected_code and wire.get("coworkMarker") == marker
            and ticket.get("arguments") == arguments,
        "workingDirectoryBound": isinstance(ticket.get("cwd"), str) and ticket.get("cwd") == wire.get("cwd")
            == (result.get("request") or {}).get("cwd"),
        "visibilityEventsPresent": isinstance(ticket.get("events"), list) and len(ticket["events"]) >= 3,
        "allObservedLayoutsPassed": isinstance(ticket.get("events"), list) and bool(ticket["events"]) and all(e.get("ok") is True for e in ticket["events"]),
    }
    records = frozen.get("files")
    checks["frozenFilesPresent"] = isinstance(records, list) and bool(records)
    checks["frozenFilesExact"] = checks["frozenFilesPresent"] and all(
        hashlib.sha256(Path(r["execution"]["path"]).read_bytes()).hexdigest() == r["execution"]["sha256"]
        and r["source"]["sha256"] == r["execution"]["sha256"] for r in records)
    checks["mainFileInManifest"] = checks["frozenFilesPresent"] and any(
        r.get("execution", {}).get("path") == frozen.get("program")
        and r.get("execution", {}).get("sha256") == frozen.get("sha256") for r in records)
    # Scope explicitly excludes claims that a person watched, or replay ran twice.
    return {"verdict": "PASS_EXECUTION_AND_OBSERVED_VISIBILITY" if all(checks.values()) else "FAIL",
            "checks": checks, "replay": "NOT_PROVEN_BY_ONE_RECEIPT", "humanWatched": "NOT_MEASURABLE"}


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("receipt", type=Path); a = p.parse_args()
    try:
        value = check_stage(a.receipt)
    except Exception as e:
        value = {"verdict": "FAIL", "error": str(e)}
    print(json.dumps(value, ensure_ascii=False, indent=2))
    raise SystemExit(0 if value["verdict"] == "PASS_EXECUTION_AND_OBSERVED_VISIBILITY" else 2)
