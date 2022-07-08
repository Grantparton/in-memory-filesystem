from fs import fs


class TestFind:
    def test_no_args(self, capsys):
        fs.FileSystem(commands=["find"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Usage: find target\n"

    def test_multiple_args(self, capsys):
        fs.FileSystem(
            commands=["touch test1 test2", "find test1 test2 test3"]
        ).initialize()

        captured = capsys.readouterr()
        assert captured.out == "test1\ntest2\n"

    def test_non_existant_directories(self, capsys):
        fs.FileSystem(commands=[f"find nothing"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == ""
