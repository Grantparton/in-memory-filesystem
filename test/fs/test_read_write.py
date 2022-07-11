from fs import fs
import pickle


class TestReadWrite:
    """
    Reading and writing are very closely related so we test both here.
    """

    def test_read_no_args(self, capsys):
        fs.FileSystem(commands=["read"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Usage: read <file>\n"

    def test_write_no_args(self, capsys):
        fs.FileSystem(commands=["write"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Usage: write <file> '<a_string>'\n"

    def test_write_past_capacity(self, capsys):
        fs.FileSystem(
            commands=["touch test_file", "write test_file 'testing'"],
            hard_disk_capacity=1,
        ).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Out of virtual disk space.\n"

    def test_write_on_non_file(self, capsys):
        fs.FileSystem(
            commands=["mkdir test", "write test 'testing'"]
        ).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Writing only supported on files\n"

    def test_standard_workflow(self, capsys):
        file_contents = "'testing'"
        filesystem = fs.FileSystem(
            commands=[
                "touch test_file",
                f"write test_file {file_contents}",
                f"write test_file {file_contents}",
                "read test_file",
            ]
        ).initialize()
        test_file = filesystem["/test_file"]
        assert test_file.data

        number_of_bytes = len(list(pickle.dumps(file_contents)))
        assert test_file.data == [
            (0, number_of_bytes),
            (number_of_bytes, number_of_bytes * 2),
        ]

        captured = capsys.readouterr()
        assert captured.out == f"{file_contents}{file_contents}\n"

    def test_remove_file(self, capsys):
        file_contents = "'testing'"
        filesystem = fs.FileSystem(
            commands=[
                "touch test_file",
                f"write test_file {file_contents}",
                "rm test_file",
            ]
        ).initialize()
