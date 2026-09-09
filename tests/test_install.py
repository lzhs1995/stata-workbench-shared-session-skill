import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def test_dry_run_does_not_create_routes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = installer.install(root / "store", root, False)
            self.assertFalse((root / "store").exists())
            self.assertFalse(plan["runtimeTouched"])

    def test_preserves_files_and_symlink_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claude = root / ".claude/skills/stata-workbench-shared-session"
            claude.mkdir(parents=True); (claude / "SKILL.md").write_text("original")
            agents = root / ".agents/skills/stata-workbench-shared-session"
            agents.parent.mkdir(parents=True); agents.symlink_to(claude)
            plan = installer.install(root / "store", root, True)
            self.assertEqual((Path(plan["routes"][0]["backup"]) / "SKILL.md").read_text(), "original")
            self.assertTrue(Path(plan["routes"][1]["backup"]).is_symlink())
            self.assertEqual(claude.resolve(), agents.resolve())
            with self.assertRaises(FileExistsError):
                installer.install(root / "store", root, True)

    def test_partial_failure_restores_original_routes_with_durable_journal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            route = root / ".claude/skills/stata-workbench-shared-session"
            route.mkdir(parents=True); (route / "SKILL.md").write_text("original")
            old = Path.symlink_to
            def fail_agents(path, *args, **kwargs):
                if ".agents" in path.parts:
                    raise OSError("injected route failure")
                return old(path, *args, **kwargs)
            with patch.object(Path, "symlink_to", fail_agents):
                with self.assertRaises(OSError):
                    installer.install(root / "store", root, True)
            self.assertEqual((route / "SKILL.md").read_text(), "original")
            self.assertFalse(route.is_symlink())
            dest = next((root / "store").iterdir())
            self.assertTrue((dest / "installation-plan.json").is_file())
            self.assertTrue((dest / "installation-failure.json").is_file())
            self.assertFalse((dest / "installation.json").exists())


if __name__ == "__main__":
    unittest.main()
