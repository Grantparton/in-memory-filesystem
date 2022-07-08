from fs import fs


# TODO: Add assertions for stdout when exceptions are thrown


class TestCp:
    def test_improper_args(self, capsys):
        fs.FileSystem(commands=["cp"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Usage: cp source ... target\n"

    def test_proper_args(self, capsys):
        filesystem = fs.FileSystem(
            commands=[
                "touch test1 test2",
                "mkdir test_dir",
                "cp test1 test2 test_dir",
                "ls test_dir",
            ]
        ).initialize()
        assert len(filesystem) == 6

        captured = capsys.readouterr()
        assert captured.out == "test1\ntest2\n"

    def test_non_existant_directories(self, capsys):
        bad_directory = "test2"
        filesystem = fs.FileSystem(
            commands=["touch test1", f"cp test1 {bad_directory}"]
        ).initialize()
        assert len(filesystem) == 2

        captured = capsys.readouterr()
        assert captured.out == f"Path {bad_directory} does not exist.\n"

    def test_non_existant_files(self, capsys):
        bad_file = "test1"
        filesystem = fs.FileSystem(
            commands=["mkdir test2", f"cp {bad_file} test2"]
        ).initialize()
        assert len(filesystem) == 2

        captured = capsys.readouterr()
        assert captured.out == f"Path {bad_file} does not exist.\n"
