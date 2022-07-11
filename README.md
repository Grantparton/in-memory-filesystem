
# In-Memory Filesystem
## Introduction
This is an implementation of an in memory file system. This implementation is
based on Unix's file system implementation in how we represent the system itself
using nodes to represent each directory/file in the file system.

## Features
* Path operations using special directories (`.` and `..`)
* Move & copy
* Symlinks
* Hardlinks
* File reading & writing
* Basic filesystem utilities

## Installation
It is recommended that this program be installed in a virtual environment. To 
do so, you can use the following commands. Note that the package requires a
minimum of Python 3.6:
```shell
python3.7 -m virtualenv venv
. venv/bin/activate
```

Then install the package locally using
```shell
pip install .
```

Now you can execute the package using the entrypoint, `fs`.

## Testing
The unit tests are written using pytest. To run them, execute the following
command from the root of the repository:
```shell
pytest test -v
```
There are currently 51 unit tests in the complete test suite.

## Usage
You can execute the package in two different ways: an interactive mode, or a
command-driven mode. To start up the filesystem in interactive mode, simply
pass the `--interactive` flag to the entrypoint:
```shell
% fs --interactive
> pwd
/
```
The alternative is a command-driven mode. This is used for testing purposes
and generates the filesystem given a list of commands, then exits. This is
less user-friendly, but still accessible via the command line.
```shell
% fs --commands 'touch a_file!' 'ls'
a_file!
%
```

There is also a flag which can be passed to control how big the virtual hard
disk is. Use the flag `--hard-disk-capacity` to do so: note that the value is in
bytes.
```shell
% fs --interactive --hard-disk-capacity 1
> touch a_file
> write a_file 'a_long_string'
Out of virtual disk space.
```

Note that you can always run `fs -h` to understand the different startup
options.

### Available Commands
The commands used to navigate are similar to those use in the Unix File System.
An important thing to note is that all of these commands support the special
`.` and `..` items in any given path.
The filesystem supports the following commands:

* cd
  * Usage: `cd <directory>`
  * Change directories to a directory indicated in the command.
* cp
  * Usage: `cp <source> ... <target>`
  * Copy any number of source files to a given target directory. Note that in
    this implementation there is no support for directory copying.
* find
  * Usage: `find <source> ...`
  * Find any items matching any number of source items in the current working
  directory
* ls
  * Usage: `ls <source> ...`
  * List the children of the source directories.
* mkdir
  * Usage: `mkdir <source> ...`
  * Create some directories.
* mv
  * Usage: `mv <source> ... <target>`
  * Move item(s) to target directory
* pwd
  * Usage: `pwd`
  * Print the working directory
* rm
  * Usage: `rm <source> ...`
  * Remove item(s) from the file system.
* touch
  * Usage: `touch <source> ...`
  * Create files in the filesystem.
* hardlink
  * Usage: `hardlink <source> <link name>`
  * Create a hard link between a source and a link. This link will
    follow the source node even if it moves.
* symlink
  * Usage: `symlink <source> <link name>`
  * Create a symbolic link between a source and a link. This link will break
    if the source object moves by design.
* write
  * Usage: `write <file_name> '<some contents>'`
  * Write some data to a file. Currently limited to a command line string.
* read
  * Usage: `read <file_name>`
  * Read some data that might've been written to a file

## Implementation
This implementation is essentially a running index of each node in the system.
At any given time, individual nodes don't have pointers to other nodes, they
have attributes that describe absolute paths to other nodes in the system. For
example, consider the following commands:

```shell
% mkdir a_dir
% touch a_file
% cd a_dir
% touch another_file
```

These commands would create inodes with the following attributes

| Node Path           | Parent | Children        |
|---------------------|--------|-----------------|
| /a_dir              | /      | /a_dir/another_file |
| /a_dir/another_file | /a_dir |                 |
| /a_file             | /      |                 |

And so on. Operations against the file system just adjust this table, which is
represented in code as the Filesystem's `inode_index` attribute. I chose this
 implementation because I know that the Unix File System also uses a table
to track inodes and I wanted to understand what operations were most difficult
to implement with that design decision. As it turns out, copying a directory
with a table like this isn't trivial: once the directory itself has its
absolute path adjusted, one must iterate through all descendants of that node
and adjust their paths accordingly. This is something I'd want to dig deeper 
on if I had more time to work on the project.

One particular area of implementation I'd like to discuss is how I chose to
approach issue of virtual hard disk space in my implementation. I chose to
implement it as a fixed size array where each slot in the array holds a single
byte from a byte array pulled apart from the serialized data. I took a naive
approach here where the next slot is determined by an ever-incrementing
hard disk index, only moving forward and never rewinding. This is the biggest
flaw in my approach, but I'm happy with it for my purposes as my only reason
to implement read/write in the first place was to properly unit test my hardlink
implementation. This is also why the read/write method is very rudimentary:
if I had more time I'd ideally add ways to write to a file other than command
line supplied strings. Writing this extension could be an entire take home
interview question in itself, but my way gets the job done with basic
functionality which is a prototype of what the UFS actually implements as well.

## Extensions
I chose to tackle four extensions: move/copy, file contents, operations on paths, and
linking. The latter two were more interesting given my design structure because I had to
introduce a helper function to navigate the tree with special directories in
place (. and ..) which at its core was a translator between any type of path
and an absolute path. The inode index table design would consistently have
O(1) node lookup without this feature.

I would also like to address the scoping of the other extensions and how my
design might interact with them. Walking a subtree with some kind of function
would be relatively easy to implement because of how lightweight it is to
navigate the inode index, making a utility like `tree` pretty interesting to
implement recursively. Adding permissions & groups also sounds simple to implement but would require
thought that is relatively unrelated to the file system itself: we could create
new classes for both users and groups which implement permissions as umasks, 
once again similar to how Unix handles this. From there, we could just 
instantiate one of these upon file system creation and add new commands for:
switching users, creating users, creating groups, adding users to groups. I
didn't want to work on this extension because it had less to do directly with
the file system itself. 
