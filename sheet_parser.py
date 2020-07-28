import parsimonious
import tune

grammar = parsimonious.grammar.Grammar(
    r"""
    entry = block+
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

        self.current_note_label = None
        self.current_note_shift = None
        self.current_note_octave = None
        self.current_note_freq = None

        self.current_note_freq = None
        self.current_note_duration = None
        self.current_note_sleep_time = None

        self.root_blocks = []

    def get_current_pattern(self):
        if not self.patterns:
            return None
        return self.patterns[-1]

    def generic_visit(self, node, children):
        pass

    def visit_entry(self, node, children):
        pass

    def visit_opening_block(self, node, children):
        current_pattern = tune.Pattern()

        new_pattern = tune.Pattern()
        self.patterns.append(new_pattern)

        if current_pattern is not None:
            current_pattern.add_tune(new_pattern)

    def visit_repeat(self, node, children):
        self.get_current_pattern().nb_loops = int(node.text)

    def visit_block(self, node, children):
        closed_block = self.patterns.pop()
        if self.patterns == []:
            self.root_blocks.append(closed_block)


    def visit_pitch_label(self, node, children):
        self.current_note_label = node.text

    def visit_shifter(self, node, children):
        self.current_note_shift = node.text

    def visit_octave(self, node, children):
        self.current_note_octave = node.text

    def visit_pitch(self, node, children):
        self.current_note_freq = tune.note_label_to_freq(self.current_note_label, self.current_note_shift, self.current_note_octave)
        self.current_note_label = None
        self.current_note_shift = None
        self.current_note_octave = None

    def visit_duration(self, node, children):
        self.current_note_duration = node.text

    def visit_sleep_time(self, node, children):
        self.current_note_sleep_time = node.text

    def visit_note(self, node, children):
        current_pattern = self.get_current_pattern()

        note = tune.Note(self.current_note_freq, self.current_note_duration)
        current_pattern.add_tune(note)

        if self.current_note_sleep_time is not None:
            silence = tune.Silence(self.current_note_sleep_time)
            current_pattern.add_tune(silence)

        self.current_note_freq = None
        self.current_note_duration = None
        self.current_note_sleep_time = None

    def visit_silence(self, node, children):
        father = self.get_current_pattern()
        father.add_tune(tune.Silence(int(node.text)))

notes = ["{ DO#5 1000 0.8 { RE1 50 0.5}*2}"]

for note in notes:
    tree = grammar.parse(note)
    sv = SheetVisitor()
    sv.visit(tree)

    for block in sv.root_blocks:
        pass

