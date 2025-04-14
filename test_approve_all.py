import os
import pathlib
import subprocess
import sys
import tempfile
import shutil
from typing import List, Callable

from approve_all import approve_all
from approvaltests import verify


def execute_the_script(script: pathlib.Path) -> None:
    subprocess.run(
        [sys.executable, script],
        text=True,
        check=True,
    )


def test__end_to_end_test() -> None:
    script = ".approval_tests_temp/approve_all.py"
    with tempfile.TemporaryDirectory(prefix="ApprovalTests.CommonScripts-") as _sandbox:
        sandbox = copy_template_dir(_sandbox, script)

        received_text = (sandbox / "a.received.txt").read_text()
        execute_the_script(sandbox / script)
        approved_text = (sandbox / "a.approved.txt").read_text()
        assert received_text == approved_text


def copy_template_dir(_sandbox: str, script: str) -> pathlib.Path:
    shutil.copytree(pathlib.Path("template_folder"), _sandbox, dirs_exist_ok=True)
    sandbox = pathlib.Path(_sandbox)
    render_template(sandbox, ".approval_tests_temp/.failed_comparison.log.template")
    script_path = sandbox / script
    shutil.copy(script_path.name, script_path)
    return sandbox


def render_template(root_dir: pathlib.Path, template_path_: str) -> None:
    template_path = root_dir / template_path_
    log_path = template_path.with_name(template_path.name.replace(".template", ""))
    content = template_path.read_text()
    content = content.replace("{root}", str(root_dir) + os.sep)
    log_path.write_text(content)


def test__console_output() -> None:
    verify_approve_all(
        [
            "a.received.txt -> a.approved.txt",
            "b.received.txt -> /text/b.approved.txt",
            "bad.received.txt -> /text/bad.approved.txt",
        ]
    )


def test__one_case() -> None:
    verify_approve_all(
        files=[
            "a.received.txt -> a.approved.txt",
        ]
    )


def test__zero_case() -> None:
    verify_approve_all([])


def verify_approve_all(files: List[str]) -> None:
    def failed_comparison_loader() -> List[str]:
        return files

    result = ""

    def system_out(text: str) -> None:
        nonlocal result
        result += text + "\n"

    def mover(from_: str, to: str) -> None:
        if "bad" in from_:
            raise Exception("Failed to move file")

    approve_all(failed_comparison_loader, mover, system_out)
    verify(result)
