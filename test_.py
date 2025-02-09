import pathlib
import subprocess
import sys
import tempfile


# Not really a test, but a way to ensure that the tests are actually running in CI and didn't get skipped silently
def test__ensure_tests_are_actually_running():
    pathlib.Path(__file__).parent.joinpath("semaphore").touch()


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


def test__end_to_end_test():
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

def load_failed_comparisons():
    return pathlib.Path(".approvals_temp/.failed_comparison.log").read_text().splitlines()

def move(a, b):
    pathlib.Path(a).replace(b)


def approve_all(failed_comparison_loader = load_failed_comparisons, mover = move):
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
