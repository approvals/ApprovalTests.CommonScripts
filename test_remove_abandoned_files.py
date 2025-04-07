from remove_abandoned_files import remove_abandoned_files, Mode
from approvaltests import verify


def test__find_abandoned_files__with_loader_and_saver():
    def load_touched_files():
        return ["b.approved.txt"]

    def get_all_approved_files():
        return ["a.approved.txt", "b.approved.txt"]

    deletes = []

    def delete(file):
        nonlocal deletes
        deletes.append(file.name)

    remove_abandoned_files(
        mode=Mode.DELETE_WITHOUT_PROMPTING,
        load_touched_files=load_touched_files,
        get_all_approved_files=get_all_approved_files,
        delete=delete,
    )

    assert deletes == ["a.approved.txt"]


def test__console_output():
    verify_abandoned_files(
        [
            "path/to/a.stray.approved.txt",
            "b.approved.txt",
            "path/to2/c.stray.approved.txt",
        ]
    )


def test__reject():
    verify_abandoned_files(
        [
            "path/to/a.stray.approved.txt",
            "b.approved.txt",
            "path/to2/c.stray.approved.txt",
        ],
        Mode.PROMPT,
        lambda: "n",  # Simulate user input
    )

def test__no_abandoned_files():
    verify_abandoned_files(
        [
            "b.approved.txt",
        ],
        Mode.PROMPT,
        None,
    )


def verify_abandoned_files(files, mode=Mode.DELETE_WITHOUT_PROMPTING, get_input=None):
    def load_touched_files():
        return [file for file in files if "stray" not in file]

    def get_all_approved_files():
        return files

    def delete(file):
        pass

    console_output = ""

    def system_out(text):
        nonlocal console_output
        console_output += text + "\n"

    def get_and_print_input():
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
