import copy
import random


def display(num, formatting):
    return f'{num:#0{formatting + 2}b}'[2:]


def bit_flipper(num, no_of_bits):
    temp = 2 ** (no_of_bits + 1) - 1
    return temp ^ num


class Gate:
    target, inverted_target, controls, number_of_lines = None, None, None, None

    def __init__(self, target, controls, number_of_lines):
        self.target = target  # binary number with only one 1-bit
        self.inverted_target = bit_flipper(target, number_of_lines)
        self.controls = controls  # which lines are influence the output
        self.number_of_lines = number_of_lines  # number of input lines total

    def generate_output(self, input_lines):
        masked_input = self.inverted_target & input_lines
        viable_input = masked_input & self.controls
        if viable_input == self.controls:  # inversion is supposed to happen
            return input_lines ^ self.target
        else:
            return input_lines

    # old input -> 101 & 110 -> 100
    # 100 == 100

    def print_gate_info(self):
        print(display(self.controls, self.number_of_lines))


class Circuit:
    number_of_lines, cascade_of_gates, starting_data, outputs, smgf, pmgf = None, None, None, None, None, None

    def __init__(self, number_of_lines):
        self.number_of_lines = number_of_lines  # number of lines in the circuit

    def set_starting_data(self, starting_data):
        self.starting_data = starting_data

    def circuit_maker(self, gate_config):
        self.cascade_of_gates = [
            Gate(config_data['target'], config_data['controls'], self.number_of_lines)
            for config_data in gate_config]

    def circuit_user(self):
        self.outputs = [None for _ in range(len(self.cascade_of_gates))]
        current_output = self.starting_data

        self.smgf = [False for _ in range(len(self.cascade_of_gates))]
        self.pmgf = copy.copy(self.smgf)

        for index, gates in enumerate(self.cascade_of_gates):
            current_input = copy.copy(current_output)
            current_output = gates.generate_output(current_output)
            self.outputs[index] = current_output
            # smgf #
            if current_input & gates.controls == gates.controls:
                self.smgf[index] = True
            # pmgf #
            else:
                self.pmgf[index] = self.generate_pmgf(current_input, gates)

    def generate_pmgf(self, current_input, gates):
        temp_controls = gates.controls
        bits_read = 0
        answer = 0
        while temp_controls != 0 and current_input != 0:
            isolator = 0b1
            current_last = current_input & isolator
            gates_last = temp_controls & isolator
            if gates_last == 1 and current_last == 0:
                # print(1)
                answer = answer | 2 ** bits_read

            temp_controls = temp_controls >> 1
            current_input = current_input >> 1
            bits_read += 1
        return answer

    def print_outputs(self):
        print(f'for input data: {display(self.starting_data, self.number_of_lines)}')

        for index, outs in enumerate(self.outputs):
            print(f'gate #{index + 1}: output data: ', end='')
            print(display(outs, self.number_of_lines))

    def print_faults(self):
        print(f'smgf:\n{self.smgf}')
        print(f'pmgf:\n{[display(i, self.number_of_lines) for i in self.pmgf]}')


class DataSet:
    no_of_lines, no_of_gates = None, None
    gate_cascade = None

    def __init__(self, no_of_lines, no_of_gates):
        self.no_of_lines = no_of_lines
        self.no_of_gates = no_of_gates

    def display_test_set(self):
        for index, gate in enumerate(self.gate_cascade):
            print(
                f'gate #{index + 1}: target: {display(gate["target"], self.no_of_lines)}\t controls: {display(gate["controls"], self.no_of_lines)}')

    def generate_test_sets(self):
        self.gate_cascade = [{} for _ in range(self.no_of_gates)]
        for index in range(self.no_of_gates):
            target = 2 ** random.randint(0, self.no_of_lines - 1)  # binary numbers like 1, 10, 100, 1000...
            inverted_target = bit_flipper(target, self.no_of_lines)
            # generate a random number that is not a multiple of 2
            controls = random.randint(0, 2 ** self.no_of_lines - 1)
            # to make sure target location is always 0 for control, we AND it with inverted target
            controls = controls & inverted_target
            self.gate_cascade[index] = {'target': target, 'controls': controls}
        return self.gate_cascade


def test0():
    circ = Circuit(3)
    mydata = [{'target': 0b001, 'controls': 0b110},
              {'target': 0b001, 'controls': 0b010},
              {'target': 0b001, 'controls': 0b100},
              {'target': 0b100, 'controls': 0b011},
              {'target': 0b100, 'controls': 0b001}]
    circ.circuit_maker(mydata)
    for i in range(2 ** 3):
        print('_______________________________________________________')
        circ.set_starting_data(i)
        circ.circuit_user()
        circ.print_outputs()
        circ.print_faults()


def test1():
    ds = DataSet(5, 6)  # 5 input lines and 6 gates
    ds.generate_test_sets()
    ds.display_test_set()
