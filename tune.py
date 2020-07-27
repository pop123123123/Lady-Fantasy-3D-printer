#!/usr/bin/python3

import enum

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
    def __init__(self, notes=[]):
        self.notes = notes

    def add_note(self, note):
        self.notes.append(note)

class Note(AbstractTune):
    def __init__(self, pitch, duration, sleep):
        self.pitch = pitch
        self.duration = duration
        self.sleep = sleep


def main():
    pass
