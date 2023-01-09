import copy


class Gate:
    target_line = None
    control_lines = None  # a list of lines to be activated

    def __init__(self, target, controls):
        self.target_line = target
        self.control_lines = controls  # array list

    def how_many_0_and_1(self, arr):
        ones = arr.count(1)
        zeros = len(arr) - ones
        return ones, zeros

    def generate_output(self, input_lines):
        output_lines = copy.copy(input_lines)

        # will be true if all given control lines == 1
        # (C1 AND C2 AND C3..)

        ones, zeros = self.how_many_0_and_1([input_lines[c] for c in self.control_lines])
        and_of_control_lines = 1 if zeros == 0 else 0  # no 0 present in control lines for the gate
        output_lines[self.target_line] = output_lines[
                                             self.target_line] ^ and_of_control_lines  # target XOR (C1 ^ C2 ^ C3..)

        return output_lines, zeros

    def print_gate_info(self):
        print(f'''target line: {self.target_line}
control lines: {self.control_lines}''')

    pass


class Inputs:
    input_data = []

    def __init__(self, data):
        self.input_data = data

    def print_data(self):
        print(self.input_data)

    pass


class Circuit:
    numberOfLines = None
    cascade_of_gates = None
    starting_data = None
    outputs = None
    smgf = None
    pmgf = None

    def __init__(self, num):
        self.numberOfLines = num  # number of input lines that will be present in the circuit
        self.cascade_of_gates = None

    def set_starting_data(self, start):
        self.starting_data = start.input_data

    def circuit_maker(self, gate_config):
        self.cascade_of_gates = [None for _ in range(len(gate_config))]

        self.smgf = [False for _ in range(len(gate_config))]
        self.pmgf = [False for _ in range(len(gate_config))]

        for index, config_data in enumerate(gate_config):  # creates a list of gates
            self.cascade_of_gates[index] = Gate(config_data['target'], config_data['controls'])

    def circuit_user(self):
        self.outputs = [None for _ in range(len(self.cascade_of_gates))]
        current_output = self.starting_data

        for index, gates in enumerate(self.cascade_of_gates):

            current_output, zeros = gates.generate_output(current_output)

            if zeros == 0:  # no zero in selected inputs = smgf
                self.smgf[index] = True
            elif zeros > 0:  # pmfg
                current_inputs = copy.copy(current_output)
                # print(f"current inputs: {current_inputs}")
                # print(f"gate controls: {gates.control_lines}")

                self.pmgf[index] = [c for c in gates.control_lines if current_inputs[c] == 0]
            # print(f"number of zeros: {zeros} for gate # {index}")
            self.outputs[index] = current_output

    def print_outputs(self):
        print(f"for input data: {self.starting_data}")
        for index, outs in enumerate(self.outputs):
            print(f"gate #{index + 1} output data: {outs}")

    def print_faults(self):
        print("_____________________________")
        print(f"For input signal: {self.starting_data}")
        print("single missing gate faults: ", end='')
        print(self.smgf)
        print("partial missing gate faults: ", end='')
        print(self.pmgf)


def test0():
    print("___________________TEST 0___________________")
    circ = Circuit(3)
    circ.set_starting_data(Inputs([1, 0, 0]))
    mydata = [{'target': 2, 'controls': [0, 1]},
              {'target': 2, 'controls': [1]},
              {'target': 2, 'controls': [0]},
              {'target': 0, 'controls': [1, 2]},
              {'target': 0, 'controls': [2]}]
    # circ.circuit_maker()
    circ.circuit_maker(mydata)
    circ.circuit_user()
    circ.print_outputs()
    circ.print_faults()
    del circ
    del mydata


def test0_1():
    print("___________________TEST 0.1___________________")
    circ = Circuit(3)
    circ.set_starting_data(Inputs([1, 1, 1]))
    mydata = [{'target': 2, 'controls': [0, 1]},
              {'target': 2, 'controls': [1]},
              {'target': 2, 'controls': [0]},
              {'target': 0, 'controls': [1, 2]},
              {'target': 0, 'controls': [2]}]
    # circ.circuit_maker()
    circ.circuit_maker(mydata)
    circ.circuit_user()
    circ.print_outputs()
    circ.print_faults()
    del circ
    del mydata


def test1():
    print("___________________TEST 1___________________")
    circ = Circuit(5)
    circ.set_starting_data(Inputs([1, 1, 0, 1, 0]))
    mydata = [{'target': 4, 'controls': [0, 1, 3]},
              {'target': 3, 'controls': [1, 2, 4]},
              {'target': 0, 'controls': [1, 3, 4]},
              {'target': 0, 'controls': []}]
    # circ.circuit_maker()

    circ.circuit_maker(mydata)
    circ.circuit_user()
    circ.print_outputs()
    circ.print_faults()
