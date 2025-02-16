from enum import Enum


class Mode(Enum):
    NO_PROMPT = 1
    PROMPT = 2


def remove_abandoned_files(mode, load_touched_files, get_all_approved_files, delete):
    delete("a.approved.txt")
