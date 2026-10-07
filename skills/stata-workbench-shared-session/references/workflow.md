# Executable workflow contract

Read [storage and log recovery](storage-and-log-recovery.md) for disk budgets, verified backup and SMCL marker reconciliation.

Read [execution policy and concurrency](execution-policy-and-concurrency.md) for
user-permitted hiding and resource coordination. The commands below require the
matching candidate client; they are not new flags for a legacy fixed client.

Use the explicit product tools directory from local installation configuration,
not a guessed port/profile. Mac defaults on a fresh public install differ from
an existing formal rc70 profile. No tool invocation may create a replacement
backend as a fallback.

The matching `tools/shared_stata.py` accepts:

```sh
python3 -B /absolute/product/tools/shared_stata.py --file /absolute/analysis.do --receipt-dir /absolute/new-receipt
python3 -B /absolute/product/tools/shared_stata.py --task /absolute/task.json --receipt-dir /absolute/new-task-run
python3 -B /absolute/product/tools/shared_stata.py --control pause
python3 -B /absolute/product/tools/shared_stata.py --control cancel
python3 -B /absolute/product/tools/shared_stata.py --control resume
```

`pause` prevents new stages; `cancel` also calls product cancellation. `resume`
does not resubmit an earlier request or approve stale tickets. A fresh task
invocation must be scoped to unexecuted/corrected stages and use fresh outputs.
One execution POST per stage; preparation/finish/control are separate non-Stata
operations and must not be falsely counted as research executions.

Task schema `stata-cowork-task/1`: `taskId`, ordered `stages`. Each stage has `id`,
`program`, `cwd`, `inputs`, `outputs`, `dependencies` (code), `requires` (earlier
stage IDs), optional `label`. Relative paths resolve against manifest directory.
Declare all code includes; dynamic includes require review and explicit closure.
The current client freezes code beneath the main source's directory and checks
source/snapshot hashes. This does not automatically rewrite arbitrary do-file
include paths or freeze undeclared external data. Author stages accordingly.

New outputs must be absent. An output existing after PASS is hashed, but file
existence/hash is not a statistical assertion: include keyed counts, missingness,
membership and method-specific checks in the Stata program. Failure stops later
stages. Existing failed outputs remain evidence, not inputs for the next stage.

Each stage receipt separately reports execution, visibility, replay and task
completion. `run.log` is retained even for readable failure responses. Failure
classification needs response lifecycle + actual run/request identity + same
backend + executed start marker + raw error; arbitrary text `r(9)` is insufficient.
The legacy response can put the request ID in its top-level `runId`; take the
actual run ID from correlated lifecycle/state, never interchange them.

Client snapshots are versioned execution inputs; manual changes should target
the named editable source. Repeated execution must use explicit saved input
checkpoints and unique outputs, not whatever happens to be in the active frame.
# Resume boundary

After a pause **between completed stages**, use a fresh receipt directory and
`--task task.json --resume-from /absolute/prior-receipt-directory`. The completed
prefix is reused only after code/input/output/receipt hashes match. It is not
executed again. An incomplete or unknown stage cannot be retried by this option;
inspect its partial effects and version the repair explicitly.

## Verify exact variable names and abbreviation state separately

A historical command may use a unique prefix rather than the full released DTA
field name. For example, `qq9010` may resolve to `qq9010n` when `varabbrev` is on.
A metadata reader finding no exact `qq9010` field is not sufficient evidence of
Stata `r(111)`. Check the complete candidate set, case and ambiguity, and record
the actual session setting before execution. Record no-match, ambiguous prefix
and unique-prefix cases separately. A unique match in one release does not bind
another release or prove the command has executed.

Preserve the author source. If a runnable successor uses the verified full name,
explain that limited binding in a Stata comment and retain the input metadata
and version evidence. Do not globally enable abbreviations or rewrite unrelated
identifiers to make a stage pass. Keep review-only annotated files separate from
executable stages; matching text inside a nested block comment is not an active
command or evidence of dynamic coverage.

## State-preserving diagnostics and restoration pilots

Persist the exact entry RNG state, sorting RNG state, working directory and
relevant object inventory before a diagnostic can change them. A diagnostic
that verifies payload equality can still fail its preservation contract. Check
both contracts, including cleanup, on success and captured error paths.

Distinguish serialization/readback, actual loading under temporary names,
restoration of selected entry values, and restoration of the entire session.
A successful Mata temporary-load pilot does not prove preservation of all
programs, results, settings, frames or open handles, and does not authorize a
plugin reload. Record precisely which objects and settings were checked.

If preservation fails, retain that run as failed and inspect its partial
effects. Prepare a versioned successor rather than replaying the request.
Never substitute an older backup for an unrecorded exact entry RNG state or
claim that the successor repairs the earlier lost state. In particular,
sorting RNG state must be checked separately from the ordinary RNG state.
