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

These lessons add guidance only. They do not install a runtime, recover a session,
certify all hidden-window states or establish multi-instance Stata concurrency.
