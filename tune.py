#!/usr/bin/python3

import enum
import os
import time

class PitchLabel(enum.Enum):
    DO = "DO"
    RE = "RE"
    MI = "MI"
    FA = "FA"
    SOL = "SOL"
    LA = "LA"
    SI = "SI"

class PitchShift(enum.Enum):
    NORMAL = ""
    SHARP = "#"
    BEMOL = "b"

PitchLabelDict = {
    "A" : PitchLabel.LA,
    "B" : PitchLabel.SI,
    "C" : PitchLabel.DO,
    "D" : PitchLabel.RE,
    "E" : PitchLabel.MI,
    "F" : PitchLabel.FA,
    "G" : PitchLabel.SOL,
    "DO" : PitchLabel.DO,
    "RE" : PitchLabel.RE,
    "MI" : PitchLabel.MI,
    "FA" : PitchLabel.FA,
    "SOL" : PitchLabel.SOL,
    "LA" : PitchLabel.LA,
    "SI" : PitchLabel.SI,
}


#Intervals to LA3
interval_dict = {
    PitchLabel.DO : -9,
    PitchLabel.RE : -7,
    PitchLabel.MI : -5,
    PitchLabel.FA : -4,
    PitchLabel.SOL : -2,
    PitchLabel.LA : 0,
    PitchLabel.SI : 2
}


class AbstractTune():
    def play(self, tempo=1):
        raise NotImplementedError()

class Pattern(AbstractTune):
    def __init__(self, tunes=None, nb_loops=1):
        if tunes is None:
            tunes = []

        self.tunes = tunes
        self.nb_loops = nb_loops

    def add_tune(self, tune):
        self.tunes.append(tune)

    def play(self, tempo=1):
        for _ in range(self.nb_loops):
            for tune in self.tunes:
                tune.play(tempo=tempo)

class Pitch():
    def __init__(self, pitch_label, octave, pitch_shift=PitchShift.NORMAL):
        self.pitch_label = pitch_label
        self.octave = octave
        self.pitch_shift = pitch_shift

        self.freq = self._compute_freq()


    SEMITONE_FREQ = 1.05946
    LA3_FREQ = 440

    def _compute_freq(self):
        shifter = 0
        if self.pitch_shift == PitchShift.SHARP:
            shifter = 1
        if self.pitch_shift == PitchShift.BEMOL:
            shifter = -1

        shifted_octave = self.octave-3
        la3_interval = shifted_octave*12 + interval_dict[self.pitch_label] + shifter
        return Pitch.LA3_FREQ * (Pitch.SEMITONE_FREQ**la3_interval)


    def get_freq(self):
        return self.freq

    def __str__(self):
        return self.pitch_label.value + self.pitch_shift.value + str(self.octave)

class Note(AbstractTune):
    def __init__(self, pitch, duration):
        self.pitch = pitch
        self.duration = duration

    def play(self, tempo=1):
        os.system("beep -f {} -l {}".format(self.pitch.get_freq(), self.duration*tempo))


    def __str__(self):
        return str(self.pitch) + " " + str(self.duration)


class Silence(AbstractTune):
    def __init__(self, duration):
        self.duration = duration

    def play(self, tempo=1):
        time.sleep(self.duration*tempo)

    def __str__(self):
        return "s", str(self.duration)
