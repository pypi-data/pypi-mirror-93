from typing import List
from uuid import UUID

from threedi_cmd_statistics.validators import ValidationError


def validate_organisations(organisations: List[str]):
    if len(organisations) == 1:
        organisation = organisations[0]
        if organisation.lower() == "all":
            return
        if not validate_uuid4(organisation):
            raise ValidationError(f"organisation uuid {organisation} is not valid (not a uuid4 hex string")

    for organisation in organisations:
        if not validate_uuid4(organisation):
            raise ValidationError(f"organisation uuid {organisation} is not valid (not a uuid4 hex string")


def validate_uuid4(uuid_string) -> bool:
    """
    from https://gist.github.com/ShawnMilo/7777304

    Validate that a UUID string is in
    fact a valid uuid4.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False
    except Exception:
        return False

    # If the uuid_string is a valid hex code,
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a
    # valid uuid4. This is bad for validation purposes.

    return val.hex == uuid_string
