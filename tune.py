#!/usr/bin/python3

import enum
import os
import time

def note_label_to_freq(note_name, note_shift, octave):
    pass

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
