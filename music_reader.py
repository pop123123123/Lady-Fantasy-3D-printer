#!/usr/bin/python3

import argparse

import sheet_parser as sp

def main():
    parser = argparse.ArgumentParser(description="Plays a music sheet")
    parser.add_argument("filename", help="source sheet file")
    parser.add_argument("-t", help="tempo multiplier")
    args = parser.parse_args()

    tempo = 1
    if args.t:
        tempo = 1/float(args.t)


    filename = args.filename
    with open(filename, "r") as f:
        sheet = f.read()

    patterns = sp.parse_sheet(sheet)

    for pattern in patterns:
        pattern.play(tempo=tempo)

if __name__ == "__main__":
    main()
