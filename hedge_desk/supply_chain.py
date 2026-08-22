"""Minimal deterministic checks for pinned third-party GitHub Actions."""

from pathlib import Path
import re
from typing import Tuple


_USES = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)
_FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def validate_github_action_pins(workflow_paths: Tuple[Path, ...]) -> Tuple[str, ...]:
    reasons = []
    for path in sorted(workflow_paths, key=lambda item: str(item)):
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            reasons.append(f"WORKFLOW_UNREADABLE:{path.name}")
            continue
        for reference in _USES.findall(source):
            if reference.startswith("./"):
                continue
            if "@" not in reference:
                reasons.append(f"ACTION_REFERENCE_MISSING_REVISION:{path.name}:{reference}")
                continue
            action, revision = reference.rsplit("@", 1)
            if not action or not _FULL_SHA.fullmatch(revision):
                reasons.append(f"ACTION_NOT_PINNED_TO_SHA:{path.name}:{reference}")
    return tuple(sorted(set(reasons)))
