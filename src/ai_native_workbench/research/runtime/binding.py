"""Run-level Case binding and Invocation-level execution binding (Spec 5.1/16).

Freezing separates the *Case package as it exists on disk right now*
(``ResearchCase``, produced by ``load_research_case`` from the approved
Case package) from the *Case frozen into a Run at creation*
(``CaseBinding``, produced by ``freeze_case_binding``). Later modifications
to the Case never mutate a Run bound through a frozen record (Spec 16.1);
identity/digest strings are deliberately deterministic and readable.

Identity and digest schemes (documented contracts, pinned by tests):

- The approved Case package follows the conventional v1 layout (architecture
  section 4.1): ``<case_dir>/00-research-charter.md`` and
  ``<case_dir>/inputs/urls.yaml``.
- ``case_id`` is the name of the approved Case directory.
- A declaration's *identity* is its conventional case-relative filename
  (``00-research-charter.md`` / ``inputs/urls.yaml``): stable across content
  revisions, case-scoped by the record's ``case_id``.
- A declaration's *digest* is ``sha256:<64hex>`` over the file's raw UTF-8
  bytes as approved, so any content change produces a new digest while the
  identity stays put — exactly what "Case changes affect new Runs only"
  needs at Run creation.
- ``ResearchCase`` additionally freezes both file texts so consumers
  (e.g. Task 5 declaration parsing) operate on the same content that was
  digested, never on a re-read of mutable disk.

Execution binding (Spec 16.2) mirrors the ``ExecutionBinding`` record: the
Invocation freezes workflow identity/version, the runtime configuration
identity, and prompt/schema identity->digest maps computed over versioned
``ConfigurationItem`` contents. Item digests cover the deterministic JSON
of ``{identity, version, content}``, so any prompt/schema revision (content
or version) changes the frozen digest.

Compatibility is exact (Spec 16.3): ``assert_compatible`` compares every
dimension of the ``CompatibilityIdentity`` record and raises on the first
mismatch. There is no fuzzy or semantic similarity check in v1.
"""

from dataclasses import dataclass
from pathlib import Path

from .digests import payload_digest, sha256_digest
from .domain import (
    CaseBinding,
    CompatibilityIdentity,
    ExecutionBinding,
    RuntimeContractError,
)

CHARTER_FILE = "00-research-charter.md"
"""Conventional filename of the approved Research Charter (architecture 4.1)."""

SOURCE_DECLARATION_FILE = "inputs/urls.yaml"
"""Conventional case-relative path of the approved source declarations."""

_IDENTITY_FIELDS = (
    "case_id",
    "charter_identity",
    "charter_digest",
    "charter_text",
    "source_declaration_identity",
    "source_declaration_digest",
    "source_declaration_text",
)


def _require_text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeContractError(f"{name} must be a non-empty string.")


class CaseLoadError(RuntimeContractError):
    """Raised when the approved Case package cannot be loaded or frozen.

    A missing, unreadable or non-UTF-8 charter / source declaration file and
    an empty declaration are all explicit load failures — the Runtime never
    binds a Run to a Case package it cannot prove it read.
    """


@dataclass(frozen=True)
class ResearchCase:
    """The approved Case package as loaded from disk (Ruling 3).

    ``charter_text`` / ``source_declaration_text`` freeze the exact file
    contents that the digests cover. Identities are the conventional
    declaration filenames; see the module docstring for the scheme.
    """

    case_id: str
    charter_identity: str
    charter_digest: str
    charter_text: str
    source_declaration_identity: str
    source_declaration_digest: str
    source_declaration_text: str

    def __post_init__(self) -> None:
        for name in _IDENTITY_FIELDS:
            _require_text(getattr(self, name), name)


@dataclass(frozen=True)
class ConfigurationItem:
    """One versioned, content-bearing configuration object (Prompt or Schema).

    ``content`` is the deterministic serialization the digest is computed
    over; identity and version are included so a digest change is
    attributable to exactly which revision drifted.
    """

    identity: str
    version: str
    content: str

    def __post_init__(self) -> None:
        for name in ("identity", "version", "content"):
            _require_text(getattr(self, name), name)


@dataclass(frozen=True)
class ExecutionConfiguration:
    """Invocation-level execution inputs before freezing (Spec 16.2).

    Mirrors the ``ExecutionBinding`` record shape so freezing is a pure
    1:1 mapping plus digest computation: workflow identity/version and the
    runtime configuration identity pass through; each prompt/schema item is
    mapped to ``identity -> sha256_digest({identity, version, content})``.
    """

    workflow_identity: str
    workflow_version: str
    runtime_configuration_identity: str
    prompts: tuple[ConfigurationItem, ...] = ()
    schemas: tuple[ConfigurationItem, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "workflow_identity",
            "workflow_version",
            "runtime_configuration_identity",
        ):
            _require_text(getattr(self, name), name)
        for section in ("prompts", "schemas"):
            items = getattr(self, section)
            if not isinstance(items, tuple) or not all(
                isinstance(item, ConfigurationItem) for item in items
            ):
                raise RuntimeContractError(
                    f"{section} must be a tuple of ConfigurationItem records."
                )
            seen: set[str] = set()
            for item in items:
                if item.identity in seen:
                    raise RuntimeContractError(
                        f"{section} declares duplicate identity {item.identity!r}."
                    )
                seen.add(item.identity)


def load_research_case(case_dir: str | Path) -> ResearchCase:
    """Load the approved Case package at *case_dir* (see module docstring).

    Raises CaseLoadError when the package is missing, follows an unknown
    layout, or holds an unreadable/empty charter or source declaration.
    """
    root = Path(case_dir)
    if not root.is_dir():
        raise CaseLoadError(
            f"case directory {str(root)!r} does not exist or is not a directory."
        )
    case_id = root.name
    if not case_id.strip() or case_id in (".", "/"):
        raise CaseLoadError(f"cannot derive a case_id from directory {str(root)!r}.")

    charter_path = root / CHARTER_FILE
    urls_path = root / SOURCE_DECLARATION_FILE
    charter = _read_declaration(charter_path, CHARTER_FILE)
    urls = _read_declaration(urls_path, SOURCE_DECLARATION_FILE)
    return ResearchCase(
        case_id=case_id,
        charter_identity=CHARTER_FILE,
        charter_digest=sha256_digest(charter[0]),
        charter_text=charter[0],
        source_declaration_identity=SOURCE_DECLARATION_FILE,
        source_declaration_digest=sha256_digest(urls[0]),
        source_declaration_text=urls[0],
    )


def _read_declaration(path: Path, label: str) -> tuple[str, bytes]:
    """Read *path* as UTF-8 text; returns (text, raw bytes)."""
    if not path.is_file():
        raise CaseLoadError(
            f"case package is missing its {label} file at {str(path)!r}."
        )
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CaseLoadError(
            f"cannot read {label} file {str(path)!r}: {exc}"
        ) from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CaseLoadError(
            f"{label} file {str(path)!r} is not valid UTF-8 text."
        ) from exc
    if not text.strip():
        raise CaseLoadError(f"{label} file {str(path)!r} is empty.")
    return text, raw


def freeze_case_binding(case: ResearchCase) -> CaseBinding:
    """Freeze the loaded Case into the immutable Run-level CaseBinding.

    The mapping is pure 1:1 (contents are not part of the binding); freezing
    marks the moment the Case definition becomes immutable for a Run.
    """
    if not isinstance(case, ResearchCase):
        raise RuntimeContractError(
            f"freeze_case_binding requires a ResearchCase (got {case!r})."
        )
    return CaseBinding(
        case_id=case.case_id,
        charter_identity=case.charter_identity,
        charter_digest=case.charter_digest,
        source_declaration_identity=case.source_declaration_identity,
        source_declaration_digest=case.source_declaration_digest,
    )


def freeze_execution_binding(config: ExecutionConfiguration) -> ExecutionBinding:
    """Freeze the invocation-level execution configuration (Spec 16.2)."""
    if not isinstance(config, ExecutionConfiguration):
        raise RuntimeContractError(
            "freeze_execution_binding requires an ExecutionConfiguration "
            f"(got {config!r})."
        )
    return ExecutionBinding(
        workflow_identity=config.workflow_identity,
        workflow_version=config.workflow_version,
        runtime_configuration_identity=config.runtime_configuration_identity,
        prompts={item.identity: _item_digest(item) for item in config.prompts},
        schemas={item.identity: _item_digest(item) for item in config.schemas},
    )


def _item_digest(item: ConfigurationItem) -> str:
    return payload_digest(
        {"identity": item.identity, "version": item.version, "content": item.content}
    )


_COMPATIBILITY_DIMENSIONS = (
    "workflow_identity",
    "workflow_version",
    "step_identity",
    "step_version",
    "runtime_configuration_identity",
    "prompt_identity",
    "prompt_version",
    "schema_identity",
    "schema_version",
)


def assert_compatible(
    expected: CompatibilityIdentity, actual: CompatibilityIdentity
) -> None:
    """Require exact identity compatibility between *expected* and *actual*.

    Every dimension of the CompatibilityIdentity tuple must match exactly;
    optional prompt/schema pairs must be both present with equal values or
    both absent (both-or-neither pairs). Raises RuntimeContractError naming
    the first mismatching dimension; no fuzzy or semantic check exists.
    """
    if not isinstance(expected, CompatibilityIdentity) or not isinstance(
        actual, CompatibilityIdentity
    ):
        raise RuntimeContractError(
            "assert_compatible requires CompatibilityIdentity records "
            f"(expected {expected!r}, actual {actual!r})."
        )
    for dimension in _COMPATIBILITY_DIMENSIONS:
        expected_value = getattr(expected, dimension)
        actual_value = getattr(actual, dimension)
        if expected_value != actual_value:
            raise RuntimeContractError(
                f"compatibility mismatch on {dimension}: expected "
                f"{expected_value!r}, actual {actual_value!r}."
            )
