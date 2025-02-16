from abandoned_files import remove_abandoned_files, Mode


def test__find_abandoned_files__with_loader_and_saver():
    def load_touched_files():
        return ["b.approved.txt"]

    def get_all_approved_files():
        return ["a.approved.txt", "b.approved.txt"]

    deletes = []

    def delete(file):
        nonlocal deletes
        deletes.append(file)

    remove_abandoned_files(mode=Mode.NO_PROMPT, load_touched_files=load_touched_files, get_all_approved_files=get_all_approved_files, delete=delete)

    assert deletes == ["a.approved.txt"]
