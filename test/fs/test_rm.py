from fs import fs


class TestRm:
    def test_no_args(self, capsys):
        fs.FileSystem(commands=["rm"]).initialize()

        captured = capsys.readouterr()
        assert captured.out == "Must provide arguments.\n"

    def test_multiple_args(self):
        filesystem = fs.FileSystem(
            commands=[
                "mkdir test1",
                "touch test1/test2",
                "rm test1/test2 test1",
            ]
        ).initialize()
        assert len(filesystem) == 1

        root_node = filesystem[""]
        assert len(root_node.children) == 2  # Just . and ..

    def test_remove_non_empty_directories(self, capsys):
        non_empty_directory = "/test1"
        filesystem = fs.FileSystem(
            commands=[
                f"mkdir {non_empty_directory}",
                f"touch {non_empty_directory}/b",
                f"rm {non_empty_directory}",
            ]
        ).initialize()
        assert len(filesystem) == 3

        captured = capsys.readouterr()
        assert captured.out == f"Directory {non_empty_directory} isn't empty.\n"
