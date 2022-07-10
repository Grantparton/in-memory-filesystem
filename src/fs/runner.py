import argparse

from . import fs


def main(args=None):
    parser = argparse.ArgumentParser(
        description=f"Start up the in-memory filesystem.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--commands", nargs="+")
    args = parser.parse_args(args)

    try:
        fs.FileSystem(
            interactive=getattr(args, "interactive", None),
            commands=getattr(args, "commands", None),
        ).initialize()
        return 0
    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    exit(main())
