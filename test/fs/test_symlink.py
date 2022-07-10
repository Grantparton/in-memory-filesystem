from fs import fs


class TestSymlink:
    def test_bad_args(self, capsys):
        fs.FileSystem(commands=["hardlink test"]).initialize()
        captured = capsys.readouterr()
        assert captured.out == "Usage: hardlink [source_item] [link_name]\n"

    def test_valid_arguments(self):
        filesystem = fs.FileSystem(
            commands=[
                "mkdir a_dir",
                "touch a_dir/a_file",
                "symlink a_dir/a_file a_symlink",
            ]
        ).initialize()
        assert len(filesystem) == 4

    def test_remove_link_source(self):
        # Creating a symlink to a file shouldn't increase the reference count
        # of that file by one, meaning a deletion of that file should create a
        # dangling link
        filesystem = fs.FileSystem(
            commands=[
                "mkdir a_dir",
                "touch a_dir/a_file",
                "symlink a_dir/a_file a_symlink",
                "rm a_dir/a_file",
            ]
        ).initialize()
        symlink = filesystem["/a_symlink"]
        root = filesystem[""]
        symlink.parent = root.path
        assert len(filesystem) == 3
