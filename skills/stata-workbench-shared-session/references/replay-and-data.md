# Replayable research handoff

Deliver a master entry and individually runnable stage entries with declared
checkpoint inputs. Stage programs may preserve generated task frames for the
user, but must restore the original active frame and cwd and verify the original
data signature. Close only their own named log/post handles. Capture failures to
retain evidence, then return the original nonzero Stata rc (never swallow it).
Use new directories, not `replace`, for new results. Preserve historical code and
failed receipts; label stateful old programs as non-replayable history.

Write author-readable `MOD-*` comments: original file/anchor, old/new formula,
reason/source, affected fields, validation and inherited limitations. File-tool
edits are genuine coding but not simulated human typing. Code echoed after an
error in `capture noisily` is not evidence every command executed.

Data boundaries demonstrated by the V751 incident:

- Technical IDs are not questionnaire missing codes. Preserve valid ID 9999.
- Decide the merge domain before asserting: matching all master intervals does
  not require using-only upstream rows to belong to that interval sample.
- Explicitly recast centered integer variables to double; `import asdouble`
  does not guarantee later replacements retain double precision.
- Parse logical references to explicit 0/1/missing with unknown values rejected.
- Do not relax tolerances to hide conversion errors.
- Separate observed events, eligibility and target variables, and distinguish
  absence from a measured false result.
- Stop dependencies after failure; opening a fixed log again or depending on a
  frame left by a previous stage is not an independently replayable entry.

Test each delivered saved entry twice, record the actual client vs human command
route, and compare substantive data outputs (DTA file timestamps may differ).
Model estimates must not be refit merely to demonstrate visibility unless the
task actually requires the refit. Explain unfinished non-Stata deliverables.
