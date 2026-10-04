"""Run with python -m uniapp.gui."""

import argparse
import tkinter as tk

from uniapp.gui.app import GUIUniApp
from uniapp.storage.database import Database


def main():
    parser = argparse.ArgumentParser(description="UniApp student GUI")
    parser.add_argument("--data", help="Optional shared student-data path")
    args = parser.parse_args()
    try:
        database = Database(args.data)
        root = tk.Tk()
    except (ValueError, OSError, tk.TclError) as error:
        print(f"Cannot start GUI: {error}")
        return 1
    GUIUniApp(root, database)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
