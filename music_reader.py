#!/usr/bin/python3

import sys

import sheet_parser as sp

def main():
    if len(sys.argv) != 2:
        print("Usage: {} filename".format(sys.argv[0]))
        exit(0)

    filename = sys.argv[1]
    with open(filename, "r") as f:
        sheet = f.read()

    patterns = sp.parse_sheet(sheet)

    for pattern in patterns:
        pattern.play()

if __name__ == "__main__":
    main()
