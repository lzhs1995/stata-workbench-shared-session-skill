# AGENTS.md

Entry point for AI agents. The instructions are plain Markdown and do not
depend on one vendor's agent; any agent that can read files and run a Python
CLI can follow them.

| You want to | Read |
| --- | --- |
| Run Stata code in a person's existing Stata Workbench Shared Session | [skills/stata-workbench-shared-session/SKILL.md](skills/stata-workbench-shared-session/SKILL.md). It is the authority; this file only points to it |
| Install the skill for Claude Code, Codex or `.agents` | [README.md](README.md#install-the-skill): `scripts/install.py` is a dry run until `--apply` |
| Re-check a run's receipt offline | [references/receipts-rc745.md](skills/stata-workbench-shared-session/references/receipts-rc745.md) |
| Find which runtime version the skill matches | `runtime-compatibility.json` (runtime `v0.1.3-rc.7.45`) |
| Change this repository | [Changing this repository](#changing-this-repository) |

The runtime itself (the VS Code extension and `tools/shared_stata.py`) lives in
[lzhs1995/stata-workbench-shared-session](https://github.com/lzhs1995/stata-workbench-shared-session).
Use a clone checked out at the tag in `runtime-compatibility.json`.

## Before you run anything

Read SKILL.md sections 2–7 and 10–11. The rules agents most often get wrong:

- Use the person's real `STATA_WORKBENCH_PROFILE` and `STATA_WORKBENCH_PORT`,
  not the README defaults.
- One POST per call. `EXECUTION_UNCONFIRMED_NO_RETRY` does not mean "did not
  run": read the receipt and never resend that call.
- Show a diff and wait for acceptance before changing a `.do` the person
  already has.
- Never start a second Stata, backend or VS Code profile to get around a busy or
  STALE session, and never kill Stata.

## Changing this repository

```sh
python3 -B -m unittest discover -s tests
STATA_WORKBENCH_RUNTIME=/abs/runtime python3 -B -m unittest discover -s tests
python3 -B scripts/runtime_contract_check.py --runtime-root /abs/runtime
```

- A change to SKILL.md or its references needs a new `skillVersion` in
  `runtime-compatibility.json` and a CHANGELOG entry; the installer never
  overwrites an installed version.
- Only document options and commands the pinned runtime has; the contract check
  enforces this for SKILL.md, references, every README and this file.
- Synthetic data only. Never add research data, receipts, private backups or
  credentials.

## What has been checked with agents

- Reading: with no prior context, a Claude Code subagent and a Codex session each
  read SKILL.md (0.1.0-dev.7) and its linked references within the skill directory,
  then answered a 10-question operating test
  (19/20 and 17/20; pass line 16, no zero on the safety questions), 2026-10-31
  and 2026-11-01.
- Install: `scripts/install.py` is covered by synthetic tests on Ubuntu and
  macOS CI. Installing on Windows is not covered by CI.
- Not checked: a live run started by each named agent product through an
  installed route, and agents other than Claude Code and Codex.
