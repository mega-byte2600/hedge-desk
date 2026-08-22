"""Executable trust-boundary checks for the public paper-only repository."""

import ast
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPOSITORY_ROOT / "hedge_desk"


def python_sources():
    return tuple(sorted(PACKAGE_ROOT.rglob("*.py")))


class ArchitectureBoundaryTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
