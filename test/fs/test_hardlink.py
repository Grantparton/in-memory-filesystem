from fs import fs


class TestHardlink:
    def test_bad_args(self, capsys):
        fs.FileSystem(commands=["symlink test"]).initialize()
        captured = capsys.readouterr()
        assert captured.out == "Usage: symlink [source_item] [link_name]\n"

    def test_valid_arguments(self):
        filesystem = fs.FileSystem(
            commands=[
                "mkdir a_dir",
                "touch a_dir/a_file",
                "hardlink a_dir/a_file a_symlink",
            ]
        ).initialize()
        assert len(filesystem) == 4

    def test_remove_link_source(self):
        # Creating a hard link to a file should increase the reference count
        # of that file by one, meaning a deletion of that file should keep the
        # file around.
        filesystem = fs.FileSystem(
            commands=[
                "mkdir a_dir",
                "touch a_dir/a_file",
                "hardlink a_dir/a_file a_hardlink",
                "rm a_dir/a_file",
            ]
        ).initialize()
        hardlink = filesystem["/a_hardlink"]
        root = filesystem[""]
        hardlink.parent = root.path
        assert len(filesystem) == 4

    def test_move_link_source(self):
        filesystem = fs.FileSystem(
            commands=[
                "mkdir a_dir b_dir",
                "touch a_dir/a_file",
                "hardlink a_dir/a_file a_hardlink",
                "mv a_dir/a_file b_dir",
            ]
        ).initialize()
        hardlink = filesystem["/a_hardlink"]
        assert hardlink.link == "/b_dir/a_file"
        assert len(filesystem) == 5
