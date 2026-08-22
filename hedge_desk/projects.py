"""Machine-readable registry for the Hedge Desk MVP program."""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class ProjectStatus(str, Enum):
    WORKING_FOUNDATION = "working_foundation"
    ARCHITECTURE_ONLY = "architecture_only"


@dataclass(frozen=True)
class MvpProject:
    number: int
    project_id: str
    name: str
    status: ProjectStatus
    objective: str


MVP_PROJECTS: Tuple[MvpProject, ...] = (
    MvpProject(
        1,
        "overnight-premium-desk",
        "Overnight Premium Desk",
        ProjectStatus.WORKING_FOUNDATION,
        "Research defined-risk option premium opportunities with timed exits.",
    ),
    MvpProject(
        2,
        "earnings-event-desk",
        "Earnings Event Desk",
        ProjectStatus.WORKING_FOUNDATION,
        "Compare equity, defined-risk option, hedged-equity, and no-trade arms.",
    ),
    MvpProject(
        3,
        "arbitrage-observer",
        "European Index Box/Parity Observer",
        ProjectStatus.WORKING_FOUNDATION,
        "Observe executable parity and box dislocations after all costs.",
    ),
    MvpProject(
        4,
        "dividend-opportunity-desk",
        "Dividend Opportunity Desk",
        ProjectStatus.WORKING_FOUNDATION,
        "Rank sustainable dividend opportunities and compare shares, options, and no trade.",
    ),
    MvpProject(
        5,
        "open-quant-ai-model-lab",
        "Open Quant/AI Model Lab",
        ProjectStatus.WORKING_FOUNDATION,
        "Run independent Quant and AI research teams with reproducible open artifacts.",
    ),
)


def validate_project_registry(
    projects: Tuple[MvpProject, ...] = MVP_PROJECTS,
) -> None:
    """Fail when project numbering or stable identities become ambiguous."""
    if tuple(project.number for project in projects) != tuple(
        range(1, len(projects) + 1)
    ):
        raise ValueError("MVP project numbers must be contiguous and ordered")
    if len({project.project_id for project in projects}) != len(projects):
        raise ValueError("MVP project identifiers must be unique")
