#!/usr/bin/python3
import sys
import os
import fileinput
import re


def process_one(file: str) -> tuple[int, int, int]:
    lines = 0
    words = 0
    symbols = 0
    try:
        with fileinput.input(files=file) as f:
            for line in f:
                lines += line.endswith(os.linesep)
                words += len(re.findall(r"\S+", line))
                symbols += len(line.encode('utf-8'))
    except OSError as err:
        print(err)
        exit(1)
    return lines, words, symbols


def print_one(lines: int, words: int, symbols: int, file: str):
    max_len = max(len(str(lines)), len(str(words)), len(str(symbols)))
    wanted_width = max(max_len + 1, 8)
    print(f"{{:>{wanted_width}}}{{:>{wanted_width}}}{{:>{wanted_width}}}".format(
        lines, words, symbols), end='')
    if file is not None:
        print(f" {file}")
    else:
        print()


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print_one(*process_one(None), None)
    else:
        total_lines = 0
        total_words = 0
        total_symbols = 0
        for file_name in args[1:]:
            lines, words, symbols = process_one(file_name)
            total_lines += lines
            total_words += words
            total_symbols += symbols
            print_one(lines, words, symbols, file_name)
        if len(args) > 2:
            print_one(total_lines, total_words, total_symbols, "total")
