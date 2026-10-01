# Execution policy, hiding and concurrent work

## Follow the user's policy with the existing runtime

Explicit shared execution means an identifiable saved program runs through the
user's bound Workbench/backend with accessible code, request, log and outputs.
It is distinct from physical screen visibility. Default to source and Terminal
side by side. A user may permit occlusion, hiding or minimization; preserve that
authorization across stages and continue non-UI work when the matched client
can verify identity, readiness and request settlement without focus operations.

Do not create an invisible replacement Stata process. Do not invent an
`--allow-hidden` flag or bypass a client's identity/readiness checks. Old clients
may still gate on window observations; a documented, reviewed matching adapter
is needed. Guidance alone does not change installed behavior.

Record execution policy and actual visibility separately. Never turn previous
visibility failures into PASS after new permission. A later screenshot cannot
prove earlier visibility, and observed visibility cannot prove a human watched.
Renderer unresponsiveness, closed applications, changed identity and uncertain
execution are different from occlusion. Inspect them rather than assuming they
are harmless hiding. Never bypass system locking; GUI actions wait for normal
unlock while independent offline work may continue.

## Coordinate the right resource

| Resource | Coordination |
|---|---|
| One Stata backend shared by people/agents | Serial submission; protect frames, cwd, globals, estimates and graphs |
| Computation plus offline verification | May overlap using frozen inputs and separate output roots |
| Distinct Workbench/Stata instances | Each has a supported profile/user-data, launcher/host/backend/port binding, own state, execution lock and outputs |
| Shared desktop focus, keys or clipboard | Existing UI queue and short lock, with the workspace's idle-input policy |

Two windows or two ports do not prove two independent backends. Before claiming
multiple-instance concurrent execution, verify isolation and actual overlapping
requests using nonresearch fixtures, including that cancel/recovery in one does
not affect the other. Check licensing and resource capacity. If not tested, call
this an isolation specification, not live acceptance.

The current public fixed-instance client and task-specific pinned clients are
not generic multi-instance schedulers. Do not remove duplicate-instance guards,
rename shared locks or edit a pinned client to force concurrency. An explicitly
requested second instance is distinct from creating one to evade a failure.

UI lock release does not mean a runner ended or a broker ticket was returned.
Use the existing coordinator/queue; no duplicate queue or unsolicited agent
message. An 8-second HID idle interval used in one workspace is a local agreement,
not a universal plugin requirement. Non-UI calculation need not hold focus.

## Settle and resume without duplicate work

Bind the execution version SHA, actual request/run IDs, instance identity,
declared inputs, new outputs and terminal evidence. HTTP success, parent exit,
backend rc, assertion result and model status are separate observations.

If the controller ends while a verifier continues, keep the original wait exit
unknown unless recorded. Revalidate the saved diagnostic and its hashes, inspect
original process identity, then record a supplemental reconciliation. Do not
invent the missing PROCESS receipt or rerun a completed model. A resume plan
must list the completed prefix it reuses and the first unsubmitted stage.

Stop future dispatch when the user changes scope, keeping current work's real
terminal evidence. Preserve originals, frozen outputs and failed attempts;
inspect partial effects before a versioned repair. Continue independent local
work during a stage-specific blocker.

## Durable research delivery

Retain author naming and coding style. Explain issues and supported corrections
using Stata comments, linking the original logic, manual/source evidence and
implemented change. Keep unresolved scientific questions explicit; don't force
an unsupported recode or expand into downstream modeling/manuscript changes.

Separate executable staged DO files from review-only commented copies. A source
span declaration does not prove every loop branch executed. Conditional output
contracts distinguish successful models, expected failures, aliases and stages
never submitted. Failed estimates must not inherit a previous model's `e()`.
Repeated omitted-term names and independent `V_modelbased` axes can be valid;
check complete coordinates and values rather than rejecting by name alone.

## Evidence scope of this update

The underlying local research experience used a pinned
`0.1.3-rc.7.43-dev.1` instance and a task-specific occlusion-permitted adapter,
with single-POST receipts and separately reported physical visibility. It does
not certify public `rc.7.39`, the PENDING `visible-cowork/1` pair, all hidden/
minimized states or two simultaneous Stata instances. This update adds operating
guidance only; retain runtime/client pins and version source, local installation,
loaded extension and live research acceptance separately.
