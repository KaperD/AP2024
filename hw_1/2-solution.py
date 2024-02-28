#!/usr/bin/python3
import sys
import fileinput
import collections

def process_one(file: str, number_of_lines: int):
    last_lines = collections.deque(maxlen=number_of_lines)
    try:
        with fileinput.input(files=file) as f:
            for line in f:
                last_lines.append(line)
    except OSError as err:
        print(err)
        exit(1)
    for line in last_lines:
        print(line, end='')


if __name__ == "__main__":
    args = sys.argv
    number_of_lines_for_files = 10
    number_of_lines_for_stdin = 17
    if len(args) < 2:
        process_one(None, number_of_lines_for_stdin)
    elif len(args) == 2:
        process_one(args[1], number_of_lines_for_files)
    else:
        is_first = True
        for file_name in args[1:]:
            if not is_first:
                print()
            is_first = False
            print(f"==> {file_name} <==")
            process_one(file_name, number_of_lines_for_files)
