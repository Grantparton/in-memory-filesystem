from fs import fs


class TestPwd:
    def test_no_args(self, capsys):
        fs.FileSystem(commands=["pwd"]).initialize()
        captured = capsys.readouterr()
        assert captured.out == "/\n"

    def test_too_many_args(self, capsys):
        fs.FileSystem(commands=["pwd /"]).initialize()
        captured = capsys.readouterr()
        assert captured.out == "pwd: too many arguments\n"

    def test_multiple_args(self, capsys):
        fs.FileSystem(
            commands=["mkdir test1", "cd test1", "pwd", "cd ..", "pwd"]
        ).initialize()

        captured = capsys.readouterr()
        assert captured.out == "/test1/\n/\n"
