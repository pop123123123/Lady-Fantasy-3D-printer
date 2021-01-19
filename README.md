# Lady Fantasy 3D printer player

Interpreter of music sheet for 3d printers.
Outputs a G-code consisting of Y linear moves.

## Get started:
Change `LA3_FREQ` in `tune.py` to your A3 feedrate.
Then just enter
```
./music_reader.py lady_fantasy.sheet
```
To get your G-code.

For all options, `./music_reader --help`

Dependencies:
- parsimonious

## TODO
Use all available stepper motors to output multiple notes at once
