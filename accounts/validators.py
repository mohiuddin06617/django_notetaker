import re
from django.core.exceptions import ValidationError


def validate_username(username: str) -> None:
    """Validates a given username.

    Args:
        username: The username to validate.

    Raises:
        ValidationError: If the username is not a str, doesn't meet
            the length requirements or is not in
            the correct format.
    """
    if not isinstance(username, str):
        raise ValidationError("Bad username type.")
    if 3 > len(username) or len(username) > 150:
        raise ValidationError("Username should contain less than 150 symbols \
                    and more than 2.")
    # if not re.fullmatch(r"^@([a-zA-Z]+\.[a-zA-Z]+\.?)+[a-zA-Z]+\d*$", username):
    if not re.fullmatch(r"^(?!.*\.\.)(?!^\d.*\.)(?!.*\.$)[a-zA-Z\d.]+$", username):
        raise ValidationError(
            "Username can't start or end with a dot. Two dots can't be \
            next to each other. Digits can be added only at the end."

        )


def validate_full_name(full_name: str) -> None:
    """Validates a given full name.

    Args:
        full_name: The full name to validate.

    Raises:
        ValidationError: If the full name is empty, contains non-alphabetic
            characters, or has more than three words.
    """
    if not full_name:
        raise ValidationError("Full name can't be empty.")
    if not full_name.replace(" ", "").isalpha():
        raise ValidationError("Full name should contain only letters.")
    if len(full_name.split()) > 3:
        raise ValidationError("Full name should contain less than 3 words.")
