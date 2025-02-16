import pathlib
from typing import Callable


def load_failed_comparisons() -> list[str]:
    return pathlib.Path("./.failed_comparison.log").read_text().splitlines()


def move(a: str, b: str) -> None:
    pathlib.Path(a).replace(b)


def approve_all(failed_comparison_loader: Callable[[],list[str]] = load_failed_comparisons, mover: Callable[[str,str], None] = move) -> None:
    for line in failed_comparison_loader():
        a, b = line.split(" -> ")
        mover(a, b)
