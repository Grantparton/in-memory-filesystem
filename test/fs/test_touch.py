from fs import fs


class TestTouch:
    def test_no_args(self, capsys):
        filesystem = fs.FileSystem(commands=["touch"]).initialize()
        assert len(filesystem) == 1

        captured = capsys.readouterr()
        assert captured.out == "Usage: touch target ...\n"

    def test_multiple_args(self):
        filesystem = fs.FileSystem(commands=["touch test1 test2"]).initialize()
        test1_node = filesystem["/test1"]
        test2_node = filesystem["/test2"]
        root_node = filesystem[""]
        assert test1_node.parent == ""
        assert test2_node.parent == ""
        assert "/test1" in root_node.children
        assert "/test2" in root_node.children

    def test_non_existant_directories(self):
        filesystem = fs.FileSystem(commands=["mkdir a/b/c"]).initialize()
        assert len(filesystem) == 1

    def test_directory_already_exists(self):
        filesystem = fs.FileSystem(commands=["touch test1 test1"]).initialize()
        test1_node = filesystem["/test1"]
        root_node = filesystem[""]
        assert test1_node.parent == ""
        assert "/test1" in root_node.children
