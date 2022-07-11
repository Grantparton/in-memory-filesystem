import argparse

from . import fs


def main(args=None):
    parser = argparse.ArgumentParser(
        description=f"Start up the in-memory filesystem.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode: specifying the commands one at a time, interactively.",
    )
    parser.add_argument(
        "--commands",
        nargs="+",
        help="If specified, execute a series of predetermined commands instead. Format as follows: --commands 'command 1' 'command 2'",
    )
    parser.add_argument(
        "--hard-disk-capacity",
        type=int,
        help="The capacity of the virtual hard disk, in bytes. Default is 1000.",
    )
    args = parser.parse_args(args)

    try:
        fs.FileSystem(
            interactive=getattr(args, "interactive", None),
            commands=getattr(args, "commands", None),
            hard_disk_capacity=getattr(args, "hard_disk_capacity", 1000),
        ).initialize()
        return 0
    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    exit(main())
