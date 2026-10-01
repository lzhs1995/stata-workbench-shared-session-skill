---
name: stata-workbench-shared-session
description: Run annotated Stata do-files in the user's existing shared Workbench session with automatic stage progression, preserved memory and checked receipts. Show source and Stata Terminal by default; honor explicit permission to cover or hide the window. Use for human/AI shared Stata coding, replayable handoff and correctly scoped instance coordination, not statistical model selection.
---

# Stata visible shared-session workbench

This operating skill is versioned separately from the runtime. Read the installed
runtime's current guide and this repository's `runtime-compatibility.json` first.
Read [runtime routing](references/runtime-routing.md) before adopting a candidate
protocol or upgrading; a PENDING pair does not replace a working backend.
Use the named existing instance, never a new Stata/backend/profile to evade a failure.
For deliberately requested multiple instances, read [execution policy and concurrency](references/execution-policy-and-concurrency.md);
each instance needs its own supported identity binding, state, outputs and queue.
Do not infer macOS paths from Windows examples or vice versa.

## Default: automatic, visible, interruptible

When asked to use this workbench, write/edit commented `.do` programs, show them,
execute and verify stages automatically. **Do not require per-stage user approval.**
Announce purpose and code changes briefly; the user may watch without replying.

Under the default visible policy, the executable version must be visible in the left editor group and the actual
Stata Terminal webview in a separate right group at the same time. Same-group
tabs, a saved log, another VS Code profile, or a later screenshot are not proof.
Use a co-working prepare/dispatch ticket only with its verified matching runtime.
For a legacy formal runtime, use its documented saved-file route and record
transport and actual visibility separately. Do not fabricate candidate tickets
or a layout receipt from window count or HTTP status.
The displayed execution snapshot and run manifest must have identical hashes.
Keep editable source distinct from the frozen version actually executing.
The candidate prepares any compatibility conversion before displaying code;
the receipt archives that exact version as `runtime-execution.do`. Verify the
author-input identity, displayed execution identity, working directory and wire
command independently. Preparing the layout alone never means code executed.
Also inspect runtime compatibility-copy evidence: an input hash does not certify
the bytes of a rewritten temporary `.do`. `EXECUTED_SOURCE_IDENTITY_NOT_CERTIFIED`
must stop dependent stages. Record both versions; do not rename that verdict PASS.

If the user asks to pause, pause later stages immediately. If they ask to stop
the active calculation, request the product's current-request cancellation and
then verify settlement; do not kill/reset Stata. If they edit a file, preserve
the change, wait for a saved version, compare it with the last executed version,
recheck memory and dependencies, then create a new execution version. Never
silently save/discard their dirty buffer. Human and AI submissions are serial.

Losing visibility is recorded evidence, not permission to steal focus or rerun
work. Let the current request settle unless canceled. If the user permits window
occlusion, hiding or minimization, continue non-UI stages through the same bound
Workbench using a matching client; do not add a visibility-only pause. Record
physical visibility separately and preserve old failures. Under a strict visible
policy, reconcile the layout before later stages. Opening source afterward is
review, not retroactive live verification. Hidden is not unresponsive or closed.

## Execute and verify

Read [workflow.md](references/workflow.md) for the exact task/receipt contract.

Read [storage and log recovery](references/storage-and-log-recovery.md) for disk budgets, verified backup and SMCL marker reconciliation.
Honor the user's free-space reserve before large writes: back up completed large files to the dedicated task folder before the projected peak crosses it, keeping higher stage budgets and verified-reclamation requirements.
Read [replay-and-data.md](references/replay-and-data.md) when delivering research
programs that the user must rerun or when crossing CSV/R/Stata representations.
Read [empirical-lineage.md](references/empirical-lineage.md) when verifying a
submission manuscript's full data/result chain or responding to NLM discrepancies.

1. Bind the exact profile, bridge owner and Stata PIDs; distinguish permission,
   window visibility, execution readiness and co-working protocol readiness.
2. Record original active frame, cwd and data signature; use unique task frames
   and saved checkpoint inputs. Never `clear all`, `log close _all`, or overwrite
   existing results just to make replay work.
3. Prepare a task manifest: stage IDs, program, code dependencies, checkpoint
   inputs, unique outputs, assertions. Use the matching client's `--task` or
   `--file`. `--code` must be materialized as a readable do-file by the client.
4. Read each result and actual outputs before progressing. Confirmed Stata errors
   require a corrected version and inspection of partial effects. Unknown outcome
   means **no resend** until it is resolved; it does not mean no execution.
5. For handoff, verify the promised replay entries and reuse already validated
   runs. Where two executions or Run Current File are required, compare outputs
   and preserved original state; do not repeat research just to fill a new checker.
   Do not certify an entire pipeline from one component's success.

## Report four separate claims

- Execution: bound runId/requestId/backend, actual return code and raw log.
- Visibility: concurrently observed source/Terminal, including any interruption.
  Record the user-authorized policy; permitted hiding never means observed visible.
- Replay: entry/dependency version, two separate runs and compared outputs.
- Task completion: all agreed deliverables, not only code or model output.

`PASS_VISIBLE_SHARED_RUN` from older clients proves transport, **not** live user
visibility. `OBSERVED_VISIBLE` means software observed a layout, not that a human
read or understood it. Skill validation is not product live acceptance.

Do not claim permanent OS permission. Preserve -1743/-1744 and host identity;
`SCREEN_LOCKED` is not a permission error or proof of zero Workbench windows.
Do not disable locking or bypass authentication to continue visible execution.
do not reset TCC, switch hosts, or restart an active research session as an
automatic connection repair. See the runtime's maintained permission guide.

Candidate status: the proposed runtime pair is not yet live-certified. The skill
and offline checks may be installed separately; do not deploy or certify the
candidate runtime from these tests. Keep existing fixed runtime paths.
