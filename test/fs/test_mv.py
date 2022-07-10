from fs import fs


class TestMv:
    def test_improper_args(self, capsys):
        fs.FileSystem(commands=["mv"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Usage: mv source ... target\n"

    def test_proper_args(self, capsys):
        filesystem = fs.FileSystem(
            commands=[
                "touch test1 test2",
                "mkdir test_dir",
                "mv test1 test2 test_dir",
                "ls",
                "ls test_dir",
            ]
        ).initialize()
        assert len(filesystem) == 4

        captured = capsys.readouterr()
        assert captured.out == "/test_dir\ntest1\ntest2\n"

    def test_non_existant_directories(self, capsys):
        bad_directory = "test2"
        fs.FileSystem(
            commands=["touch test1", f"mv test1 {bad_directory}"]
        ).initialize()

        captured = capsys.readouterr()
        assert captured.out == f"Path {bad_directory} does not exist.\n"

    def test_non_existant_files(self, capsys):
        bad_file = "test1"
        fs.FileSystem(
            commands=["mkdir test2", f"mv {bad_file} test2"]
        ).initialize()

        captured = capsys.readouterr()
        assert captured.out == f"Path {bad_file} does not exist.\n"
