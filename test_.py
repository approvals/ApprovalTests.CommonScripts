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


def test__canary():
    with tempfile.TemporaryDirectory(prefix="ApprovalTests.CommonScripts-") as _sandbox:
        sandbox = pathlib.Path(_sandbox)

        a = sandbox / "a"
        b = sandbox / "b"
        a.write_text("a contents!")
        b.write_text("b contents!")
        (sandbox / ".approvals_temp/.failed_comparison.log").write_text("a -> b")

        execute_the_script(cwd=sandbox)

        a_contents = a.read_text()
        b_contents = b.read_text()
    assert b_contents == a_contents
