from enum import Enum
from pathlib import Path
from typing import Callable

class Mode(Enum):
    DELETE_WITHOUT_PROMPTING = 1
    PROMPT = 2
    DRY_RUN = 3


def remove_abandoned_files(*, mode, load_touched_files, get_all_approved_files, delete,
                           system_out: Callable[[str], None] = print,
                           ):

    touched_files = load_touched_files()
    all_approved_files = get_all_approved_files()

    stray_files = [Path(file) for file in all_approved_files if file not in touched_files]
    for stray_file in stray_files:
        delete(str(stray_file))
    report(system_out, stray_files)


def report(system_out, stray_files):
    system_out("Unused `.approved.` files found.\n")

    for stray_file in stray_files:
        system_out(f" - {stray_file.name} (in {stray_file.parent.as_posix()}/)")

    system_out("")
    system_out(f"Deleted {len(stray_files)} files.")
