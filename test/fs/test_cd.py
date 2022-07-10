from fs import fs


class TestCd:
    def test_no_args(self, capsys):
        fs.FileSystem(commands=["cd"]).initialize()
        captured = capsys.readouterr()
        assert captured.out == "Usage: cd target\n"

    def test_non_existant_directory(self, capsys):
        bad_directory = "a_non_existant_directory"
        fs.FileSystem(commands=[f"cd {bad_directory}"]).initialize()
        captured = capsys.readouterr()
        assert captured.out == f"Path {bad_directory} does not exist.\n"

    def test_multiple_args(self, capsys):
        fs.FileSystem(
            commands=["mkdir test1 test2", "cd test1 test2"]
        ).initialize()
        captured = capsys.readouterr()
        assert captured.out == f"Usage: cd target\n"

    def test_cd_into_directory(self, capsys):
        fs.FileSystem(
            commands=["mkdir test1", "cd test1", "cd ..", "pwd"]
        ).initialize()
        captured = capsys.readouterr()
        assert captured.out == "/\n"

    def test_cd_into_root(self, capsys):
        fs.FileSystem(commands=["cd ..", "pwd"]).initialize()
        captured = capsys.readouterr()
        assert captured.out == "/\n"

    def test_cd_into_absolute_directory_nested(self, capsys):
        fs.FileSystem(
            commands=[
                "mkdir test1 test1/test2 test1/test2/test3",
                "cd /test1/test2/test3",
                "pwd",
            ]
        ).initialize()
        captured = capsys.readouterr()
        assert captured.out == "/test1/test2/test3/\n"

    def test_cd_with_special_nodes(self, capsys):
        fs.FileSystem(
            commands=[
                "mkdir test1",
                "cd /test1/../.",
                "pwd",
            ]
        ).initialize()
        captured = capsys.readouterr()
        assert captured.out == "/\n"
