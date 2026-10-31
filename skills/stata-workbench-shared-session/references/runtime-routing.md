# Which runtime is installed, and which client to use

Skill and runtime are versioned separately. This skill describes runtime
`v0.1.3-rc.7.45`; its pins are in `runtime-compatibility.json` at the skill
repository root.

## Check before the first run

1. Installed VSIX version: the tools at tag `v0.1.3-rc.7.45` hash the installed
   bundle before connecting. `--status` then prints `BLOCKED` with
   `candidate identity mismatch` or `installed version mismatch`; `--doctor`
   reports `NEEDS_ATTENTION` with the same text in its `instance` check. Either
   means the installed extension is not rc.7.45.
2. If the person runs another version, use a runtime checkout at **that**
   version's tag and that version's README. Do not mix tools and extension
   versions, and do not upgrade the person's extension to make labels match.
3. rc.7.45 has no co-working ticket protocol. The bundle contains no
   `visible-cowork` route. Use the saved-file route (`--file`) and record
   transport (receipt) and observed visibility separately.

Record separately: skill version, runtime source revision, installed VSIX,
loaded extension (from `--status`) and backend. Do not reset permissions,
create another profile, replace the backend or rerun research only to make
version labels equal.

## Portable evidence lessons

An annotated do-file, visible execution, durable output and replayable delivery
are separate artifacts. Test each promised replay entry with declared inputs,
new frames/logs and actual outputs, preserving human changes and memory. Counts
cannot replace complete sample/result keys. An unconfirmed transport is not a
Stata error and does not grant an automatic resend.

A relocated symlink can be readable while canonical-root checks or ancestor
dependencies fail. Preserve required roots or declare a new entry and mapping;
do not edit a historical gate to claim portability. Hashes certify bytes, not
program execution.

Portable checker 1.1 (`scripts/empirical_trace.py`) accepts compound `row_keys`,
exact key-array `expected_rows`, optional `expected_n` and `expected_cell_rows`.
Use current model/term/group/wave identities, not a past chapter's fixed row
count. It consumes saved CSVs and does not perform study coding. Precision,
display and tolerance stay separate.
