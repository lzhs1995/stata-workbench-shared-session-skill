## Guidance fixes 2026-11-01 (skill version unchanged, 0.1.0-dev.7)

- Section 1: say where `runtime-compatibility.json` really is. "Two directories
  above this file" holds only for the installed folder itself. On macOS the
  agent opens a symlink to it; on Windows the junctions point at cc-switch's
  plain copies, which do not contain the file (checked 2026-11-01).
- Section 7, window count not 1: check `STATA_WORKBENCH_PROFILE` and
  `STATA_WORKBENCH_PORT` first, then ask the person to keep one window. In the
  2026-10-31/11-01 readability test both a Claude and a Codex reader missed the
  profile/port check.

## 0.1.0-dev.7 — rc.7.45 full refresh, 2026-10-31

Pair the skill with runtime `v0.1.3-rc.7.45` (tag commit `fa76d6db`, bundle
`f02ae627…`, VSIX `b371bc61…`). The `visible-cowork/1` candidate pairing is
retired: rc.7.45 has no co-working ticket route; the agent route is
`tools/shared_stata.py` with one POST.

- SKILL.md rewritten in order of use: who runs the code, a three-minute start on
  macOS and Windows, every client option (checked against argparse), editor
  command ids, Stop and what to check after it, verdicts and exit codes,
  troubleshooting, rc.7.45 known limitations, platform notes, working rules.
- Removed options that rc.7.45 does not have (`--task`, `--control`,
  `--resume-from`) from command examples; `workflow.md` now describes staged work
  as one saved do-file per call.
- New `scripts/rc745_receipt_check.py` re-checks an rc.7.45 receipt offline;
  `completion_check.py` remains for earlier candidate receipts.
- New `scripts/runtime_contract_check.py` (CI): every documented option and
  command must exist in the pinned runtime, pins must match the checkout, and a
  check that inspected nothing fails. CI checks out the runtime at the pinned tag
  and runs on Ubuntu and macOS with Python 3.14.
- `runtime-compatibility.json` schema 2 with runtime tag, commit, bundle and VSIX
  hashes and per-platform results.
- The installer now keeps route backups under `<prefix>/route-backups/<stamp>/`
  instead of next to the route: a `.backup-*` sibling inside a skills folder still
  contains a SKILL.md with this skill's name.

## 0.1.0-dev.6 — cross-platform acceptance guidance, 2026-10-27

Add native Windows/Mac adapter and evidence boundaries, Windows ZIP replacement,
actual bundle-scope and Terminal DOM failures, same-backend cancellation/queue
lessons, and separate upstream reference-build claims. The runtime protocol pair
and its PENDING status are unchanged; this documentation does not replace a live
Workbench or certify a Windows desktop.

## Recovery guide 2026-10-17

Record the three-stage cmux incident: an ad-hoc Codex caller rejected by -67050,
RTK piping interactive stdout/stderr, and remaining helper onboarding. Add the
verified controlling-terminal repair, exact signing requirement syntax, original
session preservation and new Workbench generation checks. Distinguish actual
desktop success from a default Code window and the still-unrestored original
listener. Preserve failed attempts and corrections. Documentation only; no
extension reload, research replay or collaboration-transport change.

## Operating guide 2026-10-01

Honor explicit permission to cover, hide or minimize the bound Workbench window,
with execution and physical visibility reported separately. Add instance isolation,
UI coordination, conditional model output and no-duplicate resume guidance.
Documentation only; keep the pinned runtime/client and existing acceptance limits.

## 0.1.0-dev.5 — 2026-09-26

Add compound result checks and explicit legacy/candidate runtime routing. The candidate protocol remains PENDING; no native Stata runtime upgrade or certification is implied.

# Changelog

## 0.1.0-dev.2 — development, not live certified

- Independent canonical skill with Claude/Codex/.agents route installer.
- Automatic stage execution contract; no per-stage approval prompts.
- Mandatory distinct source/Terminal groups, exact source hashes and backend.
- Separate execution, observed visibility, replay and whole-task claims.
- Pause/resume boundaries: verified completed prefix only; never retry unknowns.
- Preserve installer backups and write-ahead journal; restore on partial failure.
- Independent receipt checks reject echoed commands, absent fields, bool-as-int,
  stale request/run bindings, changed backend/files and visibility interruptions.
- Accept actual leading Stata SMCL style tags without treating an echoed command
  as an executed completion marker.
- Seven synthetic tests. No new runtime installation or live acceptance claimed.
# 0.1.0-dev.3 — candidate only

- Independently bind authored snapshot, prepared compatibility output, archived
  execution bytes, working directory, actual wire command and current-run source
  diagnostics. Temporary runtime files need not survive for archive verification.
- Keep confirmed execution, observed visibility, repeatability and whole-task
  completion separate. Eight synthetic tests pass; live acceptance is pending.
# 0.1.0-dev.4 — candidate only

- Pair with the client's explicit `SCREEN_LOCKED` observation: window count is
  unknown while locked, not zero or permission-denied; no automatic unlock or
  research dispatch. Backend identity and readiness remain separate evidence.
