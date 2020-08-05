import random

class AbstractRepeatMode():
    def set_repeat_number(self, *args):
        raise NotImplementedError()

    def get_repeat_number(self):
        raise NotImplementedError()

class SimpleRepeatMode(AbstractRepeatMode):
    def __init__(self, nb_loops=1):
        self.nb_loops = nb_loops

    def set_repeat_number(self, *args):
        assert(len(args) == 1)
        nb_loops = args[0]
        assert(isinstance(nb_loops, int))

        self.nb_loops = nb_loops

    def get_repeat_number(self):
        return self.nb_loops

class RandomRepeatMode(AbstractRepeatMode):
    def __init__(self, min_repeats, max_repeats, base=1):
        self.min_repeats = min_repeats
        self.max_repeats = max_repeats
        self.base = base

    def set_repeat_number(self, *args):
        assert(len(args) == 3)
        min_repeats = args[0]
        max_repeats = args[1]
        base = args[2]
        assert(isinstance(min_repeats, int))
        assert(isinstance(max_repeats, int))
        assert(isinstance(base, int))

        self.min_repeats = min_repeats
        self.max_repeats = max_repeats
        self.base = base

    def get_repeat_number(self):
        return random.randint(self.min_repeats, self.max_repeats)*self.base
