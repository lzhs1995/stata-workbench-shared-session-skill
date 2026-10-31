---
name: stata-workbench-shared-session
description: Use when an agent must run Stata code in the user's existing Stata Workbench Shared Session (VS Code extension, runtime v0.1.3-rc.7.45) so that the person and the agent share one visible Stata session: same data, macros, estimates and graphs. Covers setup on macOS and Windows, the agent client tools/shared_stata.py, Stop, receipts and exit codes, known limitations and recovery. Not for statistical model selection.
---

# Stata Workbench Shared Session (runtime v0.1.3-rc.7.45)

## 1. What this is

- A VS Code extension holds **one** Stata session. The person runs code from the
  editor (Run Current File, Run Selection, the Stata Terminal); the agent sends
  code to the **same** session through a loopback HTTP bridge with
  `tools/shared_stata.py`. Data, macros, scalars, `e()`/`r()` results and graphs
  are shared, and the agent's output appears in the person's Stata Terminal.
- One backend runs one request at a time. The person and the agent take turns.
- Shared memory is not durable storage. Save data and results to disk before a
  reset, a restart or closing VS Code.
- Runtime repository: https://github.com/lzhs1995/stata-workbench-shared-session
  (tag `v0.1.3-rc.7.45`). The pins this skill was checked against are in
  `runtime-compatibility.json` at the skill repository root (installed copy: two
  directories above this file).

## 2. First decide who runs the code

| Situation | Who runs it | How |
| --- | --- | --- |
| The agent must execute analysis code | Agent | `tools/shared_stata.py --file <saved .do>` (section 4) |
| The person wants to step through it | Person | Save the `.do`; the person uses **Stata: Run Current File** or **Stata: Run Selection/Current Line** |
| The session is busy, STALE or not found | Nobody yet | Read the state first (section 4, `--status`), then section 7 |
| The person asks to stop the current run | Person or agent | Section 5 |

Default: write commented `.do` programs, show them, run and check each stage
automatically. **Do not ask for per-stage approval.** Announce the purpose and
code changes briefly; the person may watch, edit or press Stop at any time.

Editor commands the person uses (the agent tells them which; it does not press keys):

| Command palette title | Command id | Keys |
| --- | --- | --- |
| Stata: Run Current File | `stata-workbench.runFile` | `Ctrl+Shift+D` (macOS `Cmd+Shift+D`) |
| Stata: Run Selection/Current Line | `stata-workbench.runSelection` | `Ctrl+Shift+Enter` (macOS `Cmd+Shift+Enter`) |
| Stata: Open Interactive Terminal | `stata-workbench.openTerminal` | `Ctrl+Shift+C` (macOS `Cmd+Shift+C`) |
| Stata: View Data | `stata-workbench.viewData` | also the **Data Browser** button in the Terminal |
| Stata: Cancel Current Request | `stata-workbench.cancelRequest` | the **Stop** button in the Terminal is the documented route |
| Stata: Test MCP Server Connection | `stata-workbench.testMcpServer` | |

The run keys apply when a `.do`, `.ado` or `.mata` file has focus. Graph
thumbnails in the Terminal open in **Stata Graphs** with **Open**, without
running Stata again.

## 3. Three-minute start

The tools live in the runtime repository, not in the VSIX. Use a clone checked
out at the same tag as the installed VSIX. `STATA_WORKBENCH_PROFILE` and
`STATA_WORKBENCH_PORT` must name the profile and port the person actually uses;
the port must equal the profile's `stataMcp.visibleBridgePort`. The README
defaults are `~/.stata-workbench-shared` and `17485`; do not assume them for an
existing installation; ask the person or read their setup notes.

macOS:

```sh
git clone https://github.com/lzhs1995/stata-workbench-shared-session.git
cd stata-workbench-shared-session && git checkout v0.1.3-rc.7.45
export STATA_WORKBENCH_PROFILE="$HOME/.stata-workbench-shared"   # the person's profile
export STATA_WORKBENCH_PORT=17485                                 # the person's port
python3 -B tools/verified_workbench.py --doctor     # JSON; never starts VS Code or Stata
python3 -B tools/verified_workbench.py --status     # read-only; exit 0 = identity ok and exactly 1 window
python3 -B tools/shared_stata.py --code 'display 1+1' --cwd "$PWD"
```

Windows (PowerShell 5.1 or 7; use the installed `python.exe`, not the Microsoft
Store `python` alias):

```powershell
git clone https://github.com/lzhs1995/stata-workbench-shared-session.git
cd stata-workbench-shared-session; git checkout v0.1.3-rc.7.45
$env:STATA_WORKBENCH_PROFILE = Join-Path $HOME '.stata-workbench-shared'   # the person's profile
$env:STATA_WORKBENCH_PORT = '17485'                                         # the person's port
python -B tools/verified_workbench.py --doctor
python -B tools/verified_workbench.py --status
python -B tools/shared_stata.py --code 'display 1+1' --cwd "$PWD"
```

`$env:` variables apply to the current PowerShell window only.

The last line prints one JSON line and exits 0 with verdict
`PASS_VISIBLE_SHARED_RUN` when the session is healthy. If the person has not
installed the extension yet, follow the runtime README sections *Install* and
*Quick start*; macOS also needs `--request-permissions` once (section 9).

The first run after opening or reloading VS Code also starts the Stata service.
Measured: 14.1 s (macOS) and 25.2 s (Windows) on dev.8; backend start 31.3 s on
Windows with rc.7.45. Wait for it and do not submit again. The only safe
resubmission is HTTP 504 `PRE_RUN_SNAPSHOT_TIMEOUT`: that run was refused before
the code was sent (`payloadDispatched: false`).

The client needs a running backend. It never launches, activates, resets or
retries Stata. After the person opens or reloads VS Code, the service starts on
the first editor run or Terminal command (Run File, Run Selection or any
Terminal command). Until then the agent's call returns `BLOCKED_NO_DISPATCH`;
ask the person to run one command, for example `display 1` in the Terminal.

## 4. Agent client reference

`tools/verified_workbench.py` (exactly one mode):

| Option | Effect |
| --- | --- |
| `--doctor` | Host, permission, window, profile, port and Stata diagnosis as JSON; exit 0 only for verdict `READY`. Never starts anything |
| `--status` | Read-only observation of the bound session as JSON; exit 0 when identity is ok and the profile has exactly one window |
| `--open` | Reuse the exact profile or launch it once; add `--workspace <dir>`. With a new launch only: `--no-activate`, `--remote-debugging-port <n>`, `--disable-workspace-trust` |
| `--request-permissions` | macOS: one read-only System Events query that may show the consent prompt |

`tools/shared_stata.py` (one of `--code` / `--file` is required):

| Option | Default | Meaning |
| --- | --- | --- |
| `--code '<stata>'` | — | Inline Stata code |
| `--file <path.do>` | — | A saved do-file. Its bytes are copied into the receipt as `runtime-execution.do` and that copy is run with `do`; the sha256 is recorded |
| `--cwd <dir>` | current dir | Working directory for the run; must exist |
| `--receipt-dir <new dir>` | `./.stata-receipts/shared_<uuid>` | Must not exist yet |
| `--timeout <s>` | 3600 | HTTP wait for this POST. A timeout does not prove that Stata stopped |
| `--busy-policy fail\|wait` | `fail` | `wait` polls before submitting, up to `--max-wait` seconds; it never waits after the POST |
| `--max-wait <s>` | 60 | Pre-submit wait for `--busy-policy wait` |
| `--label '<text>'` | `Shared session AI run` | Title of the Terminal entry for this run |

Before sending, the client requires: the exact profile and bundle, exactly one
VS Code window for that profile, `identityOk`, `busy:false`, `postRunBusy:false`,
`trueReady:true`, `recovery.required:false` and a measured backend PID. One POST
per call, never repeated. Read-only probes that time out are repeated at most
three times in all.

`.do` paths may contain Chinese characters, spaces and apostrophes; Stata macro
delimiters, double quotes and control characters are rejected.

## 5. Stop

- **Person:** the **Stop** button in the Stata Terminal.
- **Agent:** only when the person asks, or to abandon the agent's own run:
  `POST http://127.0.0.1:<port>/soft-stop` (macOS: `curl -X POST …`; Windows:
  `Invoke-WebRequest -UseBasicParsing -Method Post -Uri …`). It answers 409 when
  nothing is running. `tools/shared_stata.py` has no stop option.

A soft Stop cancels the current run, drains the task and keeps the **same**
backend, then restores the checkpoint saved just before that run (dataset,
globals, estimates, graphs). Changes made by the stopped run, including its
lines that had already finished, are therefore rolled back. The Terminal shows
e.g. `human-file cancelled by soft Stop (generation 1)`; `/status` reports
`resetGenerationKind: "soft-stop"`. If Stop lands while the run is still saving
its pre-run checkpoint, the code is never sent (`payloadDispatched: false`;
HTTP 409 `PRE_RUN_CANCELLED_BY_STOP`, or 500 `EXEC_REJECTED` if the checkpoint
was still incomplete).

After a Stop:

1. Run `--status`. Continue only when `busy` and `postRunBusy` are false and
   `trueReady` is true. On Windows the restore budget is 30 s + 400 ms per saved
   estimate + 3 s per saved graph, up to 300 s, so Stop of a large session can
   take about 5 minutes. Other platforms keep 250 ms per saved item, capped at
   45 s. Wait; do not reset.
2. If `trueReady` stays false or `/status` reports `continuityLost`, the restore
   was incomplete (`RECOVERED_DEGRADED`, only part of the state came back) and the
   next run is refused with 423. Tell the person; see section 7.
3. The stopped call returns a non-PASS verdict (exit 2), typically after HTTP 500.
   That is expected. Do not resubmit it automatically; submit a corrected next
   stage with a new receipt.

## 6. Receipts, verdicts and exit codes

`shared_stata.py` prints one JSON line (`verdict`, `postCount`, `retryCount`,
`runId`, `requestId`, `responseDiagnostics`, `receipt`, `error`, `failedChecks`,
`windowObservation`). Exit 0 only for `PASS_VISIBLE_SHARED_RUN`; anything else
exits 2.

| Verdict | Was code sent? | What to do |
| --- | --- | --- |
| `PASS_VISIBLE_SHARED_RUN` | Yes, completed | Read outputs; continue. It certifies execution and identity, **not** that anyone watched the source and Terminal |
| `BLOCKED_NO_DISPATCH` | No (`postCount` 0) | Fix the cause in `error` (not ready, busy, identity, window count); then submit once |
| `EXECUTION_UNCONFIRMED_NO_RETRY` | Yes (`postCount` 1) | Do **not** resend. Read `response.json`, `response-diagnostics.json`, `result.json` and the log. A Stata error ends here too: the response carries its own `rc` (e.g. 603) and error text, and code before the error has already run. One exception: HTTP 504 `PRE_RUN_SNAPSHOT_TIMEOUT` with `payloadDispatched: false` in `response.json` means the code was not sent; submit it once more |
| `BLOCKED` | No; the client stopped before the POST (wrong bundle or version, profile lock held, pre-submit wait expired, session needs recovery, receipt directory already exists, rejected `.do` path) | Fix the cause in `error`; then submit once |

Receipt files: `request.json`, `before.json`, `execution-source.json` and
`runtime-execution.do` (with `--file`), `wire-request.json`, `response.json`,
`response-diagnostics.json`, `run.log` (only on PASS), `result.json`. The receipt
contains code and output; never commit `.stata-receipts/`.
`python3 -B scripts/rc745_receipt_check.py <receipt-dir>` re-checks a PASS receipt
offline (`scripts/` is inside this skill directory when installed, at the
repository root in a clone); see [receipts-rc745.md](references/receipts-rc745.md).

## 7. Troubleshooting

| Symptom | What to do |
| --- | --- |
| The first run seems slow | The service is starting (section 3). Wait; do not resubmit |
| HTTP 504 `PRE_RUN_SNAPSHOT_TIMEOUT` on the first run after opening or reloading | Stata took longer than 60 s to start. The code was not sent. Submit it again |
| `BLOCKED_NO_DISPATCH`: not ready or busy | The person or another client is running something. Wait with `--busy-policy wait --max-wait <s>`, or ask. Do not queue another long run |
| `--status` exit 2, window count not 1 | No window, or two windows of the same profile. The person must open exactly one (`--open --workspace <dir>`); never start a second profile to get around it |
| Status bar **Stata: STALE**; runs return HTTP 423 `recovery-required` | A force reset could not confirm the backend. Run the verified recovery **once**: `POST http://127.0.0.1:<port>/recovery-smoke`. It runs a fixed marker command and unlocks only after rc 0 and the marker in the log. Do not kill Stata or delete the session |
| A long script stalls or times out | Reconcile the original request, its receipt, the raw log and outputs first. A timeout is not proof that Stata did not run. See [storage and log recovery](references/storage-and-log-recovery.md) |
| Port already in use | Another editor owns it. Choose a free `stataMcp.visibleBridgePort` and the same `STATA_WORKBENCH_PORT`; never stop the other editor |
| `No module named 'mcp.server.fastmcp'` | The service was installed with MCP 2.x. The default route adds `mcp<2`; a custom service command needs the same constraint |
| `Failed to connect to mcp-stata` with "the network was disabled" | uv is in offline mode (`offline = true` in `~/.config/uv/uv.toml` or `UV_OFFLINE`). Turn it off for the first start, then reload the window |
| Graphs do not appear | Name graphs; several unnamed graphs overwrite the single `Graph` window |
| macOS: error `-1743`, or no windows found | `--doctor`, then `--request-permissions` once, in the same host as the agent (section 9) |
| cmux caller rejected (-67050), `stdout is not a terminal`, onboarding loop | Read [desktop recovery](references/desktop-auth-terminal-recovery.md) before any restart or permission request |

## 8. Known limitations of rc.7.45

- A top-level `exit` inside a multi-line selection (Run Selection, or an agent
  `--code` with several lines) ends the whole selection. The code before it has
  run, but the request is answered as a failure (HTTP 500). `exit` inside a
  do-file or a program is not affected. Prefer `--file` for multi-line work.
- A manual Run Selection that stops at a Stata error can be reported as failed
  without its return code ("execution released without verified completion
  evidence"; FULL45 S41, same on rc.7.44).
- macOS: while the VS Code window is hidden, Terminal text can appear only after
  the run ends.
- Stata's own start-up counts against the 60 s pre-run snapshot budget.
- One backend runs one request at a time. Several instances need separate
  profiles and ports; there is no multi-instance scheduler in this runtime.
- Exact equality of the displayed source and the executed bytes is not
  certified. With `--file`, the receipt keeps the exact bytes that ran.
- `graph use` alone does not create a graph card in the Terminal. The Data
  Browser frame name updates only when the browser opens.
- FULL45 is not complete on the published file; see the runtime README *Known
  limitations*. Windows 10, Windows on ARM and Linux are not verified; macOS
  Intel has CI only.

## 9. Platform notes

Windows:
- Use `python` from the installed Python, not the Store alias. PowerShell 5.1:
  set `$ErrorActionPreference = 'Continue'` before running native tools that
  write to stderr, and judge success by `$LASTEXITCODE`.
- `scripts/invoke_stata_visible_safe.ps1` wraps the same client
  (`-Code` / `-DoFile`). Its old `AllowHttp500Retry`, `BusyPolicy reset` and
  `SmokeAfterReset` modes now fail before dispatch.
- Never accept a UAC prompt or elevate on the person's behalf. On rc.7.45 a lock,
  unlock and a declined UAC prompt left the same backend and extension host running.
- If `code` cannot install a VSIX: `Get-Command code`, `code --version`; fix `PATH`
  to VS Code's `bin\code.cmd`, or use **Extensions: Install from VSIX...**.
- The rc.7.45 Windows test runs used the operator kit's private profile and port
  17497 (runtime `docs/WINDOWS_ACCEPTANCE.md`), not the README default.

macOS:
- The host that runs the agent tools needs System Events **Automation**; ask in
  that same host with `--request-permissions` once, and the person clicks
  **Allow**. Agents started inside cmux may be attributed to cmux. **Accessibility**
  is a separate grant, needed when the system reports it for window inspection.
- `-1743` (`AUTOMATION_DENIED`) does not prove the person clicked Deny.
  `-1744` means request consent once. `PERMISSION_CHECK_TIMEOUT` and
  `WINDOW_QUERY_TIMEOUT` mean "not measured", not denied or zero windows.
  `SCREEN_LOCKED` is not a permission error.
- Do not reset TCC, switch hosts or restart a research session to repair a
  connection. See runtime `docs/MAC_PERMISSIONS.md`.

## 10. Working rules

- **Visible by default.** The executable `.do` and the Stata Terminal are on
  screen. If the person allows covering, hiding or minimizing the window, keep
  running through the same session and record physical visibility separately.
  Losing visibility is not permission to steal focus or rerun work.
- **Preserve the person's edits.** Never save or discard their unsaved buffer.
  If they edit a file, wait for the saved version, compare it with the last
  executed version, recheck memory and dependencies, then run a new version.
- **Pause and stop.** "Pause" stops later stages at once. "Stop" means section 5;
  never kill or reset Stata for it.
- **Unknown outcome means no resend.** `EXECUTION_UNCONFIRMED_NO_RETRY` does not
  mean "did not run". Resolve it from the receipt and the log first.
- **Do not destroy shared state.** Never `clear all`, `log close _all` or
  overwrite existing results to make replay work. Record the active frame, cwd and
  data signature; use task-specific frames and saved checkpoint inputs.
- **Respect storage limits** the person states; see
  [storage and log recovery](references/storage-and-log-recovery.md).
- **Report four claims separately:** execution (runId/requestId, backend, rc,
  raw log), visibility (what was actually on screen), replay (two runs, compared
  outputs) and task completion (every agreed deliverable).

## 11. Do not

- Start another Stata, backend or VS Code profile to get around a busy, STALE or
  missing session.
- Resend a POST whose outcome is unknown, or call `/force-reset` or
  `/panic-kill` without the person's explicit request.
- Kill Stata, delete the session, or remove lock files that a process holds.
- Commit `.stata-receipts/`, research data, logs or credentials.
- Treat `PASS_VISIBLE_SHARED_RUN`, HTTP 200 or a file existing as proof that a
  person watched the run or that the statistics are right.

## 12. References

| Read when | File |
| --- | --- |
| Writing staged tasks and checking results | [workflow.md](references/workflow.md) |
| Re-checking a receipt offline | [receipts-rc745.md](references/receipts-rc745.md) |
| Editing an author's `.do`, delivering saved data | [shared-session-delivery-lessons.md](references/shared-session-delivery-lessons.md) |
| Hiding the window, several instances, UI coordination | [execution-policy-and-concurrency.md](references/execution-policy-and-concurrency.md) |
| Disk budgets, backups, SMCL markers, long-run stalls | [storage-and-log-recovery.md](references/storage-and-log-recovery.md) |
| Graph or export timeouts, tables, DOCX/RTF | [native-export-and-real-file-delivery.md](references/native-export-and-real-file-delivery.md) |
| Rerunnable delivery, CSV/R/Stata crossings | [replay-and-data.md](references/replay-and-data.md) |
| Manuscript data/result chain, NLM discrepancies | [empirical-lineage.md](references/empirical-lineage.md) |
| Checking which runtime is installed | [runtime-routing.md](references/runtime-routing.md) |
| Changing Windows/Mac adapters or packaging | [cross-platform-acceptance.md](references/cross-platform-acceptance.md) |
| cmux/desktop permission and terminal recovery | [desktop-auth-terminal-recovery.md](references/desktop-auth-terminal-recovery.md) |
