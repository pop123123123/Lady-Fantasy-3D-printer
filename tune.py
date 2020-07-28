#!/usr/bin/python3

import enum
import os
import time

class NoteLabel(enum.Enum):
    DO = "DO",
    RE = "RE",
    MI = "MI",
    FA = "FA",
    SOL = "SOL",
    LA = "LA",
    SI = "SI"

class NoteShift(enum.Enum):
    SHARP = "#"
    BEMOL = "b"

#Intervals to LA3
interval_dict = {
    NoteLabel.DO : -9,
    NoteLabel.RE : -7,
    NoteLabel.MI : -5,
    NoteLabel.FA : -4,
    NoteLabel.SOL : -2,
    NoteLabel.LA : 0,
    NoteLabel.SI : 2
}

def note_label_to_freq(note_name, octave, note_shift=None):
    shifter = 0
    if note_shift == NoteShift.SHARP:
        shifter = 1
    if note_shift == NoteShift.BEMOL:
        shifter = -1

    semitone_freq = 1.05946
    la3_freq = 440

    shifted_octave = octave-3
    la3_interval = shifted_octave*12 + interval_dict[note_name] + shifter

    return la3_freq * (semitone_freq**la3_interval)

class Pitch(enum.Enum):
    MI2 = 164.8
    SOLD2 = 207.6
    LA2 = 220.0
    LAD2 = 233.0
    SI2 = 247.5
    DO3 = 264.0
    RE3 = 297.0
    MI3 = 330.0
    FA3 = 352.0
    SOL3 = 392.0
    LA3 = 440.0

class AbstractTune():
    def play(self, tempo=1):
        raise NotImplementedError()

class Pattern(AbstractTune):
    def __init__(self, tunes=[], nb_loops=1):
        self.tunes = tunes
        self.nb_loops = nb_loops

    def add_tune(self, tune):
        self.tunes.append(tune)

    def play(self, tempo=1):
        for _ in range(self.nb_loops):
            for tune in self.tunes:
                tune.play(tempo=tempo)

class Note(AbstractTune):
    def __init__(self, pitch, duration, sleep_time=0):
        self.pitch = pitch
        self.duration = duration
        self.sleep_time = sleep_time

    def play(self, tempo=1):
        os.system("beep -f {} -l {}".format(self.pitch.value, self.duration*tempo))
        time.sleep(self.sleep_time*tempo)

class Silence(AbstractTune):
    def __init__(self, duration):
        self.duration = duration

    def play(self, tempo=1):
        time.sleep(self.duration*tempo)
