#!/usr/bin/python3

import tune

intro_notes = [
    tune.Note(tune.Pitch.LA2, 150),
    tune.Note(tune.Pitch.MI3, 150),
    tune.Note(tune.Pitch.LA3, 150),

    tune.Note(tune.Pitch.MI3, 150),
    tune.Note(tune.Pitch.LA3, 150),
    tune.Note(tune.Pitch.MI3, 150)
]
intro = tune.Pattern(intro_notes, nb_loops=4)

bridge = tune.Note(tune.Pitch.MI3, 1000, 0.5)

theme_notes_1 = [
    tune.Note(tune.Pitch.MI3, 500),
    tune.Note(tune.Pitch.FA3, 750),
    tune.Note(tune.Pitch.MI3, 150, 0.1),
    tune.Note(tune.Pitch.MI3, 150, 0.1),
    tune.Note(tune.Pitch.RE3, 150, 0.1),
    tune.Note(tune.Pitch.RE3, 150, 0.1),
    tune.Note(tune.Pitch.DO3, 150, 0.1),
    tune.Note(tune.Pitch.MI3, 750, 0.1),
    tune.Note(tune.Pitch.RE3, 150, 0.1),
    tune.Note(tune.Pitch.DO3, 400, 0.1),
    tune.Note(tune.Pitch.DO3, 400, 0.1),
    tune.Note(tune.Pitch.RE3, 400, 0.3),
    tune.Note(tune.Pitch.DO3, 150, 0.1),
    tune.Note(tune.Pitch.DO3, 150, 0.1),
    tune.Note(tune.Pitch.SI2, 150, 0.1),
    tune.Note(tune.Pitch.SI2, 150, 0.1),
    tune.Note(tune.Pitch.SOLD2, 150, 0.1),
    tune.Note(tune.Pitch.LA2, 500)
]

theme_1 = tune.Pattern(theme_notes_1, nb_loops=2)

theme_notes_2 = [
    tune.Note(tune.Pitch.MI3, 500),
    tune.Note(tune.Pitch.FA3, 700, 0.3),
    tune.Note(tune.Pitch.SOL3, 700, 0.1),
    tune.Note(tune.Pitch.FA3, 250),
    tune.Note(tune.Pitch.MI3, 500, 0.2),
    tune.Note(tune.Pitch.RE3, 150),
    tune.Note(tune.Pitch.MI3, 150),
    tune.Note(tune.Pitch.RE3, 400, 0.1),
    tune.Note(tune.Pitch.DO3, 150, 0.1),
    tune.Note(tune.Pitch.MI3, 150, 0.1),
    tune.Note(tune.Pitch.RE3, 200, 0.3),
    tune.Note(tune.Pitch.DO3, 150, 0.1),
    tune.Note(tune.Pitch.RE3, 200, 0.1),
    tune.Note(tune.Pitch.SI2, 150, 0.1),
    tune.Note(tune.Pitch.DO3, 150, 0.1),
    tune.Note(tune.Pitch.SI2, 150, 0.1),
    tune.Note(tune.Pitch.SOLD2, 250),
    tune.Note(tune.Pitch.LA2, 500)
]

theme_2 = tune.Pattern(theme_notes_2, nb_loops=2)

lady_fantasy = tune.Pattern(tunes=[intro, bridge, theme_1, theme_2], nb_loops=2)
lady_fantasy.play(tempo=0.5)

