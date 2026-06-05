from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field, ValidationError, model_validator

REQUIRED_SECTION_ORDER: tuple[str, ...] = (
    "synopsis",
    "utility",
    "fortification_upgrades",
    "team_notes",
    "build_notes",
)


class MarkdownSection(BaseModel):
    """Markdown-heavy section rendered as prose."""

    kind: Literal["markdown"]
    key: Literal["synopsis", "team_notes", "build_notes"]
    title: str
    markdown: str = ""


class BulletsSection(BaseModel):
    """Bullet-list section rendered as a dense list."""

    kind: Literal["bullets"]
    key: Literal["utility"]
    title: str
    bullets: list[str] = Field(default_factory=list)


class UtilityRow(BaseModel):
    """Single utility row for two-column key/value rendering."""

    label: str
    detail: str


class UtilityTableSection(BaseModel):
    """Utility section rendered as a two-column table."""

    kind: Literal["utility_table"]
    key: Literal["utility"]
    title: str
    rows: list[UtilityRow] = Field(default_factory=list)


class FortificationUpgrade(BaseModel):
    """Single fortification row (one level)."""

    level: Literal[1, 2, 3, 4, 5, 6]
    description: str = ""


class FortificationTableSection(BaseModel):
    """Fixed table section for Segment 1-6 upgrades."""

    kind: Literal["fortification_table"]
    key: Literal["fortification_upgrades"]
    title: str
    upgrades: list[FortificationUpgrade] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_levels(self) -> "FortificationTableSection":
        levels = [row.level for row in self.upgrades]
        if levels != [1, 2, 3, 4, 5, 6]:
            raise ValueError(
                "fortification_upgrades must contain exactly six rows for levels 1..6 in order"
            )
        return self


NotesSection = Annotated[
    MarkdownSection | BulletsSection | UtilityTableSection | FortificationTableSection,
    Field(discriminator="kind"),
]


class DollNotesDocument(BaseModel):
    """Schema-backed notes document loaded from JSON."""

    doll: str
    sections: list[NotesSection]
    warning: str | None = None

    @model_validator(mode="after")
    def validate_required_sections(self) -> "DollNotesDocument":
        keys = [section.key for section in self.sections]
        if keys != list(REQUIRED_SECTION_ORDER):
            raise ValueError(
                "sections must contain exactly the required keys in order: "
                + ", ".join(REQUIRED_SECTION_ORDER)
            )
        return self


def _to_slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.strip().lower())
    return normalized.strip("_")


def _notes_directory() -> Path:
    # app/gui/templates/doll_notes.py -> app/resources/doll_notes
    return Path(__file__).resolve().parents[2] / "resources" / "doll_notes"


def get_default_notes_document(doll_name: str) -> DollNotesDocument:
    sections: list[NotesSection] = [
        MarkdownSection(
            kind="markdown",
            key="synopsis",
            title="Synopsis",
            markdown="Add notes here.",
        ),
        BulletsSection(
            kind="bullets",
            key="utility",
            title="Utility",
            bullets=["Add utility notes."],
        ),
        FortificationTableSection(
            kind="fortification_table",
            key="fortification_upgrades",
            title="Fortification Level upgrades",
            upgrades=[
                FortificationUpgrade(level=1, description="Add exact benefit notes."),
                FortificationUpgrade(level=2, description="Add exact benefit notes."),
                FortificationUpgrade(level=3, description="Add exact benefit notes."),
                FortificationUpgrade(level=4, description="Add exact benefit notes."),
                FortificationUpgrade(level=5, description="Add exact benefit notes."),
                FortificationUpgrade(level=6, description="Add exact benefit notes."),
            ],
        ),
        MarkdownSection(
            kind="markdown",
            key="team_notes",
            title="Team notes",
            markdown="Add team synergy notes.",
        ),
        MarkdownSection(
            kind="markdown",
            key="build_notes",
            title="Build notes",
            markdown="Add build priorities and tradeoffs.",
        ),
    ]
    return DollNotesDocument(doll=doll_name, sections=sections)


def load_notes_document(doll_name: str) -> DollNotesDocument:
    """Load a Doll notes document from resources, with safe fallback."""
    slug = _to_slug(doll_name)
    notes_path = _notes_directory() / f"{slug}.json"

    if not notes_path.exists():
        return get_default_notes_document(doll_name)

    try:
        payload = json.loads(notes_path.read_text(encoding="utf-8").lstrip("\ufeff"))
        loaded = DollNotesDocument.model_validate(payload)

        # Ensure each file can only describe its matching Doll to avoid accidental mixups.
        if _to_slug(loaded.doll) != slug:
            fallback = get_default_notes_document(doll_name)
            fallback.warning = f"Notes file doll name '{loaded.doll}' does not match page '{doll_name}'."
            return fallback

        return loaded
    except (json.JSONDecodeError, ValidationError) as error:
        fallback = get_default_notes_document(doll_name)
        fallback.warning = f"Could not load notes file: {error}"
        return fallback
