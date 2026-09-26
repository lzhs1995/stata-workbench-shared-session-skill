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
