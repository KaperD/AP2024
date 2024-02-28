#!/usr/bin/python3
import sys
import fileinput


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 2:
        print("Too many arguments")
        exit(1)
    try:
        with fileinput.input(files=args[1:2]) as f:
            for i, line in enumerate(f):
                print(i+1, line, end='')
    except OSError as err:
        print(err)
        exit(1)
