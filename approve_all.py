import pathlib
from typing import Callable, List

SCRIPT_DIR = pathlib.Path(__file__).parent

APPROVAL_TESTS_TEMP_DIRECTORY: str = ".approval_tests_temp"


def load_failed_comparisons() -> List[str]:
    return (SCRIPT_DIR / ".failed_comparison.log").read_text().splitlines()


def move(a: str, b: str) -> None:
    pathlib.Path(a).replace(b)


def approve_all(
    failed_comparison_loader: Callable[[], List[str]] = load_failed_comparisons,
    mover: Callable[[str, str], None] = move,
) -> None:
    for line in failed_comparison_loader():
        a, b = line.split(" -> ")
        try:
            mover(a, b)
        except Exception :
            pass



if __name__ == "__main__":
    approve_all()
