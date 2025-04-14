from remove_abandoned_files import remove_abandoned_files, Mode
from approvaltests import verify
from typing import Callable, List, Optional
import pathlib


def test__find_abandoned_files__with_loader_and_saver() -> None:
    def load_touched_files() -> List[str]:
        return ["b.approved.txt"]

    def get_all_approved_files() -> List[str]:
        return ["a.approved.txt", "b.approved.txt"]

    deletes = []

    def delete(file: pathlib.Path) -> None:
        nonlocal deletes
        deletes.append(file.name)

    remove_abandoned_files(
        mode=Mode.DELETE_WITHOUT_PROMPTING,
        load_touched_files=load_touched_files,
        get_all_approved_files=get_all_approved_files,
        delete=delete,
    )

    assert deletes == ["a.approved.txt"]


def test__console_output() -> None:
    verify_abandoned_files(
        [
            "path/to/a.stray.approved.txt",
            "b.approved.txt",
            "path/to2/c.stray.approved.txt",
        ]
    )


def test__reject() -> None:
    verify_abandoned_files(
        [
            "path/to/a.stray.approved.txt",
            "b.approved.txt",
            "path/to2/c.stray.approved.txt",
        ],
        Mode.PROMPT,
        lambda: "n",  # Simulate user input
    )


def test__no_abandoned_files() -> None:
    verify_abandoned_files(
        [
            "b.approved.txt",
        ],
        Mode.PROMPT,
        None,
    )


def test__path_normalization() -> None:
    def load_touched_files() -> List[str]:
        return ["path/to/./file.approved.txt"]

    def get_all_approved_files() -> List[str]:
        return ["path/to/file.approved.txt"]

    deletes = []

    def delete(file: pathlib.Path) -> None:
        nonlocal deletes
        deletes.append(file.name)

    remove_abandoned_files(
        mode=Mode.DELETE_WITHOUT_PROMPTING,
        load_touched_files=load_touched_files,
        get_all_approved_files=get_all_approved_files,
        delete=delete,
    )

    # These paths should be considered equivalent, so no files should be deleted
    assert deletes == [], "File was incorrectly identified as abandoned"


def verify_abandoned_files(
    files: List[str],
    mode: Mode = Mode.DELETE_WITHOUT_PROMPTING,
    get_input: Optional[Callable[[], str]] = input,
) -> None:
    def load_touched_files() -> List[str]:
        return [file for file in files if "stray" not in file]

    def get_all_approved_files() -> List[str]:
        return files

    def delete(file: pathlib.Path) -> None:
        pass

    console_output = ""

    def system_out(text: str) -> None:
        nonlocal console_output
        console_output += text + "\n"

    def get_and_print_input() -> str:
        assert get_input is not None

        input = get_input()
        system_out(input)
        return input

    remove_abandoned_files(
        mode=mode,
        load_touched_files=load_touched_files,
        get_all_approved_files=get_all_approved_files,
        delete=delete,
        system_out=system_out,
        get_input=get_and_print_input,
    )

    verify(
        console_output,
    )
