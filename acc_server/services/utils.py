from typing import Tuple


def try_parse_int(number: str, on_error: int = 0) -> Tuple[int, bool]:
    try:
        value = int(number)
        return value, True
    except ValueError:
        return on_error, False
