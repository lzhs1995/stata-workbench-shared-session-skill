"""Install skill routes with recoverable exact-target backups; default dry-run."""
import argparse
import datetime
import json
from pathlib import Path
import shutil
import os

ROOT = Path(__file__).resolve().parents[1]


def journal(path, value):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as handle:
        json.dump(value, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())


def install(prefix, user_root, apply=False):
    version = json.loads((ROOT / "runtime-compatibility.json").read_bytes())["skillVersion"]
    dest = Path(prefix).resolve() / version
    source = ROOT / "skills/stata-workbench-shared-session"
    routes = [Path(user_root) / client / "skills/stata-workbench-shared-session" for client in (".claude", ".agents", ".codex")]
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    plan = {"version": version, "destination": str(dest), "apply": apply,
            "routes": [{"path": str(p), "backup": str(p.with_name(p.name + ".backup-" + stamp))} for p in routes],
            "runtimeTouched": False, "liveAcceptance": "PENDING"}
    if not apply:
        return plan
    if dest.exists():
        raise FileExistsError("version already installed; never overwrite it: " + str(dest))
    # Copy only tracked skill/runtime contract, not receipts or arbitrary scratch.
    dest.mkdir(parents=True, exist_ok=False)
    shutil.copytree(source, dest / "skills/stata-workbench-shared-session")
    # Receipt tools must be reachable from the installed skill, not only a clone.
    checks = dest / "skills/stata-workbench-shared-session/scripts"
    checks.mkdir(exist_ok=True)
    for name in ("completion_check.py", "empirical_trace.py"):
        shutil.copy2(ROOT / "scripts" / name, checks / name)
    shutil.copy2(ROOT / "runtime-compatibility.json", dest / "runtime-compatibility.json")
    for row in plan["routes"]:
        row["existed"] = Path(row["path"]).exists() or Path(row["path"]).is_symlink()
    journal(dest / "installation-plan.json", plan)  # durable BEFORE any route mutation
    installed = []
    try:
        for index, row in enumerate(plan["routes"]):
            target, backup = Path(row["path"]), Path(row["backup"])
            target.parent.mkdir(parents=True, exist_ok=True)
            if backup.exists() or backup.is_symlink():
                raise FileExistsError(str(backup))
            if target.exists() or target.is_symlink():
                target.rename(backup)  # symlink itself, never its referent
            installed.append(row)
            target.symlink_to(dest / "skills/stata-workbench-shared-session", target_is_directory=True)
            journal(dest / ("route-%d.json" % index), row)
        journal(dest / "installation.json", plan)
    except Exception as error:
        rollback = []
        for row in reversed(installed):
            target, backup = Path(row["path"]), Path(row["backup"])
            try:
                # Remove ONLY our exact newly installed link, never arbitrary data.
                if target.is_symlink() and os.readlink(target) == str(dest / "skills/stata-workbench-shared-session"):
                    target.unlink()
                if backup.exists() or backup.is_symlink():
                    if target.exists() or target.is_symlink():
                        raise RuntimeError("route concurrently changed; preserve both paths")
                    backup.rename(target)
                rollback.append({"path": str(target), "restored": True})
            except Exception as restoration:
                rollback.append({"path": str(target), "restored": False, "error": repr(restoration)})
        journal(dest / "installation-failure.json", {"error": repr(error), "rollback": rollback})
        raise
    return plan


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prefix", type=Path, required=True)
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()
    print(json.dumps(install(a.prefix, Path.home(), a.apply), indent=2))
