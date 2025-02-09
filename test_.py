import pathlib
import tempfile


# Not really a test, but a way to ensure that the tests are actually running in CI and didn't get skipped silently
def test__ensure_tests_are_actually_running():
    pathlib.Path(__file__).parent.joinpath("semaphore").touch()


def execute_the_script(param):
    pass



def test__canary():
    with tempfile.TemporaryDirectory(prefix="ApprovalTests.CommonScripts-") as temp_dir:
        pathlib.Path(temp_dir, "a").write_text("a contents!")
        pathlib.Path(temp_dir, "b").write_text("b contents!")
        pathlib.Path(temp_dir, "example_failed_comparison.log").write_text("a->b")

        execute_the_script("example_failed_comparison.log")

        # compare the first file to the second file
        a_contents = pathlib.Path(temp_dir, "a").read_text()
        b_contents = pathlib.Path(temp_dir, "b").read_text()
    assert b_contents == a_contents

