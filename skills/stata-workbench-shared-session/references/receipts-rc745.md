# rc.7.45 receipts and the offline re-check

`tools/shared_stata.py` writes one receipt directory per call (default
`./.stata-receipts/shared_<uuid>`, or `--receipt-dir`, which must not exist).
Files are written once and never overwritten.

| File | Written when | Content |
| --- | --- | --- |
| `request.json` | session was ready, before the POST | code, cwd, source `agent`, label |
| `before.json` | same | observation before the POST: identity, window, `/status` |
| `runtime-execution.do` | with `--file` | exact bytes of the author file, frozen before the POST |
| `execution-source.json` | with `--file` | author path, frozen path, bytes, sha256 |
| `wire-request.json` | just before the POST | exact payload, ending with `display as text "___VERIFIED_CLIENT_<token>___"` |
| `response.json` | after the POST returned | HTTP status and body |
| `response-diagnostics.json` | same | runId/requestId/rc/logPath from the body or a nested error envelope |
| `run.log` | only on PASS | copy of the run log containing both completion markers |
| `result.json` | always | verdict, postCount, retryCount, checks, failedChecks, before/after, error |

Reading a receipt:
- No `wire-request.json`: nothing was sent by this call.
- `wire-request.json` present: one POST was made (`postCount` 1). Even without
  `response.json`, Stata may have run it. Do not resend.
- `result.json.checks` lists each completion check; `failedChecks` names the
  ones that were not true.

## Re-check a PASS offline

```sh
python3 -B scripts/rc745_receipt_check.py /abs/receipt-dir
```

It re-derives the PASS from the files: verdict, one POST and zero retries, all
client checks true, the wire request from `agent` ending with the client marker,
HTTP 200 with `ok` and `rc` 0, the log's sha256 and both markers
(`___CODEX_RUN_DONE_<runId>___` and the client marker), the same backend PID
before and after, and with `--file` the frozen bytes' sha256. Exit 0 = PASS,
2 = FAIL. It certifies what the client recorded, not that a person watched.

`scripts/completion_check.py` checks receipts of the earlier candidate client
(`visibility-prepare.json`, `visibility-finish.json`); it does not apply to
rc.7.45 receipts.
