import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "web" / "index.html"


class SidebarChromeTests(unittest.TestCase):
    def test_dead_workspace_ordinal_is_not_public_ui(self):
        index = INDEX.read_text(encoding="utf-8")
        self.assertNotIn('class="workspace-label"', index)
        self.assertNotIn('WORKSPACE <span>01</span>', index)
        self.assertIn('<nav aria-label="Workspace">', index)


if __name__ == "__main__":
    unittest.main()
