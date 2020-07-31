import parsimonious
import tune

grammar = parsimonious.grammar.Grammar(
    r"""
    entry = declarative? ws sheet ws
    declarative = "DECLARE:" ws declare_tune+ ws
    declare_tune = name inline_ws ":=" inline_ws anonym_tune ws

    sheet = "BEGIN:" ws tune+ ws

    tune = (anonym_tune / named_tune) ws

    named_tune = name ws
    anonym_tune = block / sound

    block = opening_block ws tune* ws "}" ws repeater? ws
    opening_block = "{"
    repeater = "*" ws repeat_counter
    repeat_counter = ~"\d+"

    sound = note / silence

    note = pitch ws duration ws sleep_time? ws
    pitch = pitch_label shifter? octave
    pitch_label = "DO" / "RE" / "MI" / "FA" / "SOL" / "LA" / "SI"
    shifter = "#" / "b"
    octave = ~"\d+"

    silence = "s"? ws sleep_time
    duration = ~"\d+"
    sleep_time = ~"\d*.\d+"

    name = ~"[A-Z 0-9]+"i
    ws = ~"\s*"
    inline_ws = ~"[ \t]*"
    """
)

class SheetVisitor(parsimonious.nodes.NodeVisitor):
    def __init__(self):
        self.allfather_pattern = tune.Pattern([])
        self.patterns = [self.allfather_pattern]

        self.current_name = None

        self.current_tune = None

        self.declarations = {}

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

    def visit_name(self, node, children):
        self.current_name = node.text.strip()

    def visit_declare_tune(self, node, children):
        self.declarations[self.current_name] = self.current_tune

        self.current_name = None
        self.current_tune = None

    def visit_opening_block(self, node, children):
        # TODO: en enlevant les [] ca fait de la merde
        self.patterns.append(tune.Pattern([]))

    def visit_repeat_counter(self, node, children):
        self.get_current_pattern().nb_loops = int(node.text)

    def visit_block(self, node, children):
        closed_block = self.patterns.pop()
        self.current_tune = closed_block

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

    def visit_named_tune(self, node, children):
        #if self.current_name not in self.declarations:
        #    raise parsimonious.exceptions.ParseError("Pattern {} never been declared".format(node.text))

        self.current_tune = self.declarations[self.current_name]

        self.current_name = None

    def visit_tune(self, node, children):
        current_pattern = self.get_current_pattern()
        current_pattern.add_tune(self.current_tune)

        self.current_tune = None

    def visit_note(self, node, children):
        local_pattern = tune.Pattern([])

        note = tune.Note(self.current_pitch, self.current_note_duration)
        local_pattern.add_tune(note)

        if self.current_pitch_sleep_time is not None:
            silence = tune.Silence(self.current_pitch_sleep_time)
            local_pattern.add_tune(silence)

        self.current_tune = local_pattern

        self.current_pitch = None
        self.current_pitch_duration = None
        self.current_pitch_sleep_time = None

    def visit_silence(self, node, children):
        self.current_tune = tune.Silence(self.current_pitch_sleep_time)

def parse_sheet(sheet):
    tree = grammar.parse(sheet)
    sv = SheetVisitor()
    sv.visit(tree)
    return sv.allfather_pattern
