"""Check that the skill only documents options, commands and pins the pinned runtime has.

Inputs: this skill repository and a checkout of the runtime at the tag named in
runtime-compatibility.json. Read-only; prints JSON; exit 0 = PASS, 2 = FAIL.

Rules
- Every `--option` inside a fenced code block or an inline code span in the
  skill's Markdown must be an argparse option of the runtime's tools/*.py or of
  this repository's scripts/*.py, or be listed in scripts/known_external_flags.json.
  When the same line or span names a script (`shared_stata.py`), the option must
  belong to that script.
  Entries marked "historical" may appear only in inline code (they document
  options that do not exist), never in a fenced command block.
- Every `stata-workbench.<id>` must be a command contributed by package.json.
- runtime-compatibility.json pins must equal the checkout (version, bundle sha256,
  client constants).
- Zero checked options or zero checked commands is a FAIL (vacuous gate).
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FLAG = re.compile(r"(?:(?<=^)|(?<=[\s`'\"(\[|=]))(--[a-z][a-z0-9]*(?:-[a-z0-9]+)*)")
SCRIPT = re.compile(r"([A-Za-z0-9_]+\.py)\b")
COMMAND = re.compile(r"\bstata-workbench\.([A-Za-z][A-Za-z0-9]*)\b")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE = re.compile(r"`([^`\n]+)`")


def argparse_options(paths):
    """Map script file name -> set of its `--options` (argparse add_argument literals)."""
    found = {}
    for path in paths:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=str(path))
        options = found.setdefault(Path(path).name, set())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "add_argument":
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value.startswith("--"):
                        options.add(arg.value)
    return found


def markdown_mentions(files):
    """Yield (file, line, kind, text) for fenced code lines and inline code spans."""
    for path in files:
        fenced = False
        for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced:
                yield path, number, "fenced", line
            else:
                for span in INLINE.findall(line):
                    yield path, number, "inline", span


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def module_constants(path, names):
    values = {}
    for node in ast.parse(Path(path).read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    values[target.id] = node.value.value
    return values


def check(skill_root, runtime_root):
    skill_root, runtime_root = Path(skill_root).resolve(), Path(runtime_root).resolve()
    compat = json.loads((skill_root / "runtime-compatibility.json").read_bytes())
    allow = json.loads((skill_root / "scripts/known_external_flags.json").read_bytes())["options"]
    by_script = argparse_options(sorted((runtime_root / "tools").glob("*.py")))
    by_script.update(argparse_options(sorted((skill_root / "scripts").glob("*.py"))))
    known = set().union(*by_script.values()) if by_script else set()
    runtime_options = set().union(*argparse_options(sorted((runtime_root / "tools").glob("*.py"))).values())
    package = json.loads((runtime_root / "package.json").read_bytes())
    commands = {c["command"] for c in package.get("contributes", {}).get("commands", [])}
    files = sorted((skill_root / "skills").rglob("*.md")) + [skill_root / "README.md"]
    problems, used_allow = [], set()
    flags_checked = commands_checked = 0
    for path, line, kind, text in markdown_mentions(files):
        where = f"{path.relative_to(skill_root)}:{line}"
        named = [name for name in SCRIPT.findall(text) if name in by_script]
        for option in FLAG.findall(text):
            flags_checked += 1
            entry = allow.get(option)
            if entry is not None:
                used_allow.add(option)
                if entry.get("category") == "historical" and kind == "fenced":
                    problems.append({"where": where, "problem": "HISTORICAL_OPTION_IN_COMMAND_BLOCK", "option": option})
                continue
            if named:
                if not any(option in by_script[name] for name in named):
                    problems.append({"where": where, "problem": "OPTION_NOT_IN_NAMED_SCRIPT",
                                     "option": option, "scripts": named})
            elif option not in known:
                problems.append({"where": where, "problem": "UNKNOWN_OPTION", "option": option})
    for path in files:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for name in COMMAND.findall(line):
                commands_checked += 1
                if "stata-workbench." + name not in commands:
                    problems.append({"where": f"{path.relative_to(skill_root)}:{number}",
                                     "problem": "UNKNOWN_COMMAND", "command": "stata-workbench." + name})
    runtime = compat.get("runtime") or {}
    client = module_constants(runtime_root / "tools/verified_workbench.py", {"VERSION", "BUNDLE_SHA256"})
    bundle = sha256(runtime_root / "dist/extension.js")
    pins = {
        "versionMatchesPackage": runtime.get("version") == package.get("version"),
        "tagMatchesVersion": runtime.get("tag") == "v" + str(package.get("version")),
        "bundleSha256MatchesCheckout": runtime.get("bundleSha256") == bundle,
        "clientPinsMatch": client.get("VERSION") == package.get("version") and client.get("BUNDLE_SHA256") == bundle,
    }
    problems += [{"problem": "PIN_MISMATCH", "check": k} for k, ok in pins.items() if not ok]
    if not runtime_options or not commands:
        problems.append({"problem": "VACUOUS_RUNTIME", "runtimeOptions": len(runtime_options), "commands": len(commands)})
    if flags_checked == 0 or commands_checked == 0:
        problems.append({"problem": "VACUOUS_SKILL", "optionsChecked": flags_checked, "commandsChecked": commands_checked})
    return {"verdict": "PASS" if not problems else "FAIL", "runtimeRoot": str(runtime_root),
            "optionsChecked": flags_checked, "commandsChecked": commands_checked,
            "runtimeOptions": len(runtime_options), "runtimeCommands": len(commands), "pins": pins,
            "unusedAllowEntries": sorted(set(allow) - used_allow), "problems": problems}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runtime-root", type=Path, required=True,
                        help="checkout of lzhs1995/stata-workbench-shared-session at the pinned tag")
    parser.add_argument("--skill-root", type=Path, default=ROOT)
    args = parser.parse_args()
    out = check(args.skill_root, args.runtime_root)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["verdict"] == "PASS" else 2)
