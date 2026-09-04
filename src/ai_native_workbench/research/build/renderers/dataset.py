"""Deterministic serializers for dataset projections."""

import csv
import json
from collections.abc import Mapping
from io import StringIO

from ..errors import BuildValidationError
from ..projection import DatasetProjection


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _require_projection(projection: object) -> DatasetProjection:
    if not isinstance(projection, DatasetProjection):
        raise BuildValidationError("Dataset renderer requires a DatasetProjection.")
    return projection


def render_dataset_json(projection: DatasetProjection) -> str:
    projection = _require_projection(projection)
    payload = {"projection_version": projection.version, "rows": [{"ref": str(row.ref), "object_type": row.object_type, "logical_id": row.logical_id, "fields": _plain(row.fields)} for row in projection.rows]}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def render_dataset_csv(projection: DatasetProjection) -> str:
    projection = _require_projection(projection)
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=["ref", "object_type", "logical_id", "fields_json"], lineterminator="\n")
    writer.writeheader()
    for row in projection.rows:
        writer.writerow({"ref": str(row.ref), "object_type": row.object_type, "logical_id": row.logical_id, "fields_json": json.dumps(_plain(row.fields), ensure_ascii=False, sort_keys=True, separators=(",", ":"))})
    return output.getvalue()
