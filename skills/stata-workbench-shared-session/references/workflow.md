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
