import parsimonious
import tune

grammar = parsimonious.grammar.Grammar(
    r"""
    entry = block+ ws
    block = opening_block ws tune* ws "}" ws ("*" repeat)?
    opening_block = "{"
    tune = block / sound
    sound = note / silence
    note = pitch ws duration ws sleep_time? ws
    silence = "s"? ws sleep_time
    duration = ~"\d+"
    sleep_time = ~"\d*.\d+"
    pitch = pitch_label shifter? octave
    pitch_label = "DO" / "RE" / "MI" / "FA" / "SOL" / "LA" / "SI"
    shifter = "#" / "b"
    octave = ~"\d+"
    repeat = ~"\d+"
    ws = ~"\s*"
    """
)

class SheetVisitor(parsimonious.nodes.NodeVisitor):
    def __init__(self):
        self.patterns = []

        self.current_pitch_label = None
        self.current_pitch_shift = None
        self.current_pitch_octave = None
        self.current_pitch_freq = None

        self.current_pitch = None
        self.current_pitch_duration = None
        self.current_pitch_sleep_time = None

        self.root_blocks = []

    def get_current_pattern(self):
        if self.patterns == []:
            return None
        return self.patterns[-1]

    def generic_visit(self, node, children):
        pass

    def visit_entry(self, node, children):
        pass

    def visit_opening_block(self, node, children):
        # TODO: en enlevant les [] ca fait de la merde
        new_pattern = tune.Pattern([])

        current_pattern = self.get_current_pattern()
        if current_pattern is not None:
            current_pattern.add_tune(new_pattern)

        # New pattern becomes current pattern
        self.patterns.append(new_pattern)

    def visit_repeat(self, node, children):
        self.get_current_pattern().nb_loops = int(node.text)

    def visit_block(self, node, children):
        closed_block = self.patterns.pop()
        if self.patterns == []:
            self.root_blocks.append(closed_block)

    def visit_pitch_label(self, node, children):
        self.current_pitch_label = tune.PitchLabel(node.text)

    def visit_shifter(self, node, children):
        self.current_pitch_shift = tune.PitchShift(node.text)

    def visit_octave(self, node, children):
        self.current_pitch_octave = int(node.text)

    def visit_pitch(self, node, children):
        if self.current_pitch_shift is None:
            self.current_pitch_shift = tune.PitchShift.NORMAL

        self.current_pitch = tune.Pitch(self.current_pitch_label, self.current_pitch_octave, self.current_pitch_shift)

        self.current_pitch_label = None
        self.current_pitch_shift = None
        self.current_pitch_octave = None

    def visit_duration(self, node, children):
        self.current_note_duration = int(node.text)

    def visit_sleep_time(self, node, children):
        self.current_pitch_sleep_time = float(node.text)

    def visit_note(self, node, children):
        current_pattern = self.get_current_pattern()

        note = tune.Note(self.current_pitch, self.current_note_duration)
        current_pattern.add_tune(note)

        if self.current_pitch_sleep_time is not None:
            silence = tune.Silence(self.current_pitch_sleep_time)
            current_pattern.add_tune(silence)

        self.current_pitch = None
        self.current_pitch_duration = None
        self.current_pitch_sleep_time = None

    def visit_silence(self, node, children):
        father = self.get_current_pattern()
        father.add_tune(tune.Silence(int(node.text)))
