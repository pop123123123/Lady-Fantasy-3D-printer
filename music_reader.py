#!/usr/bin/python3

import argparse

import sheet_parser as sp

def main():
    parser = argparse.ArgumentParser(description="Plays a music sheet")
    parser.add_argument("filename", help="source sheet file")
    parser.add_argument("-s", "--string", action="store_true", help="read the music from a string")
    parser.add_argument("-t", "--tempo", help="tempo multiplier")
    args = parser.parse_args()

    tempo = 1
    if args.tempo:
        tempo = 1/float(args.tempo)

    if args.string:
        sheet = args.filename
    else:
        filename = args.filename
        with open(filename, "r") as f:
            sheet = f.read()

    melody = sp.parse_sheet(sheet)
    melody.play(tempo=tempo)

if __name__ == "__main__":
    main()
