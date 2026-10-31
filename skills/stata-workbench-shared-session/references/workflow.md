# Staged workflow with the rc.7.45 client

Read [storage and log recovery](storage-and-log-recovery.md) for disk budgets,
verified backup and SMCL marker reconciliation, and
[execution policy and concurrency](execution-policy-and-concurrency.md) for
user-permitted hiding and resource coordination.

Use the person's real profile, port and a runtime checkout at the installed tag.
No tool invocation may create a replacement backend as a fallback.

## One stage = one saved do-file = one call

The rc.7.45 client has no task manifest, pause, cancel or resume option. Run a
multi-stage analysis as a sequence of saved do-files, one call each:

```sh
python3 -B tools/shared_stata.py --file /abs/stage01_clean.do --cwd /abs/project --receipt-dir /abs/receipts/stage01
python3 -B scripts/rc745_receipt_check.py /abs/receipts/stage01
python3 -B tools/shared_stata.py --file /abs/stage02_models.do --cwd /abs/project --receipt-dir /abs/receipts/stage02
```

(Run the receipt check from this skill's installed `scripts/` directory.)

Before each stage:
1. Its inputs exist and were produced by an accepted earlier stage.
2. Its outputs do not exist yet (new names per run), so a file existing after
   PASS is evidence of this run.
3. The program contains its own assertions (`assert`, `confirm`, keyed counts,
   missingness, membership); a file existing or hashing is not a statistical check.

After each stage:
1. Exit 0 and verdict `PASS_VISIBLE_SHARED_RUN`, then the receipt re-check passes.
2. Read the outputs and the log before starting the next stage.
3. Exit 2: stop the sequence. `BLOCKED*` sent nothing. `EXECUTION_UNCONFIRMED_NO_RETRY`
   may have run partly: inspect partial effects, write a corrected, versioned
   stage, and submit that once. Never resubmit the same call automatically.

Pause between stages simply means not starting the next call. Stop during a
stage is SKILL.md section 5. A resumed sequence starts at the first stage
without an accepted receipt and uses new receipt directories and new outputs.

## Classify a failure from the receipt

A Stata error has its own `rc` and error text in `response.json`; arbitrary
text such as `r(9)` in output is not enough. Classification needs the response,
the run/request identity (`runId`, `requestId`), the same backend PID before and
after, and the raw log. The response's `runId` and `requestId` are different
identifiers; never interchange them.

## Historical candidate client (not rc.7.45)

Earlier candidate clients documented a `stata-cowork-task/1` manifest with
`--task`, `--control` and `--resume-from`. These options do not exist in
rc.7.45 `tools/shared_stata.py`. Receipts from that client are checked with
`scripts/completion_check.py`; rc.7.45 receipts with `scripts/rc745_receipt_check.py`.

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
