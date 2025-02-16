import os
import pathlib
import subprocess
import sys
import tempfile

from approve_all import approve_all


def execute_the_script(cwd: pathlib.Path):
    subprocess.run(
        [
            sys.executable,
            ".approval_tests_temp/approve_all.py",
        ],
        cwd=cwd,
        text=True,
        check=True,
    )


def test__end_to_end_test():
    with tempfile.TemporaryDirectory(prefix="ApprovalTests.CommonScripts-") as _sandbox:
        template_folder = pathlib.Path("template_folder")
        import shutil
        shutil.copytree(template_folder, _sandbox, dirs_exist_ok=True)

        sandbox = pathlib.Path(_sandbox)
        a = sandbox / "a.received.txt"
        received_text = a.read_text()
        # copy sandef copy_and_replace_template(sandbox: pathlib.Path):
        template_path = sandbox / ".approval_tests_temp/.failed_comparison.log.template"
        log_path = sandbox / ".approval_tests_temp/.failed_comparison.log"

        # Read the template content
        content = template_path.read_text()

        # Replace {root} with the full path of the sandbox
        print(f"{content=}")
        content = content.replace("{root}", str(sandbox) + os.sep)
        print(f"{content=}")

        # Write the modified content to the log file
        log_path.write_text(content)

        (sandbox / ".approval_tests_temp/approve_all.py").write_text(
            pathlib.Path("approve_all.py").read_text()
        )

        execute_the_script(cwd=sandbox)

        approved_text = (sandbox / "a.approved.txt").read_text()

    assert received_text == approved_text


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
