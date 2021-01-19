#!/usr/bin/python3

import enum
import os
import time

import repeat_mode as rm

class PitchLabel(enum.Enum):
    DO = "DO"
    RE = "RE"
    MI = "MI"
    FA = "FA"
    SOL = "SOL"
    LA = "LA"
    SI = "SI"

class PitchAccidental(enum.Enum):
    NATURAL = ""
    SHARP = "#"
    FLAT = "b"

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
    def __init__(self, tunes=None, repeat_mode=None):
        if tunes is None:
            tunes = []

        self.tunes = tunes

        if repeat_mode is None:
            self.repeat_mode = rm.SimpleRepeatMode()

    def add_tune(self, tune):
        self.tunes.append(tune)

    def set_repeat_mode(self, repeat_mode):
        self.repeat_mode = repeat_mode

    def play(self, tempo=1):
        for _ in range(self.repeat_mode.get_repeat_number()):
            for tune in self.tunes:
                tune.play(tempo=tempo)

class Pitch():
    def __init__(self, pitch_label, octave, pitch_accidental=PitchAccidental.NATURAL):
        self.pitch_label = pitch_label
        self.octave = octave
        self.pitch_accidental = pitch_accidental

        self.freq = self._compute_freq()


    SEMITONE_FREQ = 1.05946
    LA3_FREQ = 1840

    def _compute_freq(self):
        accidenter = 0
        if self.pitch_accidental == PitchAccidental.SHARP:
            accidenter = 1
        if self.pitch_accidental == PitchAccidental.FLAT:
            accidenter = -1

        accidented_octave = self.octave-3
        la3_interval = accidented_octave*12 + interval_dict[self.pitch_label] + accidenter
        return Pitch.LA3_FREQ * (Pitch.SEMITONE_FREQ**la3_interval)


    def get_freq(self):
        return self.freq

    def __str__(self):
        return self.pitch_label.value + self.pitch_accidental.value + str(self.octave)


print('G90')
print('G0 X0 Y0')
print('G91')
print('M203 X60 Y60')

y = 0
direction = 1
MARGIN = 20
BED_SIZE = 100
def get_size(rate, seconds):
  return seconds * rate / 60

class Note(AbstractTune):
    def __init__(self, pitch, duration):
        self.pitch = pitch
        self.duration = duration

    def play(self, tempo=1):
        global direction, y
        f = round(self.pitch.get_freq(), 2)
        s = round(get_size(f, self.duration * tempo / 1000), 2)
        if s > 30:
            d = self.duration
            self.duration = d / 2
            self.play(tempo)
            self.play(tempo)
            self.duration = d
            return
        if y + s * direction >= BED_SIZE - MARGIN:
            direction = -1
        elif y + s * direction <= MARGIN:
            direction = 1
        s *= direction
        y += s
        print('G0 F{} X{} Y{}'.format(f, 0, s))

    def __str__(self):
        return str(self.pitch) + " " + str(self.duration)


class Silence(AbstractTune):
    def __init__(self, duration):
        self.duration = duration

    def play(self, tempo=1):
        print('G4 S{}'.format(self.duration*tempo))

    def __str__(self):
        return "s", str(self.duration)
