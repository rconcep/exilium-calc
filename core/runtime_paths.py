from __future__ import annotations

from pathlib import Path
import sys


def _candidate_roots() -> list[Path]:
    roots: list[Path] = []

    if getattr(sys, "frozen", False):
        roots.append(Path(sys.executable).resolve().parent)

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        roots.append(Path(meipass))

    roots.append(Path.cwd())
    roots.append(Path(__file__).resolve().parents[1])

    unique_roots: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root)
        if key not in seen:
            seen.add(key)
            unique_roots.append(root)

    return unique_roots


def get_resources_root() -> Path:
    """Return the best-available resources directory for the current runtime."""
    for root in _candidate_roots():
        candidate = root / "resources"
        if candidate.exists():
            return candidate

    return Path(__file__).resolve().parents[1] / "resources"


def get_resource_path(*parts: str) -> Path:
    return get_resources_root().joinpath(*parts)