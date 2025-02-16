import pathlib
import subprocess
import sys
import tempfile
from typing import Callable


def execute_the_script(cwd: pathlib.Path):
    subprocess.run(
        [
            sys.executable,
            "approve_all.py",
        ],
        cwd=cwd,
        text=True,
        check=True,
    )


def ptest__end_to_end_test():
    with tempfile.TemporaryDirectory(prefix="ApprovalTests.CommonScripts-") as _sandbox:
        sandbox = pathlib.Path(_sandbox)

        a = sandbox / "a"
        b = sandbox / "b"
        a.write_text("a contents!")
        b.write_text("b contents!")
        (sandbox / ".approvals_temp/.failed_comparison.log").write_text("a -> b")

        execute_the_script(cwd=sandbox)

        b_contents = b.read_text()
    assert b_contents == "a contents"
    assert not a.exists()


def load_failed_comparisons() -> list[str]:
    return pathlib.Path("./.failed_comparison.log").read_text().splitlines()


def move(a: str, b: str) -> None:
    pathlib.Path(a).replace(b)


def approve_all(failed_comparison_loader: Callable[[],list[str]] = load_failed_comparisons, mover: Callable[[str,str], None] = move) -> None:
    for line in failed_comparison_loader():
        a, b = line.split(" -> ")
        mover(a, b)


def test__approve_all__with_loader_and_saver():
    def failed_comparison_loader():
        return ["a.received.txt -> a.approved.txt",
                "b.received.txt -> b.approved.txt",]

    moves = []

    def mover(a, b):
        nonlocal moves
        moves.append( f"{a} -> {b}")

    approve_all(failed_comparison_loader, mover)

    assert moves == failed_comparison_loader()
