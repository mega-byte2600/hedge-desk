from dataclasses import replace
import unittest

from hedge_desk.projects import MVP_PROJECTS, ProjectStatus, validate_project_registry


class ProjectRegistryTests(unittest.TestCase):
    def test_fourth_mvp_is_dividend_desk_and_not_claimed_as_built(self) -> None:
        validate_project_registry()
        dividend = MVP_PROJECTS[3]
        self.assertEqual(dividend.number, 4)
        self.assertEqual(dividend.project_id, "dividend-opportunity-desk")
        self.assertEqual(dividend.status, ProjectStatus.ARCHITECTURE_ONLY)

    def test_duplicate_project_identity_fails_closed(self) -> None:
        duplicate = replace(MVP_PROJECTS[4], project_id=MVP_PROJECTS[0].project_id)
        with self.assertRaisesRegex(ValueError, "identifiers must be unique"):
            validate_project_registry(MVP_PROJECTS[:4] + (duplicate,))

    def test_fifth_mvp_is_open_quant_ai_lab(self) -> None:
        project = MVP_PROJECTS[4]
        self.assertEqual(project.number, 5)
        self.assertEqual(project.project_id, "open-quant-ai-model-lab")
        self.assertEqual(project.status, ProjectStatus.WORKING_FOUNDATION)

    def test_earnings_mvp_has_working_point_in_time_foundation(self) -> None:
        self.assertEqual(MVP_PROJECTS[1].status, ProjectStatus.WORKING_FOUNDATION)

    def test_arbitrage_mvp_has_working_executable_edge_foundation(self) -> None:
        self.assertEqual(MVP_PROJECTS[2].status, ProjectStatus.WORKING_FOUNDATION)


if __name__ == "__main__":
    unittest.main()
