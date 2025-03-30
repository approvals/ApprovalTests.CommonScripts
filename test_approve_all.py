import os
import pathlib
import subprocess
import sys
import tempfile
import shutil

from approve_all import approve_all
from approvaltests import verify

def execute_the_script(script: pathlib.Path):
    subprocess.run(
        [sys.executable, script],
        text=True,
        check=True,
    )


def test__end_to_end_test():
    script = ".approval_tests_temp/approve_all.py"
    with tempfile.TemporaryDirectory(prefix="ApprovalTests.CommonScripts-") as _sandbox:
        sandbox = copy_template_dir(_sandbox, script)

        received_text = (sandbox / "a.received.txt").read_text()
        execute_the_script(sandbox / script)
        approved_text = (sandbox / "a.approved.txt").read_text()
        assert received_text == approved_text


def copy_template_dir(_sandbox, script):
    shutil.copytree(pathlib.Path("template_folder"), _sandbox, dirs_exist_ok=True)
    sandbox = pathlib.Path(_sandbox)
    render_template(sandbox, ".approval_tests_temp/.failed_comparison.log.template")
    script_path = sandbox / script
    shutil.copy(script_path.name, script_path)
    return sandbox


def render_template(root_dir, template_path):
    template_path = root_dir / template_path
    log_path = template_path.with_name(template_path.name.replace(".template", ""))
    content = template_path.read_text()
    content = content.replace("{root}", str(root_dir) + os.sep)
    log_path.write_text(content)


def test__approve_all__with_loader_and_saver():
    def failed_comparison_loader():
        return [
            "a.received.txt -> a.approved.txt",
            "b.received.txt -> b.approved.txt",
        ]

    moves = []

    def mover(a, b):
        nonlocal moves
        moves.append(f"{a} -> {b}")

    approve_all(failed_comparison_loader, mover)

    assert moves == failed_comparison_loader()


def test__approve_all_even_when_move_fails():
    def failed_comparison_loader():
        return [
            "a.received.txt -> a.approved.txt",
            "b.received.txt -> b.approved.txt",
        ]
    moves = []
    def mover(a, b):
        nonlocal moves
        if (a == "a.received.txt"):
            raise Exception("Failed to move file")
        moves.append(f"{a} -> {b}")

    approve_all(failed_comparison_loader, mover)

    assert moves == failed_comparison_loader()[1:]


def test__console_output():
    verify_approve_all([
        "a.received.txt -> a.approved.txt",
        "b.received.txt -> b.approved.txt",
        "bad.received.txt -> bad.approved.txt",
    ])


def verify_approve_all(files):
    def failed_comparison_loader():
        return files

    result = ""

    def system_out(text):
        nonlocal result
        result += text + "\n"

    def mover(from_, to):
        if "bad" in from_:
            raise Exception("Failed to move file")

    approve_all(failed_comparison_loader, mover, system_out)
    verify(result)


def test__zero_case():
    def failed_comparison_loader():
        return [
        ]
    result = ""

    def system_out(text):
        nonlocal result
        result += text + "\n"
    def mover(from_, to):
        pass

    approve_all(failed_comparison_loader, mover, system_out)

    verify(result)