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
    system_out: Callable[[str], None] = print
) -> None:
    failures = []
    successes = []
    failed_comparisons = failed_comparison_loader()
    for line in failed_comparisons:
        from_, to = line.split(" -> ") # rename these
        try:
            mover(from_, to)
            successes.append(pathlib.Path(to).name)
        except Exception as e:
            failures.append((pathlib.Path(to).name, str(e)))
    report(failed_comparisons, failures, successes, system_out)


def report(failed_comparisons, failures, successes, system_out):
    if len(failed_comparisons) == 1:
        system_out("Mismatched file found.")
    elif len(failed_comparisons) == 0:
        system_out("No mismatched files found.")

    else:
        system_out(f"Mismatched files found.")
    if len(successes):
        system_out("Updating:")
        for approved_file in successes:
            system_out(f"  - {approved_file}")
    if len(failures):
        system_out("Failed to update:")
        for approved_file, reason in failures:
            system_out(f"  - {approved_file}")
            system_out(f"    Reason: {reason}")
    system_out("")
    if len(successes) == 1:
        system_out(f"Approved 1 file.")
    else:
        system_out(f"Approved {len(successes)} files.")


if __name__ == "__main__":
    approve_all()
