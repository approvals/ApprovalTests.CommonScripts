from abandoned_files import remove_abandoned_files, Mode
from approvaltests import verify, Options
from approvaltests.reporters import GenericDiffReporter, GenericDiffReporterConfig


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


def verify_abandoned_files(files):
    def load_touched_files():
        return [file for file in files if "stray" not in file]

    def get_all_approved_files():
        return files

    def delete(file):
        pass

    result = ""

    def system_out(text):
        nonlocal result
        result += text + "\n"

    remove_abandoned_files(
        mode=Mode.DELETE_WITHOUT_PROMPTING,
        load_touched_files=load_touched_files,
        get_all_approved_files=get_all_approved_files,
        delete=delete,
        system_out=system_out,
    )

    class ReportWithBeyondCompare5Windows(GenericDiffReporter):
        def __init__(self):
            super().__init__(
                config=GenericDiffReporterConfig(
                    name=self.__class__.__name__,
                    path="{ProgramFiles}/Beyond Compare 5/BCompare.exe",
                )
            )

    verify(result, options=Options().with_reporter(ReportWithBeyondCompare5Windows()))
