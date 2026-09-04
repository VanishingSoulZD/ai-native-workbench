import json
import pytest

from ai_native_workbench.research.build import (
    DatasetProjection,
    ResearchNoteProjection,
    render_dataset_csv,
    render_dataset_json,
    render_research_note_markdown,
)
from ai_native_workbench.research.build.projection import DatasetRow, ResearchNoteSection
from ai_native_workbench.research.build.errors import BuildValidationError
from ai_native_workbench.research.canonical import CanonicalObjectType, CanonicalRef


def dataset_projection():
    row = DatasetRow(CanonicalRef(CanonicalObjectType.CLAIM, 'claim'), 'claim', 'claim', {'statement': 'Projected only', 'evidence_refs': ('evidence:e1',)})
    return DatasetProjection('v1', (row,))


def note_projection():
    ref = CanonicalRef(CanonicalObjectType.UNKNOWN, 'unknown')
    return ResearchNoteProjection('v1', (ResearchNoteSection('Unknowns / Limitations', ('Open question',), (ref,)),))


def test_dataset_renderers_emit_declared_deterministic_representations():
    projection = dataset_projection()
    rendered_json = render_dataset_json(projection)
    assert json.loads(rendered_json) == {'projection_version': 'v1', 'rows': [{'fields': {'evidence_refs': ['evidence:e1'], 'statement': 'Projected only'}, 'logical_id': 'claim', 'object_type': 'claim', 'ref': 'claim:claim'}]}
    assert render_dataset_json(projection) == rendered_json
    assert render_dataset_csv(projection) == 'ref,object_type,logical_id,fields_json\nclaim:claim,claim,claim,"{""evidence_refs"":[""evidence:e1""],""statement"":""Projected only""}"\n'


def test_note_renderer_preserves_projected_content_and_provenance_without_inference():
    rendered = render_research_note_markdown(note_projection())
    assert rendered == '# Research Note\n\n## Unknowns / Limitations\nOpen question\nProvenance reference: unknown:unknown\n'
    assert render_research_note_markdown(note_projection()) == rendered


@pytest.mark.parametrize('renderer', [render_dataset_json, render_dataset_csv, render_research_note_markdown])
def test_renderers_reject_invalid_projection_input(renderer):
    with pytest.raises(BuildValidationError):
        renderer(object())
