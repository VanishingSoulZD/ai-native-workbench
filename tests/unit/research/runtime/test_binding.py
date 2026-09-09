"""Tests for Run-level Case binding, Invocation-level execution binding and
exact compatibility (Spec 5.1/5.2/16.2/16.3, Task 3).

Covers the brief Step 1 assertions: Case changes affect new Runs only,
compatible later Invocations may continue the same Run, and incompatible
Workflow/Prompt/Schema/Runtime configuration fails deterministically — with
no fuzzy compatibility anywhere.
"""

import hashlib
import json

import pytest

from ai_native_workbench.research.runtime import (
    CaseBinding,
    CompatibilityIdentity,
    ExecutionBinding,
    RunRecord,
    RunState,
    RuntimeContractError,
)
from ai_native_workbench.research.runtime.binding import (
    CaseLoadError,
    ConfigurationItem,
    ExecutionConfiguration,
    ResearchCase,
    assert_compatible,
    freeze_case_binding,
    freeze_execution_binding,
    load_research_case,
)
from ai_native_workbench.research.runtime.store import FileSystemRuntimeStore

CHARTER_FILE = "00-research-charter.md"
URLS_FILE = "inputs/urls.yaml"
CASE_ID = "case-1"
RUN_ID = "run-1"

CHARTER_TEXT = (
    "# Research Charter\n\nApproved charter for binding tests — 批准的执行宪章。\n"
)
URLS_TEXT = "- id: src-1\n  url: https://example.com/source\n"


# ---------------------------------------------------------------------------
# Shared fixtures/helpers (per-file convention: no cross-test imports)
# ---------------------------------------------------------------------------


def make_case_dir(
    tmp_path,
    case_id: str = CASE_ID,
    charter_text: str = CHARTER_TEXT,
    urls_text: str = URLS_TEXT,
):
    """Create the approved Case package layout under tmp_path/cases/<case_id>."""
    case_dir = tmp_path / "cases" / case_id
    inputs = case_dir / "inputs"
    inputs.mkdir(parents=True)
    (case_dir / CHARTER_FILE).write_text(charter_text, encoding="utf-8")
    (inputs / "urls.yaml").write_text(urls_text, encoding="utf-8")
    return case_dir


def sha256_digest(text: str) -> str:
    """Independent reference digest (pins the documented digest scheme)."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_case(**overrides) -> ResearchCase:
    defaults = dict(
        case_id=CASE_ID,
        charter_identity=CHARTER_FILE,
        charter_digest=sha256_digest(CHARTER_TEXT),
        charter_text=CHARTER_TEXT,
        source_declaration_identity=URLS_FILE,
        source_declaration_digest=sha256_digest(URLS_TEXT),
        source_declaration_text=URLS_TEXT,
    )
    defaults.update(overrides)
    return ResearchCase(**defaults)


def make_run(case_binding: CaseBinding, run_id: str = RUN_ID) -> RunRecord:
    return RunRecord(
        run_id=run_id,
        case_id=case_binding.case_id,
        case_binding=case_binding,
        state=RunState.CREATED,
        cumulative_execution_scope=(),
        current_invocation_id=None,
        completion_reason=None,
    )


def make_item(
    identity: str, version: str = "1", content: str = "instructions"
) -> ConfigurationItem:
    return ConfigurationItem(identity=identity, version=version, content=content)


def make_config(**overrides) -> ExecutionConfiguration:
    defaults = dict(
        workflow_identity="research-standard",
        workflow_version="1.0.0",
        runtime_configuration_identity="runtime-config-001",
        prompts=(make_item("prompt-r1"),),
        schemas=(make_item("schema-r1"),),
    )
    defaults.update(overrides)
    return ExecutionConfiguration(**defaults)


def make_identity(**overrides) -> CompatibilityIdentity:
    defaults = dict(
        workflow_identity="research-standard",
        workflow_version="1.0.0",
        step_identity="R2",
        step_version="1",
        runtime_configuration_identity="runtime-config-001",
    )
    defaults.update(overrides)
    return CompatibilityIdentity(**defaults)


# ---------------------------------------------------------------------------
# Case loading and Run-level Case binding (brief Step 1)
# ---------------------------------------------------------------------------


def test_load_research_case_captures_identity_and_digests(tmp_path):
    case_dir = make_case_dir(tmp_path)
    case = load_research_case(case_dir)
    assert case.case_id == CASE_ID
    assert case.charter_identity == CHARTER_FILE
    assert case.charter_digest == sha256_digest(CHARTER_TEXT)
    assert case.charter_text == CHARTER_TEXT
    assert case.source_declaration_identity == URLS_FILE
    assert case.source_declaration_digest == sha256_digest(URLS_TEXT)
    assert case.source_declaration_text == URLS_TEXT


def test_loading_same_case_is_deterministic(tmp_path):
    case_dir = make_case_dir(tmp_path)
    assert load_research_case(case_dir) == load_research_case(case_dir)


def test_case_change_affects_new_runs_only(tmp_path):
    """Ruling 3/16.1: a Case edit is visible only to Runs frozen afterwards."""
    case_dir = make_case_dir(tmp_path)
    store = FileSystemRuntimeStore(tmp_path / "runtime-store")

    first_binding = freeze_case_binding(load_research_case(case_dir))
    store.create_run(make_run(first_binding))

    # The approved source declarations change on disk (identity unchanged,
    # content digest changes).
    changed_urls = URLS_TEXT + "- id: src-2\n  url: https://example.org/other\n"
    (case_dir / "inputs" / "urls.yaml").write_text(changed_urls, encoding="utf-8")

    second_binding = freeze_case_binding(load_research_case(case_dir))
    assert second_binding != first_binding
    assert second_binding.source_declaration_identity == URLS_FILE
    assert second_binding.source_declaration_digest == sha256_digest(changed_urls)

    # A new Run freezes the changed declarations ...
    store.create_run(make_run(second_binding, run_id="run-2"))
    assert store.load_run("run-2").case_binding == second_binding
    # ... while the first Run keeps the declarations frozen at its creation.
    assert store.load_run(RUN_ID).case_binding == first_binding


def test_charter_change_changes_only_the_charter_digest(tmp_path):
    case_dir = make_case_dir(tmp_path, charter_text="v1 charter\n")
    before = freeze_case_binding(load_research_case(case_dir))
    (case_dir / CHARTER_FILE).write_text("v2 charter\n", encoding="utf-8")
    after = freeze_case_binding(load_research_case(case_dir))
    assert after.charter_digest == sha256_digest("v2 charter\n")
    assert after.charter_digest != before.charter_digest
    assert after.source_declaration_digest == before.source_declaration_digest


def test_freeze_case_binding_is_a_pure_mapping(tmp_path):
    case_dir = make_case_dir(tmp_path)
    binding = freeze_case_binding(load_research_case(case_dir))
    assert binding == CaseBinding(
        case_id=CASE_ID,
        charter_identity=CHARTER_FILE,
        charter_digest=sha256_digest(CHARTER_TEXT),
        source_declaration_identity=URLS_FILE,
        source_declaration_digest=sha256_digest(URLS_TEXT),
    )


def test_freeze_case_binding_rejects_non_case():
    with pytest.raises(RuntimeContractError):
        freeze_case_binding(object())  # type: ignore[arg-type]


def test_research_case_rejects_blank_fields():
    for name in (
        "case_id",
        "charter_identity",
        "charter_digest",
        "charter_text",
        "source_declaration_identity",
        "source_declaration_digest",
        "source_declaration_text",
    ):
        with pytest.raises(RuntimeContractError, match=name):
            make_case(**{name: "   "})


# ---------------------------------------------------------------------------
# Case package loader failures (explicit, never silent)
# ---------------------------------------------------------------------------


def test_loader_missing_charter_fails(tmp_path):
    case_dir = make_case_dir(tmp_path)
    (case_dir / CHARTER_FILE).unlink()
    with pytest.raises(CaseLoadError):
        load_research_case(case_dir)


def test_loader_missing_urls_yaml_fails(tmp_path):
    case_dir = make_case_dir(tmp_path)
    (case_dir / "inputs" / "urls.yaml").unlink()
    with pytest.raises(CaseLoadError):
        load_research_case(case_dir)


def test_loader_empty_charter_fails(tmp_path):
    case_dir = make_case_dir(tmp_path, charter_text="   \n")
    with pytest.raises(CaseLoadError):
        load_research_case(case_dir)


def test_loader_empty_urls_yaml_fails(tmp_path):
    case_dir = make_case_dir(tmp_path, urls_text="")
    with pytest.raises(CaseLoadError):
        load_research_case(case_dir)


def test_loader_unknown_directory_fails(tmp_path):
    with pytest.raises(CaseLoadError):
        load_research_case(tmp_path / "cases" / "ghost-case")


def test_loader_non_directory_path_fails(tmp_path):
    case_dir = make_case_dir(tmp_path)
    with pytest.raises(CaseLoadError):
        load_research_case(case_dir / CHARTER_FILE)


def test_loader_non_utf8_charter_fails(tmp_path):
    case_dir = tmp_path / "cases" / CASE_ID
    inputs = case_dir / "inputs"
    inputs.mkdir(parents=True)
    (case_dir / CHARTER_FILE).write_bytes(b"\xff\xfe not utf-8")
    (inputs / "urls.yaml").write_text(URLS_TEXT, encoding="utf-8")
    with pytest.raises(CaseLoadError):
        load_research_case(case_dir)


def test_case_load_error_is_a_contract_error(tmp_path):
    with pytest.raises(CaseLoadError) as excinfo:
        load_research_case(tmp_path / "cases" / "ghost-case")
    assert isinstance(excinfo.value, RuntimeContractError)


# ---------------------------------------------------------------------------
# Execution configuration and Invocation-level binding (brief Step 1)
# ---------------------------------------------------------------------------


def test_same_execution_configuration_freezes_equally():
    # Compatible later Invocations may continue the same Run only when the
    # frozen execution configuration is identical (Spec 16.2).
    assert freeze_execution_binding(make_config()) == freeze_execution_binding(
        make_config()
    )


def test_freeze_execution_binding_maps_identities_to_digests():
    binding = freeze_execution_binding(make_config())
    assert binding == ExecutionBinding(
        workflow_identity="research-standard",
        workflow_version="1.0.0",
        runtime_configuration_identity="runtime-config-001",
        prompts={"prompt-r1": sha256_digest_of_item(make_item("prompt-r1"))},
        schemas={"schema-r1": sha256_digest_of_item(make_item("schema-r1"))},
    )


def sha256_digest_of_item(item: ConfigurationItem) -> str:
    text = json.dumps(
        {"identity": item.identity, "version": item.version, "content": item.content},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_configuration_digests_are_version_and_content_sensitive():
    base = freeze_execution_binding(make_config()).prompts["prompt-r1"]
    new_version = freeze_execution_binding(
        make_config(prompts=(make_item("prompt-r1", version="2"),))
    ).prompts["prompt-r1"]
    new_content = freeze_execution_binding(
        make_config(prompts=(make_item("prompt-r1", content="other"),))
    ).prompts["prompt-r1"]
    new_identity = freeze_execution_binding(
        make_config(prompts=(make_item("prompt-r2"),))
    ).prompts["prompt-r2"]
    assert base != new_version
    assert base != new_content
    assert base != new_identity
    assert len(base) == len("sha256:" + "a" * 64)


def test_freezes_without_prompts_or_schemas_are_allowed():
    binding = freeze_execution_binding(make_config(prompts=(), schemas=()))
    assert binding.prompts == {}
    assert binding.schemas == {}


def test_execution_configuration_validation():
    with pytest.raises(RuntimeContractError):
        make_config(workflow_identity="")
    with pytest.raises(RuntimeContractError):
        make_config(workflow_version="  ")
    with pytest.raises(RuntimeContractError):
        make_config(runtime_configuration_identity="")
    with pytest.raises(RuntimeContractError):
        make_config(prompts=(make_item("prompt-r1"), make_item("prompt-r1")))
    with pytest.raises(RuntimeContractError):
        make_config(prompts=("not-an-item",))  # type: ignore[assignment]
    with pytest.raises(RuntimeContractError):
        make_config(schemas=(make_item(""),))


def test_freeze_execution_binding_requires_configuration():
    with pytest.raises(RuntimeContractError):
        freeze_execution_binding(object())  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Exact compatibility (brief Step 3: no fuzzy or semantic checks)
# ---------------------------------------------------------------------------


def test_compatible_identities_pass():
    assert assert_compatible(make_identity(), make_identity()) is None


@pytest.mark.parametrize(
    "dimension, override",
    [
        ("workflow_identity", "research-standard-2"),
        ("workflow_version", "1.1.0"),
        ("step_identity", "R3"),
        ("step_version", "2"),
        ("runtime_configuration_identity", "runtime-config-002"),
        ("prompt_identity", None),
        ("prompt_version", "9"),
        ("schema_identity", "schema-v2"),
        ("schema_version", "2"),
    ],
)
def test_identity_mismatch_fails_and_names_the_dimension(dimension, override):
    expected = make_identity(
        prompt_identity="prompt-r2",
        prompt_version="1",
        schema_identity="schema-r2",
        schema_version="1",
    )
    # Only the dimension under test differs from the expected identity; the
    # optional pairs vary as both-or-neither so the mismatch lands on the
    # intended dimension (dimension order is prompt before schema).
    kwargs = dict(
        prompt_identity="prompt-r2",
        prompt_version="1",
        schema_identity="schema-r2",
        schema_version="1",
    )
    if dimension == "prompt_identity":
        kwargs.pop("prompt_identity")
        kwargs.pop("prompt_version")
    elif dimension == "prompt_version":
        kwargs["prompt_version"] = "9"
    elif dimension == "schema_identity":
        kwargs.pop("schema_identity")
        kwargs.pop("schema_version")
    elif dimension == "schema_version":
        kwargs["schema_version"] = "2"
    else:
        kwargs[dimension] = override
    actual = make_identity(**kwargs)
    with pytest.raises(RuntimeContractError) as excinfo:
        assert_compatible(expected, actual)
    assert dimension in str(excinfo.value)


def test_present_vs_absent_prompt_pair_is_incompatible():
    with_prompt = make_identity(
        prompt_identity="prompt-r2", prompt_version="1"
    )
    without_prompt = make_identity()
    with pytest.raises(RuntimeContractError):
        assert_compatible(with_prompt, without_prompt)
    with pytest.raises(RuntimeContractError):
        assert_compatible(without_prompt, with_prompt)


def test_incompatible_workflow_version_fails_deterministically():
    # Incompatible configurations fail the same way on every call.
    expected = make_identity()
    actual = make_identity(workflow_version="2.0.0")
    with pytest.raises(RuntimeContractError):
        assert_compatible(expected, actual)
    with pytest.raises(RuntimeContractError):
        assert_compatible(expected, actual)


def test_assert_compatible_rejects_non_identities():
    with pytest.raises(RuntimeContractError):
        assert_compatible(make_identity(), object())  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError):
        assert_compatible(None, make_identity())  # type: ignore[arg-type]
