"""Deterministic Markdown serialization for research-note projections."""

from ..errors import BuildValidationError
from ..projection import ResearchNoteProjection


def render_research_note_markdown(projection: ResearchNoteProjection) -> str:
    if not isinstance(projection, ResearchNoteProjection):
        raise BuildValidationError("Research-note renderer requires a ResearchNoteProjection.")
    lines = ["# Research Note"]
    for section in projection.sections:
        lines.extend(("", f"## {section.heading}", *section.paragraphs))
        lines.extend(f"Provenance reference: {reference}" for reference in section.refs)
    return "\n".join(lines) + "\n"
