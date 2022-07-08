from fs import fs


class TestCd:
    def test_no_args(self, capsys):
        fs.FileSystem().initialize()
        captured = capsys.readouterr()
        assert captured.out == "Must supply --interactive or --commands " \
                               "'command1' ...\n"

    def test_bad_arg(self, capsys):
        fs.FileSystem(commands=['? ? ?']).initialize()
        captured = capsys.readouterr()
        assert captured.out == "Unrecognized command: ?\n"
