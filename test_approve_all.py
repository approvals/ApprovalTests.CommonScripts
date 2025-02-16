import os
import pathlib
import subprocess
import sys
import tempfile
import shutil

from approve_all import approve_all


def execute_the_script(script: pathlib.Path):
    subprocess.run(
        [
            sys.executable,
            script
        ],
        text=True,
        check=True,
    )


def test__end_to_end_test():

    script =".approval_tests_temp/approve_all.py"
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
