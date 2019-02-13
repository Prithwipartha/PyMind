constant = {
    'pi': 3.14159,
    'e': 2.71828,
    'golden_ratio': 1.61803
}


class MatheMagics(object):
    def __init__(self, string='', name='not named'):
        self.list = []
        self.vars = {}
        self.name = None
        self.segments = []

        self.get_body(string, name)
        self.describe(show_name=True)

    def get_body(self, string='', name=''):
        if string is not '':
            string = string.split()
            for i in range(len(string)):
                try:
                    string[i] = int(string[i])
                except ValueError:
                    pass
                if type(string[i]) is not int:
                    if string[i].isdecimal():
                        string[i] = float(string[i])
            self.list = string
            self.renew_variables()
            if name is not '':
                self.name = name

    def get_type(self):
        ret = None
        for i in self.list:
            if i is '=':
                ret = 'Equation'

        if ret is None:
            ret = 'Expression'
        return ret

    def __repr__(self):
        string = ''
        string += '=>  '
        for i in self.list:
            string += str(i) + ' '
        return string

    def describe(self, show_name=False):
        if show_name:
            print(self.get_type() + ':' + self.name)
        print(self)
        self.show_variables()

    def set_value(self, variable, value):
        self.vars[variable] = value

    def renew_variables(self):
        self.vars = {}
        for i in self.list:
            if type(i) is str:
                if i.isalpha():
                    try:
                        self.vars[i]
                    except KeyError:
                        self.vars[i] = None

    def show_variables(self):
        print('   Variable' + '  ' + ': ' + 'Value')
        keys = list(self.vars.keys())
        for i in range(len(keys)):
            print(str(i + 1) + ') ' + keys[i] + str(' ' * (10-len(keys[i]))) + ': ' + str(self.vars[keys[i]]))

    def plot(self):
        pass


class Equation(MatheMagics):
    def __init__(self, string, name):
        MatheMagics.__init__(self, string, name)


class Expression(MatheMagics):
    def __init__(self, string, name):
        MatheMagics.__init__(self, string, name)


class Tape(object):
    blank_symbol = " "

    def __init__(self,
                 tape_string=""):
        self.__tape = dict((enumerate(tape_string)))
        # last line is equivalent to the following three lines:
        # self.__tape = {}
        # for i in range(len(tape_string)):
        #    self.__tape[i] = input[i]

    def __str__(self):
        s = ""
        min_used_index = min(self.__tape.keys())
        max_used_index = max(self.__tape.keys())
        for i in range(min_used_index, max_used_index):
            s += self.__tape[i]
        return s

    def __getitem__(self, index):
        if index in self.__tape:
            return self.__tape[index]
        else:
            return Tape.blank_symbol

    def __setitem__(self, pos, char):
        self.__tape[pos] = char


class TuringMachine(object):

    def __init__(self,
                 tape="",
                 blank_symbol=" ",
                 initial_state="",
                 final_states=None,
                 transition_function=None):
        self.__tape = Tape(tape)
        self.__head_position = 0
        self.__blank_symbol = blank_symbol
        self.__current_state = initial_state
        if transition_function is None:
            self.__transition_function = {}
        else:
            self.__transition_function = transition_function
        if final_states is None:
            self.__final_states = set()
        else:
            self.__final_states = set(final_states)

    def get_tape(self):
        return str(self.__tape)

    def step(self):
        char_under_head = self.__tape[self.__head_position]
        x = (self.__current_state, char_under_head)
        if x in self.__transition_function:
            y = self.__transition_function[x]
            self.__tape[self.__head_position] = y[1]
            if y[2] == "R":
                self.__head_position += 1
            elif y[2] == "L":
                self.__head_position -= 1
            self.__current_state = y[0]

    def final(self):
        if self.__current_state in self.__final_states:
            return True
        else:
            return False
