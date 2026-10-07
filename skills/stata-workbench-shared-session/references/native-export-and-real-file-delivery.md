# Native export failures and real-file delivery

Treat controller exit, transport cancellation, native Stata termination and
shared-state restoration as separate facts. A timeout may cancel the request
while embedded Stata still holds a log or output open. Inspect the bound worker,
its open files, log progression and a bounded native sample when available.
Do not set readiness flags, replace the backend or replay the request to bypass
an unresolved native operation.

One macOS PNG-export sample showed bitmap conversion waiting in Java/AWT AppKit
initialization. This is evidence of that process's wait, not proof of a universal
cause or a successful fix. A bridge cleanup candidate and its offline tests do
not establish native recovery. Keep supported recovery, installation and actual
state restoration separately evidenced; do not repeatedly send breaks or reset
shared memory merely because the transport has settled.

## Check nested DO coverage before calling a raster export safe

Record the actual wire command, cwd and referenced execution files, not just
the user-facing DO. A saved shared-state wrapper can call another export DO.
One installed version prepared only the first reference: its failed request
reported zero Darwin conversions although the nested export file contained
raster commands. An offline replay reproduced the gap; the recursive candidate
reached the inner exports. These findings support an adapter defect in that
request, not a diagnosis that every VS Code graph failure has the same cause.

The runtime candidate follows literal double-quoted, line-start `.do` calls,
with common capture/quietly/noisily prefixes, into temporary execution copies.
It preserves author sources, excludes comments/quoted examples, and rejects
missing files, cycles, ambiguous relative cwd, and bounded size/depth/count
overruns. It is not a full Stata parser. Macro paths, `run`, `include`, semicolon
delimiters and other dynamic command forms are not full coverage; inspect the
actual export file and record `partial-static` rather than claiming protection.
Files generated during execution need a later separately prepared stage.

Keep the same-request `sourceCompatibility` / `darwinCompatibility`, original
and temporary hashes, wire, output files and native result together. An empty
replacement list does not prove a nested program has no raster export. A
failed descendant transformation must stop submission, even under `capture do`.
Do not test a suspected native PNG hang again in the research backend. A scoped
SVG/converter output must be checked as an image; it does not establish native
PNG pixel identity or remove every possible operating-system graphics failure.

When the client returns `_httperror`, preserve its original bytes and extract
runId/requestId/rc/logPath as diagnostics only. Do not merge conflicting IDs,
promote an HTTP failure to success, or treat absent IDs as zero submission.
Check original native termination before continuing. Updating the repository,
installing the package, loading it, and validating real output are distinct
steps: a PR or offline PASS does not mean the active extension is repaired.

A real saved-GPH recovery through the existing Workbench produced a decoded,
nonblank 1200 × 800 RGB PNG with Stata rc=0, using frozen SVG/converter execution
copies and no data/model recalculation. The earlier isolated attempt failed at
SVG export with `could not find Graph window`, r(693), after `graph use ..., nodraw`.
The corrected copy loaded/drew the private graph without `nodraw`. Inspect the
actual log: r(693) is not by itself proof of insufficient disk space. Keep the
failed attempt and do not repeat it as an unknown retry.

The prepared-copy route is distinct from installing or loading the candidate
extension; that installation was not part of this live check. One decoded PNG
does not certify all missing graphs or the full nested data chain. Stata graph
drawing is also distinct from OS window focus: honor explicit permission to
cover/hide the Workbench, while retaining instance and terminal-state checks.

## Separate data delivery from graph conversion

- Save DTA checkpoints before graph export. Give precision CSV exports their own
  saved DO, isolated output root, input hashes and terminal receipt.
- After a failed graph stage, reuse audited saved data for missing exports once
  the original session is genuinely available. Preserve the failed attempt and
  do not recompute the successful data block just to obtain CSVs.
- Keep literal string IDs, variable order, stored values and missing-value codes.
  Document any display-format change, such as `%24.17g`. Compare the entire CSV
  against the saved DTA. Retain DTA metadata and the author's rounded CSV too.
- Preserve the author's style and names. Explain narrow changes with `***`, `//`
  or block comments. Put session protection in an identified wrapper, keeping
  the original data logic readable. Do not execute a review-only annotated copy.
- Record prepared, submitted, completed, compared and scientifically accepted
  statuses separately. Stage counts and source-line spans do not prove complete
  source or branch coverage.

## Make the chapter folder usable without reading machine manifests

Deliver actual input/output DTA, CSV and DO files, with a short chapter README
linking each file, the execution order, original/revised roles and unresolved
differences. Use a labelled cross-chapter folder where attribution is unknown.
Manifests are supporting evidence and cannot substitute for data files.

For remote large files, provide a usable verified retrieval location after
upload, ordinary roundtrip SHA and full member-content verification. A local
archive or proposed cloud directory is not a download link. Distinguish byte
equality, common-value equality, metadata differences and historical R adoption;
none is interchangeable with the others or with scientific acceptance.

Before writes, preserve the user's disk reserve plus estimated peak temporary,
download and extraction space. A snapshot of a file still open by a failed
worker is failure evidence, not a completed output eligible for cleanup. Keep
originals, frozen results and failure receipts. Continue independent offline
work while the native operation remains unresolved.

## Finish only the missing outputs and verify the shared state

After the one-image recovery, a single existing-Workbench request produced the
remaining 23 PNG/GPH pairs from the already audited saved DTA. All 24 PNGs
decoded and were nonblank; a contact sheet was visually checked. Native return
was 0 and the wrapper's original-data signature, frame, graph inventory and
current-graph restoration assertions passed. The same backend was ready after
completion. No successful cleaning, score calculation or model was repeated.

Bind the saved input to its earlier audit hash, not merely its current file
name. Reuse already accepted outputs instead of regenerating them. Use private
graph names and a separate session-protection wrapper; retain readable author
plotting commands and explain stale titles in comments. The author's title
"Comparison of Three Graphs" was retained even though its command combined two
panels. Plot production and scientific interpretation are separate checks.

Record all image dimensions, hashes and decode results, plus native terminal
and restoration evidence. Contact-sheet inspection is not a proof of native
PNG pixel identity or of every unseen graphics object. This recovery did not
install/reload the candidate extension or certify the full research chain.

These lessons add guidance only. They do not install a runtime, recover a session,
certify all hidden-window states or establish multi-instance Stata concurrency.

## Preserve existing Mata state before table commands

A shared session may already contain Mata objects created by the Workbench's
own checkpoint code. A precondition that Mata must be empty can reject a table
stage before any author command executes. In one recorded incident, four
`__codex_*` objects were present; this did not establish a frozen VS Code window
or a failure of `asdoc`. Keep the failed request and its skipped checks. A later
diagnostic cannot retroactively certify restoration steps the failed wrapper
did not run.

Inventory existing names and protect supported Mata values, matrices, scalars,
macros and open handles in a separate execution wrapper. Do not clear shared
Mata or close unknown handles to satisfy a guard. The bounded successor saved
and restored the existing ordinary objects and verified seven return markers.
This is evidence for that inventory and wrapper, not a universal serializer for
pointers, external resources or every possible Mata type.

Stata's extended macro-list `==` comparison is order-sensitive; `===` checks
membership irrespective of order. For an unordered name inventory use `===`,
then separately verify each saved value and whether the name originally
existed. A set comparison alone does not protect macro content. Match a
versioned verifier to the exact restoration markers; preserve the execution
receipt and add an offline verifier when marker names change, rather than
repeating successful Stata work just to satisfy an old regex.

## Separate RTF text encoding from table numbers and page layout

One actual `asdoc` output declared ANSI while containing raw UTF-8 Chinese
labels. Four original RTF files and their precision CSVs were retained. The
successor display copies converted only non-ASCII text to standard RTF Unicode
escapes; inverse text recovery was exact and all 124 table numbers were
independently checked against the saved DTA. Native text readback confirmed
readable Chinese. No new calculation was needed.

Inspect the actual bytes and declarations before choosing a conversion; do not
blindly re-encode arbitrary RTF or change its control syntax. Keep the native
file separate from the labelled display copy and pin both hashes. Successful
text parsing is not Word page-rendering acceptance, and rounded RTF figures
must use their printed precision while the CSV is checked at full precision.

## Keep preserve/restore boundaries and historical numbers explicit

A final `save` after `restore` saves the restored dataset, not the temporary
dataset used inside `preserve`. Audit the full boundary. If the temporary sample
is useful for checking a table, save it as an explicitly new isolated checkpoint
before restoration; do not pretend it was an original author output or merge
its variables into the final panel. Keep new logging/export commands annotated.

In the bounded follow-up, two saved DTA/CSV pairs contained 2,293,608 cells that
matched independent reconstruction, and 146 returned scalars from seven
t-tests and four contingency tables matched independent calculations. Four
statistics differed from comments in the historical DO; those old numbers
were retained and reported beside the new results. Matching a test calculation
does not validate its independence assumptions for repeated panel observations
or establish that historical R scripts adopted the regenerated data.

DTA sort-list entries terminate at the first zero. Compare only active sort
indices, not reserved trailing storage. Retain a failed offline checker and
document its correction; do not rerun statistical work because an audit reader
mistook unused bytes for active metadata.

These additions describe observed execution and bounded checks. They do not
install/reload the extension, certify every export path or guarantee that
future operating-system graphics failures cannot occur.

## Preserve column order, coding direction and stored precision

`keep` selects variables without necessarily reordering them. If a supplemental
DTA must match an author's CSV column list, use a separately annotated `order`
after `keep`; verify the ordered names as well as all values. A recode before
`preserve` remains in force after `restore`. Trace the actual sequence before
assuming a later graph or export still uses the original categories.

In one bounded comparison, the current source collapsed seven frequency
categories to five before a positive linear transformation. Historical exports
instead matched a seven-category reverse transformation after float32 storage.
That finding identifies a reproducible value relationship, not the unknown
historical executed program. Retain the author track and report the difference;
do not silently change it to force equality with a same-named historical file.

Report CSV text equality, full stored-value equality and float32 roundtrip
separately. A default CSV can look close yet fail roundtrip for a few cells;
a precision CSV checked against every saved DTA cell resolves export loss,
not a category/direction mismatch. Same-name DTA files can have different row
counts, columns and versions. Compare common keys and unmatched rows, including
literal string IDs; actual differences between two string IDs are not merely a
numeric display-format issue. Do not expose individual identifiers in public
experience reports.

Rank ties can leave a percentile-defined low group empty. Preserve the author's
missing result and report it instead of splitting ties to manufacture a group.
Reconstruct calculations using the actual float/double storage at each step:
rounding a transformed score can create ties that unrounded arithmetic lacks.
Execution agreement does not validate a claimed scientific property of a score.

## Larger graph batches remain bounded output checks

A later single request read an already audited checkpoint and produced 84 PNG
and 84 native GPH files, expanding four author plotting statements across 21
variables and performing seven display commands. Frozen SVG/converter copies
provided raster export; no data cleaning, scoring or model was repeated. All
PNG files decoded and all seven contact sheets were visually inspected. Eight
recorded restoration checks passed and the same backend was ready afterward.

Keep graph filenames and author titles; use private in-memory graph names.
Record expanded-command coverage, original and prepared source hashes, native
terminal evidence and the exact scope of restoration. Native GPH headers plus
successful saves do not establish separate reload acceptance. Contact sheets
do not establish every-pixel or historical/native-PNG identity. This larger
batch demonstrates that recovery route only; it neither installs the candidate
extension nor permanently fixes native Java/AWT initialization or certifies
multiple simultaneous Stata backends.


## Preserve installed repairs when preparing a new candidate

Before installation, compare the actual installed bundle and runtime modules
with the candidate, not just version numbers or a green pull-request check.
In this release review, the recursive-export candidate initially omitted the
installed finalizer, bounded Terminal history, source-column/graph routing and
log-tail yielding repairs. Installing it would have reverted those changes.

The maintenance replay now includes all four installed patch modules and the
finalizer return-code parser. Their behavioral regressions run in the release
check, while the candidate retains recursive DO preparation and its isolated
package dependency tests. The rebuilt bundle matches the installed bundle; the
new export behavior resides in the separately pinned compatibility modules.
Verify both bundle and module hashes inside the final VSIX. These offline
checks do not prove that an existing VS Code host has loaded the candidate or
that its actual graph/table output passes live acceptance.
