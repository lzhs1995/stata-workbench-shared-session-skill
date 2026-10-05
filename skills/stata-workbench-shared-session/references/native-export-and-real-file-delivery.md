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
