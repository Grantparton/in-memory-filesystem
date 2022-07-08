from typing import List, Dict
from . import exceptions


class INode:
    """
    Class the represents an inode object in our filesystem, similar to how the
    Unix File System deals with files. Both directories and files are
    both the same underlying object, an inode.
    """

    def __init__(
        self, path: str = None, is_directory: bool = False, parent: str = None
    ):
        self.is_directory = is_directory
        self.children = {".": path, "..": parent}
        self.parent = parent
        self.path = path


class FileSystem:
    def __init__(self, interactive: bool = False, commands: List[str] = None):
        """
        Initialize an empty filesystem.
        :param interactive: If True, consume commands from user input instead.
        :param commands: If passed, rely on a list of strings of commands
            instead.
        """
        self.interactive = interactive
        self.current_location = ""
        self.commands = commands
        # TODO: Allow files and directories to share names
        # We could make the index a tuple of both the path and the type of
        # the node such that file and directories can share a namespace.
        root_inode = INode(path="", is_directory=True,
                           parent=self.current_location)
        self.inode_index = {self.current_location: root_inode}

    def __create_new_inode(self,
                           name: str, parent: str, is_directory: bool) -> None:
        """
        This is used by all methods that create new inode entries in our
        filesystem. We must supply the name of the base item, the path to the
        parent of the new inode, and whether or not this is a directory.
        :param name: The base name of the item we want to create.
        :param parent: The absolute path to the parent of the node we want to
            create.
        :param is_directory: Whether or not we're creating directories
        :return: None
        """
        parent_node = self.inode_index[parent]
        new_node_path = parent + "/" + name
        if new_node_path not in parent_node.children.keys():
            new_node = INode(
                path=new_node_path, is_directory=is_directory, parent=parent
            )
            if is_directory:
                new_node.children = {".": new_node_path, "..": parent}
            self.inode_index[new_node_path] = new_node
            parent_node.children[new_node_path] = new_node
            self.inode_index[parent] = parent_node
        else:
            raise exceptions.NodeAlreadyExists(
                f"Filesystem item with name {new_node_path} already exists."
            )

    def __create_new_inodes(self, inputs: List[str],
                            directories: bool = False) -> None:
        """
        Helper function used to kick off the inode creation process. We wrap the
        inner-most __create_new_inode with this function to filter out special
        characters.
        :param inputs:
        :param directories:
        :return:
        """
        for item in inputs:
            if item in [".", ".."]:
                raise exceptions.ImproperArguments(
                    "Cannot create files with reserved names . or .."
                )
            parent_node = self.__find_node(item, parent=True)
            self.__create_new_inode(item.split("/")[-1], parent_node.path,
                                    directories)

    def __find_node(self, path: str, parent: bool = False) -> INode:
        """
        Find a node in the filesystem. Essentially a translator of a path that
        may include special characters (./..) into the node of the absolute
        path.
        :param path: A /-delimited path that must be traversed.
        :param parent: If True, return the parent of the passed absolute path
            instead.
        :return: The inode for a given path.
        """
        split_path = path.split("/")
        if split_path[0]:
            current_path = self.current_location
        else:
            # An empty string for the first element means the path had a
            # leading '/', indicating we start at the root instead.
            current_path = ""
            split_path.pop(0)
        node = self.inode_index[current_path]
        for item in split_path[: -1 if parent else len(split_path)]:
            if item == ".":
                continue
            elif item == "..":
                node = self.inode_index[node.parent]
                current_path = node.parent
            else:
                current_path = current_path + "/" + item
                node = self.inode_index.get(current_path, None)
                if not node:
                    raise exceptions.PathException(f"Path {path} does not exist.")
        return node

    def ls(self, paths: List[str], match: str = "") -> None:
        """
        List the contents of given directories indicated by `paths`. Also allow
        supplying a match, which can be used to restrict the output to specific
        patterns.
        :param paths: A list of paths to list against.
        :param match: A string that needs to be matched in order to count for
            output.
        :return: None
        """
        if not paths:
            # Default argument for ls is the current working directory.
            paths = ["."]
        for path in paths:
            node = self.__find_node(path)
            for item in node.children.keys():
                item_node = self.inode_index.get(item, None)
                cwd_scoped_item = item.split("/")[-1]
                if (match and cwd_scoped_item == match) or not match:
                    if item_node:
                        print(f"{'/' if item_node.is_directory else ''}{cwd_scoped_item}")

    def touch(self, inputs: List[str]) -> None:
        """
        Create new file(s). Take a list of inputs, which are paths to the
        new inodes, and create the backing nodes for them.
        :param inputs: List of paths to instantiate
        :return: None
        """
        if inputs:
            self.__create_new_inodes(inputs)
        else:
            raise exceptions.ImproperArguments("Usage: touch target ...")

    def mkdir(self, inputs: List[str]) -> None:
        """
        Create new directory entries. Take a list of inputs, which are paths to
        the new inodes, and create the backing nodes for them.
        :param inputs: List of paths to instantiate
        :return: None
        """
        if inputs:
            self.__create_new_inodes(inputs, directories=True)
        else:
            raise exceptions.ImproperArguments("Usage: mkdir target ...")

    def rm(self, paths: List[str]) -> None:
        """
        Remove the items indicated in `paths` from the filesystem. We know that
        an item is a candidate for removal if it is a directory with only two
        children (. and ..) or the item is a file. Removal requires both a
        target node and the parent of that node: in order to save on tree
        traversal time we just find the parent then traverse one item further.
        :param paths: List of paths of each item we want to remove.
        :return: None
        """
        if paths:
            for path in paths:
                parent_node = self.__find_node(path, parent=True)
                last_item = path.split("/")[-1]
                if last_item == ".":
                    node_path = parent_node.path
                elif last_item == "..":
                    node_path = parent_node.parent
                else:
                    node_path = parent_node.path + "/" + last_item
                node = self.inode_index[node_path]
                if (
                    node.is_directory and len(node.children) == 2
                ) or not node.is_directory:
                    del parent_node.children[node_path]
                    self.inode_index[parent_node.path] = parent_node
                    del self.inode_index[node_path]
                else:
                    raise exceptions.DirectoryNonEmpty(
                        f"Directory {node_path} isn't empty."
                    )
        else:
            raise exceptions.ImproperArguments("Must provide arguments.")

    def mv(self, inputs: List[str]) -> None:
        """
        Moving is the same as copying but removes the copy target after the
        copying itself is complete. Reuse that method here.
        :param inputs: List of items we want to move.
        :return: None
        """
        self.cp(inputs, move=True)

    def cp(self, inputs: List[str], move: bool = False) -> None:
        """
        Copy a list of items from one directory to another. An optional
        parameter `move` can be passed to remove the source items after the
        process of copying is complete. Note that in this implementation we
        only support copying of files.
        :param inputs: List of items we want to copy.
        :param move: True if original items should be deleted.
        :return: None
        """
        action = "mv" if move else "cp"
        if len(inputs) >= 2:
            sources = inputs[:-1]
            target = inputs[-1]
            target_node = self.__find_node(target)
            if target_node.is_directory:
                for source in sources:
                    try:
                        source_node = self.__find_node(source)
                        new_path = target_node.path + "/" + source.split("/")[0]
                        # TODO: Implement directory copy
                        if not source_node.is_directory:
                            copied_node = INode(path=new_path,
                                                parent=target_node.path)
                            target_node.children[new_path] = copied_node
                            self.inode_index[new_path] = copied_node
                            if move:
                                parent_node_of_source = self.inode_index[
                                    source_node.parent
                                ]
                                del parent_node_of_source.children[source_node.path]
                                del self.inode_index[source_node.path]
                        else:
                            raise exceptions.ImproperArguments(
                                "Operation unsupported on directories."
                            )

                    except exceptions.PathException as e:
                        print(e)
                        continue
                self.inode_index[target_node.path] = target_node
            else:
                raise exceptions.ImproperArguments("Cannot move items to a file.")
        else:
            raise exceptions.ImproperArguments(f"Usage: {action} source ... target")

    def find(self, names: List[str]) -> None:
        """
        Find some items in the current directory. We use the `ls` method here
        because we can specify to `ls` that we only want to return items
        that match the item names.
        :param names: List of names we want to find in the current working
            directory.
        :return: None
        """
        if names:
            for name in names:
                self.ls(self.current_location, match=name)
        else:
            raise exceptions.ImproperArguments(f"Usage: find target")

    def cd(self, path: List[str]) -> None:
        """
        Change the current working directory to the path listed in `path`. The
        parameter is a list in order to catch misuse of the command.
        :param path: The path we want to change directories to.
        :return: None
        """
        if path and len(path) == 1:
            node = self.__find_node(path[0])
            self.current_location = node.path
        else:
            raise exceptions.ImproperArguments("Usage: cd target")

    def pwd(self, inputs) -> None:
        """
        Print the current working directory. Essentially a getter for the
        FileSystem `current_location` attribute.
        :param inputs: Should be an empty list. If not, raise error.
        :return: None
        """
        if inputs:
            raise exceptions.ImproperArguments("pwd: too many arguments")
        print(self.current_location + "/")

    def exec(self, command: str) -> int:
        """
        Given a string of a command, execute the command. `command` will be of
        the form `<command> <arg1> <arg2> ...`, like `touch a_file` for example.
        :param command: A string indicating a command and its arguments.
        :return: 1 when the `exit` command is issued.
        """
        split_input = command.split()
        if split_input[0] == "ls":
            self.ls(split_input[1:])
        elif split_input[0] == "find":
            self.find(split_input[1:])
        elif split_input[0] == "touch":
            self.touch(split_input[1:])
        elif split_input[0] == "mkdir":
            self.mkdir(split_input[1:])
        elif split_input[0] == "pwd":
            self.pwd(split_input[1:])
        elif split_input[0] == "cd":
            self.cd(split_input[1:])
        elif split_input[0] == "rm":
            self.rm(split_input[1:])
        elif split_input[0] == "cp":
            self.cp(split_input[1:])
        elif split_input[0] == "mv":
            self.mv(split_input[1:])
        elif split_input[0] == "exit":
            return 1
        else:
            print(f"Unrecognized command: {split_input[0]}")

    def initialize(self) -> Dict[str, INode]:
        """
        Boot up the in-memory filesystem. Depending on the arguments passed on
        object initialization, choose to either rely on user input for the
        commands or iterate over a list of commands.
        :return: The inode index of the filesystem, a dictionary mapping
            an absolute path of a node to the node itself.
        """
        if self.commands:
            for command in self.commands:
                try:
                    if self.exec(command) == 1:
                        break
                except (
                    exceptions.ImproperArguments,
                    exceptions.PathException,
                    exceptions.NodeAlreadyExists,
                    exceptions.DirectoryNonEmpty,
                ) as e:
                    print(e)
        elif self.interactive:
            print('Use the command `exit` to terminate the program.')
            while True:
                command = input(f"{self.current_location} > ")
                try:
                    if self.exec(command) == 1:
                        break
                except (
                    exceptions.ImproperArguments,
                    exceptions.PathException,
                    exceptions.NodeAlreadyExists,
                    exceptions.DirectoryNonEmpty,
                ) as e:
                    print(e)
        else:
            print("Must supply --interactive or --commands 'command1' ...")
        return self.inode_index
