class PathException(Exception):
    """
    Exception thrown when invalid path is supplied.
    """


class ImproperArguments(Exception):
    """
    Exception thrown when invalid arguments are passed to a function.
    """


class NodeAlreadyExists(Exception):
    """
    Exception thrown when encountering existing nodes during a command that
    intends to create new nodes.
    """


class DirectoryNonEmpty(Exception):
    """
    Exception thrown when trying to remove a directory that isn't empty.
    """


class OutOfDisk(Exception):
    """
    Exception thrown when trying to write to a file but the virtual disk is
    full.
    """
