from fs import fs


class TestLs:
    def test_no_args(self, capsys):
        fs.FileSystem(commands=["touch test1 test2", "ls"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == "test1\ntest2\n"

    def test_multiple_args(self, capsys):
        fs.FileSystem(
            commands=[
                "mkdir test1 test3",
                "touch test1/test2 test3/test4",
                "ls test1 test3",
            ]
        ).initialize()

        captured = capsys.readouterr()
        assert captured.out == "test2\ntest4\n"

    def test_non_existant_directories(self, capsys):
        bad_directory = "a_non_existant_directory"
        fs.FileSystem(commands=[f"ls {bad_directory}"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == f"Path {bad_directory} does not exist.\n"
