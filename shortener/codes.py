import secrets
import string
from typing import Final

CODE_CHARACTERS: Final[str] = string.ascii_letters + string.digits
CODE_LENGTH: Final[int] = 7


def generate_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(CODE_CHARACTERS) for _ in range(length))


def is_valid_code(code: str) -> bool:
    return len(code) == CODE_LENGTH and all(char in CODE_CHARACTERS for char in code)
