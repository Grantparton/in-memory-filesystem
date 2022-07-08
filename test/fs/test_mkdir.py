from fs import fs


class TestMkdir:
    def test_no_args(self, capsys):
        filesystem = fs.FileSystem(commands=["mkdir"]).initialize()
        assert len(filesystem) == 1

        captured = capsys.readouterr()
        assert captured.out == "Usage: mkdir target ...\n"

    def test_multiple_args(self):
        filesystem = fs.FileSystem(
            commands=["mkdir test1 test2", "mkdir test2/test3"]
        ).initialize()
        test1_node = filesystem["/test1"]
        test2_node = filesystem["/test2"]
        test3_node = filesystem["/test2/test3"]
        root_node = filesystem[""]
        assert list(filesystem.keys()) == ["", "/test1", "/test2", "/test2/test3"]
        assert test1_node.parent == ""
        assert test2_node.parent == ""
        assert test3_node.parent == "/test2"
        assert "/test1" in root_node.children
        assert "/test2" in root_node.children
        assert "/test2/test3" in test2_node.children
        assert len(root_node.children) == 4
        assert len(test2_node.children) == 3

    def test_non_existant_directories(self):
        filesystem = fs.FileSystem(commands=["mkdir a/b/c"]).initialize()
        assert len(filesystem) == 1

    def test_directory_already_exists(self):
        filesystem = fs.FileSystem(
            commands=["mkdir test1", "mkdir test1/test2", "mkdir test1"]
        ).initialize()
        assert len(filesystem) == 3
        test1_node = filesystem["/test1"]
        test2_node = filesystem["/test1/test2"]
        assert len(test1_node.children) == 3
        assert test2_node.parent == test1_node.path
