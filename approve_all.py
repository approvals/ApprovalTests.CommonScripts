import pathlib
from typing import Callable

SCRIPT_DIR = pathlib.Path(__file__).parent

APPROVAL_TESTS_TEMP_DIRECTORY: str = ".approval_tests_temp"


def load_failed_comparisons() -> list[str]:
    return (SCRIPT_DIR / ".failed_comparison.log").read_text().splitlines()


def move(a: str, b: str) -> None:
    pathlib.Path(a).replace(b)


def approve_all(
    failed_comparisons: list[str],
    mover: Callable[[str, str], None] = move,
) -> None:
    for line in failed_comparisons:
        a, b = line.split(" -> ")
        mover(a, b)


if __name__ == "__main__":
    approve_all(load_failed_comparisons())
