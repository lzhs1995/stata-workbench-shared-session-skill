# Stata Workbench Shared Session — operating skill

Operating skill for agents that run Stata in the user's existing
[Stata Workbench Shared Session](https://github.com/lzhs1995/stata-workbench-shared-session),
so that the person and the agent share one visible Stata session.

This version describes runtime **v0.1.3-rc.7.45** (pre-release). Pins, platform
results and the agent route are in `runtime-compatibility.json`; CI checks the
skill against a checkout of that tag.

Start with [SKILL.md](skills/stata-workbench-shared-session/SKILL.md). It is
ordered for use: what the runtime is, who runs the code, a three-minute start on
macOS and Windows, the full client options, Stop, receipts and exit codes,
troubleshooting, known limitations and platform notes. The references cover
staged work, receipts, author DO preservation, storage, exports, replay and
desktop recovery.

## Install the skill

Installation is separate from the runtime: it never updates Workbench, restarts
a backend or contacts another agent.

```sh
python3 -B scripts/install.py --prefix /absolute/skill-storage
# Inspect the proposed changes, then:
python3 -B scripts/install.py --prefix /absolute/skill-storage --apply
```

The installer copies the skill and its receipt checkers into
`<prefix>/<skillVersion>/`, then points the Claude, Codex and `.agents` skill
routes at it. Existing routes are kept as timestamped backups; an existing
version directory is never overwritten.

## Checks

```sh
python3 -B -m unittest discover -s tests
# With a runtime checkout at the pinned tag:
STATA_WORKBENCH_RUNTIME=/abs/runtime python3 -B -m unittest discover -s tests
python3 -B scripts/runtime_contract_check.py --runtime-root /abs/runtime
```

`runtime_contract_check.py` fails when the skill mentions a client option or a
`stata-workbench.*` command that the pinned runtime does not have, when the
pins differ from the checkout, or when it checked nothing.

This repository contains operating guidance, offline checkers and synthetic
tests only. Never add research data, receipts, private backups or credentials.
