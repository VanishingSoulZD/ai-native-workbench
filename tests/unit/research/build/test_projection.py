from copy import deepcopy

from ai_native_workbench.research.build import project_dataset, project_research_note, resolve_snapshot_state
from ai_native_workbench.research.canonical import CanonicalRegistry, Claim, Entity, Evidence, Source, Unknown


def resolved_state():
    registry = CanonicalRegistry()
    source_ref = registry.register(Source('source', 'Primary source', 'Publisher', 'https://example.test', 'report', '', '', 'high'))
    entity_ref = registry.register(Entity('entity', 'organization', 'Example', 'active', {'region': 'global'}))
    evidence_ref = registry.register(Evidence('evidence', source_ref, 'Observed', '', 'report', 'high', (), (), ''))
    claim_a_ref = registry.register(Claim('claim-a', 'Active claim', entity_ref, 'factual', 'active', 0.9, (evidence_ref,)))
    claim_b_ref = registry.register(Claim('claim-b', 'Provisional claim', entity_ref, 'factual', 'provisional', 0.4, (evidence_ref,)))
    registry.replace(evidence_ref, Evidence('evidence', source_ref, 'Observed', '', 'report', 'high', (claim_a_ref,), (claim_b_ref,), ''))
    unknown_ref = registry.register(Unknown('unknown', 'What is missing?', 'It limits confidence.', 'scope', 'open'))
    snapshot = registry.snapshot('snapshot', (source_ref, entity_ref, evidence_ref, claim_a_ref, claim_b_ref, unknown_ref), case_id='case', cutoff='2026', workflow_version='workflow')
    return registry, snapshot, claim_a_ref, claim_b_ref, evidence_ref, unknown_ref


def test_dataset_preserves_directional_evidence_relations_and_identity():
    registry, snapshot, claim_a_ref, claim_b_ref, evidence_ref, _ = resolved_state()
    projection = project_dataset(resolve_snapshot_state(snapshot, registry), 'projection-v1')
    row = next(row for row in projection.rows if row.ref == evidence_ref)
    assert row.ref == evidence_ref
    assert row.fields['supports_claim_refs'] == (str(claim_a_ref),)
    assert row.fields['contradicts_claim_refs'] == (str(claim_b_ref),)
    assert str(claim_b_ref) not in row.fields['supports_claim_refs']
    assert str(claim_a_ref) not in row.fields['contradicts_claim_refs']


def test_projection_preserves_unknown_provenance_qualification_and_snapshot_state():
    registry, snapshot, claim_a_ref, _, _, unknown_ref = resolved_state()
    resolved = resolve_snapshot_state(snapshot, registry)
    registry.replace(claim_a_ref, Claim('claim-a', 'Current registry value', resolved.states[claim_a_ref].subject_ref, 'factual', 'active', 0.9, resolved.states[claim_a_ref].evidence_ids))
    dataset = project_dataset(resolved, 'projection-v1')
    note = project_research_note(resolved, 'projection-v1')
    claim_row = next(row for row in dataset.rows if row.ref == claim_a_ref)
    assert claim_row.fields['statement'] == 'Active claim'
    assert claim_row.fields['evidence_refs'] == ('evidence:evidence',)
    assert any(row.ref == unknown_ref and row.object_type == 'unknown' for row in dataset.rows)
    finding = next(section for section in note.sections if section.heading == 'Key Findings')
    assert any('Active claim' in paragraph and 'status: active' in paragraph and 'confidence: 0.9' in paragraph for paragraph in finding.paragraphs)
    assert any('Provisional claim' in paragraph and 'status: provisional' in paragraph and 'confidence: 0.4' in paragraph for paragraph in finding.paragraphs)
    assert 'Current registry value' not in '\n'.join(finding.paragraphs)
    assert any(section.heading == 'Unknowns / Limitations' and section.refs == (unknown_ref,) for section in note.sections)
    assert any(section.heading == 'Provenance' and tuple(str(ref) for ref in section.refs) == ('source:source',) for section in note.sections)


def test_projection_is_deterministic_read_only_and_has_only_declared_fields():
    registry, snapshot, *_ = resolved_state()
    resolved = resolve_snapshot_state(snapshot, registry)
    before = tuple((ref, obj) for ref, obj in resolved.states.items())
    first = project_dataset(resolved, 'projection-v1')
    assert first == project_dataset(resolved, 'projection-v1')
    assert before == tuple((ref, obj) for ref, obj in resolved.states.items())
    expected = {'id', 'observation', 'date_or_period', 'evidence_type', 'evidence_grade', 'source_ref', 'supports_claim_refs', 'contradicts_claim_refs', 'note'}
    evidence_row = next(row for row in first.rows if row.object_type == 'evidence')
    assert set(evidence_row.fields) == expected
