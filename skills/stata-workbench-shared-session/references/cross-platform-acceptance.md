# Windows/Mac acceptance and development lessons

Use this when developing or validating the shared-session runtime. Read the
installed runtime guide and its exact identity manifest first. This document is
operating guidance; installing it does not install a candidate runtime or adopt
its protocol. Keep the compatibility record's pending pairing unchanged until
that specific protocol has its own acceptance.

## Keep common execution rules and native adapters separate

Use one receipt verifier and one single-dispatch client. Platform adapters own
process/window observation, executable selection and file locks. Windows needs
CIM/TCP process ownership, exact parsed argv/profile matching, process creation
times and stable byte-range locks; Mac uses its supported process and permission
observers. An arbitrary listener, substring match or top-level window count is
not the expected Workbench, Stata backend or source/Terminal layout.

Invoke the Windows Code executable with an argument array. A shell shim adds
another quoting layer for spaces, Unicode and apostrophes. Keep Python tool
selection explicit; never substitute a Microsoft Store alias for the configured
interpreter. The Stata service may use a separate, pinned private environment.
Do not infer Windows paths from a tested Mac profile or vice versa.

PowerShell wrappers should delegate to the same execution contract. Retired
automatic HTTP-500 retry or reset options must fail before dispatch. Waiting
before a first submission is different from repeating a possibly executed one.
Use a non-starting doctor to report missing configuration, installation, native
permissions and identity without creating another instance.

Actual Windows checks exposed a DOCX failure hidden by POSIX semantics: close
the original ZIP before `os.replace`. Test real OS behavior as well as adapters.
Keep binary fixture bytes, LF/CRLF streams, filename validation, Windows error
messages, native VSCE entry invocation and PowerShell 5.1/7 behavior explicit.

## Identify what each check proves

Track source revision, built/packaged files, installed files, loaded extension
host, selected service configuration/runtime, licensed execution and observed GUI
separately. Pin all executable helpers in the runtime manifest, including Python,
wrappers and document/image helpers; the bundle hash alone misses those changes.

The 2026-10-27 runtime work passed Mac ARM, Mac Intel and Windows Server CI.
Those runners had no licensed Stata or interactive Windows desktop. Do not claim
Windows native acceptance from successful CIM/lock/PowerShell and package tests.
Keep the actual Windows machine, Stata edition, Python/editor versions, lock and
consent transitions as operator cases. Source/reference builds remain separate.

An author DO displayed beside Terminal is useful evidence, but a compatibility
transform can execute different bytes. Archive and hash both versions, bind the
executed copy to its request and log, and do not claim displayed/executed equality
without checking it. A snapshot after completion is not a live visibility pass.
For a newly opened file, verify its group before dispatch: the current runtime
can follow the focused Terminal group when the source was not already visible.

## Test the actual graph route and restored DOM

Two native failures survived earlier isolated tests:

1. The Terminal handler and Graphs provider were sibling bundle closures. A
   module-private callback was invisible to the handler, which silently opened
   the ordinary editor. A VM harness had flattened the scopes and falsely passed.
   Export the callback explicitly and preserve the real module boundaries in
   regression tests. Keep the old implementation as a failing control.
2. `clearAllOutput` removed the artifact container during Terminal restoration.
   Later messages rendered into the still-referenced but detached element.
   Files existed and counters said two graphs, while no thumbnail was in the
   document. Preserve/reconnect the container and verify `isConnected` plus the
   actual rendered thumbnail, not only the in-memory object or render count.

In runtime dev.5, the reloaded private Mac Terminal displayed the saved graph
artifacts; thumbnail → modal Open created the real Stata Graphs panel and loaded
the expected image. Ten route/identity checks passed, including unchanged
execution request/run IDs, backend and reservation count across the preview.
That bounds the result to this route and version. It is not a new FULL45 suite.

Reuse saved GPH/data when testing a preview repair. The current artifact scanner
does not classify `graph use` alone as a graph-producing command. Preserve that
limitation; do not label a successful GPH load as an artifact-card pass. Any new
synthetic rendering stage gets its own request and outputs. Keep failed native
records rather than rerunning accepted research to manufacture a cleaner receipt.

The earlier dev.3 PNG/GPH case used SVG+sips compatibility. Both PNGs fully
decoded at 800×480 with equal pixels; a native GPH reload succeeded. This does
not establish native Mac bitmap recovery or every renderer/platform combination.

## Queue, cancellation and cleanup are separate outcomes

In the private dev.3 Mac check, Run File created scalar 40, the installed Python
client changed it to 42 with one POST, and actual Run Selection verified the same
state. Two clients were started while the first was busy; the second dispatched
after the first settled, with one POST per client. This establishes serial
sharing of that backend, not independent concurrent Stata engines.

Soft Stop preserved an original HTTP 500 cancellation response. The stop request
succeeded, the actual task and transport drained, scoped restore returned zero,
and the backend stayed the same without a hard reset. Cancellation-generation
wording in an error alone is not proof that Stata restarted. Verify actual process
identity, escalation fields, restored data and a later bounded request.

Use unique test frames, scalars and graph names. Verify the declared entry state,
data restoration and each cleanup return code. Remove only test-owned objects;
an empty restored original frame is not proof of complete global-session
equivalence. Preserve uncertain or failed operations and reconcile their original
requests; a verification error never authorizes automatic replay.

## Reference source builds and research handoff

The separate reference build pinned 27 upstream files and compared 15 outputs
across repeated local builds, Mac ARM/Intel CI and Windows CI. It did not run the
upstream Sentry upload script or replace the maintained `dist` tree. Equal build
outputs do not prove parity with the maintained bridge, state patches, finalizers
or graph UI. Port one behavior at a time and retain its existing regression and
package/native acceptance before changing the runtime entry point.

Keep plugin acceptance distinct from dissertation completion. The chapter data
cleaning/R-preparation branch, inventory counts, historical provenance gaps,
research definitions, model fitting and candidate adoption have their own
contracts. CFPS cleaning/wave-update logic belongs to the separate domain skill;
this skill manages execution, shared-session evidence and operational recovery.
Send concrete bounded evidence to the designated mainline session under the
existing communication authority. Notice receipt, full-body reading, limited
tracking and scientific acceptance are different states.

Runtime implementation and evidence ledger:
https://github.com/lzhs1995/stata-workbench-shared-session/pull/8

Reference source build:
https://github.com/lzhs1995/stata-workbench-shared-session/pull/9
