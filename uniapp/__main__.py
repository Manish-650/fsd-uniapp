"""Run with python -m uniapp from the repository root."""

import argparse

from uniapp.cli.app import CLIUniApp
from uniapp.storage.database import Database


def main():
    parser = argparse.ArgumentParser(description="University student enrolment")
    parser.add_argument("--data", help="Optional path to a separate students.data file")
    args = parser.parse_args()
    try:
        database = Database(args.data)
    except (ValueError, OSError) as error:
        print(f"Cannot open student data: {error}")
        return 1
    CLIUniApp(database).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
