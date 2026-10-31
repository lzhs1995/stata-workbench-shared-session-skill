"""Read-only re-check of one rc.7.45 `tools/shared_stata.py` receipt directory.

Never contacts the bridge, executes, retries or alters Stata. It re-derives the
client's PASS from the files the rc.7.45 client writes, so an agent can confirm a
reported PASS without trusting the printed JSON line.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

PASS = "PASS_VISIBLE_SHARED_RUN"


def _read(path):
    return json.loads(Path(path).read_bytes())


def check(directory):
    root = Path(directory).resolve(strict=True)
    result = _read(root / "result.json")
    wire = _read(root / "wire-request.json")
    response = _read(root / "response.json")
    body = response.get("body") if isinstance(response.get("body"), dict) else {}
    token = result.get("clientToken")
    rid = body.get("runId")
    log_path = root / "run.log"
    log = log_path.read_bytes() if log_path.is_file() else b""
    log_meta = result.get("log") or {}
    before = (result.get("before") or {}).get("status") or {}
    after = (result.get("after") or {}).get("status") or {}
    client_marker = "___VERIFIED_CLIENT_" + str(token) + "___"
    checks = {
        "verdictPass": result.get("verdict") == PASS,
        "onePost": type(result.get("postCount")) is int and result["postCount"] == 1,
        "zeroRetries": type(result.get("retryCount")) is int and result["retryCount"] == 0,
        "allClientChecksTrue": isinstance(result.get("checks"), dict) and bool(result["checks"])
            and all(v is True for v in result["checks"].values()) and result.get("failedChecks") == [],
        "wireFromAgent": wire.get("source") == "agent" and isinstance(token, str) and bool(token)
            and str(wire.get("code", "")).endswith('display as text "' + client_marker + '"\n'),
        "wireMatchesResult": wire == result.get("wireRequest"),
        "http200Ok": response.get("http") == 200 and body.get("ok") is True and body == result.get("response"),
        "rcZero": type(body.get("rc")) is int and body["rc"] == 0,
        "logHashMatches": bool(log) and log_meta.get("sha256") == hashlib.sha256(log).hexdigest()
            and log_meta.get("bytes") == len(log),
        "runMarkerInLog": isinstance(rid, str) and bool(rid) and ("___CODEX_RUN_DONE_" + rid + "___").encode() in log,
        "clientMarkerInLog": client_marker.encode() in log,
        "sameBackend": isinstance(before.get("ownedBackendPids"), list) and bool(before["ownedBackendPids"])
            and before["ownedBackendPids"] == after.get("ownedBackendPids"),
    }
    source = result.get("executionSource")
    if source is not None:
        executed = (root / "runtime-execution.do").read_bytes()
        checks["executedBytesMatch"] = (source == _read(root / "execution-source.json")
            and source.get("sha256") == hashlib.sha256(executed).hexdigest() and source.get("bytes") == len(executed))
    failed = [name for name, ok in checks.items() if ok is not True]
    return {"verdict": "PASS" if not failed else "FAIL", "receipt": str(root), "runId": rid,
            "checks": checks, "failedChecks": failed,
            "note": "Certifies execution and identity recorded by the client, not that a person watched the run."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        out = check(args.receipt)
    except (OSError, ValueError) as error:
        out = {"verdict": "FAIL", "receipt": str(args.receipt), "error": repr(error)}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["verdict"] == "PASS" else 2)
