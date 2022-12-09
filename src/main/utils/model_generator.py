import json

from typing import cast
from pathlib import Path
from datamodel_code_generator import InputFileType, generate, LiteralType


def generate_model(schema: dict, output_path: str):
    path = Path(output_path)
    generate(
        json.dumps(schema, ensure_ascii=False), input_file_type=InputFileType.JsonSchema, output=path,
        field_constraints=True, enum_field_as_literal=cast(LiteralType, "all")
    )
    return output_path
