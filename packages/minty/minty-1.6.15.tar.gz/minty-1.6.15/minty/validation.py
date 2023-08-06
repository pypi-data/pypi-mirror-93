# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import json
import statsd
from .exceptions import ValidationError
from functools import wraps
from jsonpointer import JsonPointer
from jsonschema import Draft7Validator, draft7_format_checker
from typing import Optional
from uuid import UUID

_format_checker = draft7_format_checker


@_format_checker.checks("uuid", raises=ValueError)
def is_uuid(instance):
    return UUID(hex=str(instance))


def validate_with(schema_data: Optional[bytes]):
    """Ensure the decorated function is called with valid arguments

    :param schema_data: The JSONSchema to validate against.
        Should be UTF-8-encoded JSON bytes.
    :type schema_data: bytes
    :return: Decorator for validating function arguments against `schema`
    """
    assert schema_data is not None, "No validation JSON found"

    schema = json.loads(schema_data.decode("utf-8"))

    def validity_wrapper(f):
        validator = Draft7Validator(
            schema=schema, format_checker=_format_checker
        )

        @wraps(f)
        def check_validity(*args, **kwargs):
            with statsd.Timer(__name__).time("check_validity"):
                errors = []
                for error in validator.iter_errors(instance=kwargs):
                    error_pointer = JsonPointer.from_parts(error.absolute_path)

                    errors.append(
                        {
                            "context": error.validator,
                            "message": error.message,
                            "cause": str(error.cause) if error.cause else None,
                            "property": error_pointer.path,
                        }
                    )

                if len(errors):
                    raise ValidationError(errors)

            return f(*args, **kwargs)

        return check_validity

    return validity_wrapper
