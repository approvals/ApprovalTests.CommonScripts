from enum import Enum
from pathlib import Path
from typing import Callable, List

SCRIPT_DIR = Path(__file__).parent


class Mode(Enum):
    DELETE_WITHOUT_PROMPTING = 1
    PROMPT = 2
    DRY_RUN = 3


def delete_file(path: Path) -> None:
    path.unlink(missing_ok=True)


def load_touched_files() -> List[str]:
    return (SCRIPT_DIR / ".approved_files.log").read_text().splitlines()


def get_all_approved_files() -> List[str]:
    return list(map(str, SCRIPT_DIR.parent.rglob("*.approved.*")))


def remove_abandoned_files(
    *,
    mode: Mode,
    load_touched_files: Callable[[], List[str]] = load_touched_files,
    get_all_approved_files: Callable[[], List[str]] = get_all_approved_files,
    delete: Callable[[Path], None] = delete_file,
    system_out: Callable[[str], None] = print,
):
    touched_files = load_touched_files()
    all_approved_files = get_all_approved_files()

    stray_files = [
        Path(file) for file in all_approved_files if file not in touched_files
    ]
    report_dry_run(system_out, stray_files)

    if should_delete(mode, system_out):
        for stray_file in stray_files:
            delete(stray_file)

    report_final_status(system_out, stray_files)


def should_delete(mode: Mode, system_out) -> bool:
    if mode == Mode.PROMPT:
        system_out("Delete? [Y/n]")
        response = input()
        return response in ["Y", "y", ""]
    elif mode == Mode.DELETE_WITHOUT_PROMPTING:
        return True
    elif mode == Mode.DRY_RUN:
        return False

    return False


def report_dry_run(system_out, stray_files):
    system_out("Unused `.approved.` files found.\n")

    for stray_file in stray_files:
        system_out(f" - {stray_file.name} (in {stray_file.parent.as_posix()}/)")


def report_final_status(system_out, stray_files):
    system_out("")
    system_out(f"Deleted {len(stray_files)} files.")


if __name__ == "__main":
    remove_abandoned_files(mode=Mode.PROMPT)
