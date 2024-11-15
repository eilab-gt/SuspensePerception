#!/usr/bin/env python3

import ftfy

def fix_encoding(in_file: str, out_file: str) -> None:
    """
    Fix broken unicode in the given file
    Args:
        in_file: filepath of the file to fix
        out_file: filepath of where to save the fixed file
    """

    with open(in_file, "r") as f:
        s = f.read()

    s = ftfy.fix_text(s)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(s)

if __name__ == "__main__":
    fix_encoding("Die_Brasilianische_Katze.md", "Die_Brasilianische_Katze_fixed.md")
