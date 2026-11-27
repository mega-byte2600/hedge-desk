"""Executable trust-boundary checks for the public paper-only repository."""

import ast
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPOSITORY_ROOT / "hedge_desk"
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"


def python_sources():
    # The boundary covers the package AND the scripts: the RoR-substitution
    # escape lived in scripts/real_nke_paper_trade.py (Sentry-era GAP 1,
    # 2026-11-26), which called estimate_risk_of_ruin and fed the result
    # into build_validated_risk_inputs while this test scanned hedge_desk/
    # only. A script is not a safer place to calculate RoR than the package.
    return tuple(sorted(PACKAGE_ROOT.rglob("*.py"))) + tuple(
        sorted(SCRIPTS_ROOT.rglob("*.py"))
    )


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_boundary_scan_covers_scripts(self) -> None:
        # Pin the coverage itself: if scripts/ ever drops out of
        # python_sources(), the two tests below pass for the wrong reason
        # (no offenders found because nothing was scanned).
        scanned = {str(p.relative_to(REPOSITORY_ROOT)) for p in python_sources()}
        self.assertIn("scripts/real_nke_paper_trade.py", scanned)
        self.assertIn("scripts/real_ccl_paper_trade.py", scanned)

    def test_risk_of_ruin_calculation_is_confined_to_conventional_boundary(self) -> None:
        allowed = {
            PACKAGE_ROOT / "risk" / "ruin.py",
        }
        offenders = []
        for path in python_sources():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = (
                        node.func.id
                        if isinstance(node.func, ast.Name)
                        else (
                            node.func.attr
                            if isinstance(node.func, ast.Attribute)
                            else ""
                        )
                    )
                    if name == "estimate_risk_of_ruin" and path not in allowed:
                        offenders.append(str(path.relative_to(REPOSITORY_ROOT)))
        self.assertEqual(offenders, [])

    def test_agentic_decision_runtime_does_not_import_ror_calculator(self) -> None:
        decision_source = (PACKAGE_ROOT / "core" / "decision.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("estimate_risk_of_ruin", decision_source)

    def test_validated_risk_inputs_cannot_be_constructed_by_agent_modules(self) -> None:
        allowed = {
            PACKAGE_ROOT / "risk" / "inputs.py",
            PACKAGE_ROOT / "demo.py",
        }
        offenders = []
        for path in python_sources():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = (
                        node.func.id
                        if isinstance(node.func, ast.Name)
                        else (
                            node.func.attr
                            if isinstance(node.func, ast.Attribute)
                            else ""
                        )
                    )
                    if name == "build_validated_risk_inputs" and path not in allowed:
                        offenders.append(str(path.relative_to(REPOSITORY_ROOT)))
        self.assertEqual(offenders, [])

    def test_paper_runtime_has_no_broker_or_network_client_dependency(self) -> None:
        forbidden_roots = {
            "alpaca", "ib_insync", "ibapi", "requests", "httpx", "websocket",
            "websockets",
        }
        offenders = []
        for path in python_sources():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules = [node.module]
                for module in modules:
                    if module.split(".", 1)[0] in forbidden_roots:
                        offenders.append(
                            f"{path.relative_to(REPOSITORY_ROOT)}:{module}"
                        )
        self.assertEqual(offenders, [])
        self.assertFalse((PACKAGE_ROOT / "broker").exists())

    def test_stat_inference_cannot_become_trade_or_control_authority(self) -> None:
        authority_paths = {
            PACKAGE_ROOT / "core" / "decision.py",
            PACKAGE_ROOT / "paper" / "workflow.py",
            PACKAGE_ROOT / "release.py",
            PACKAGE_ROOT / "backoffice" / "compliance.py",
            PACKAGE_ROOT / "backoffice" / "portfolio.py",
        }
        offenders = []
        for path in authority_paths:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules = [node.module]
                if any(module == "hedge_desk.stat_inference" for module in modules):
                    offenders.append(str(path.relative_to(REPOSITORY_ROOT)))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
