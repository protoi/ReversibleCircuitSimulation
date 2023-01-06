import copy


def display(num, formatting):
    print(f'{num:#0{formatting + 2}b}')


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
        display(self.controls, self.number_of_lines)


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
                answer = self.generate_pmgf(current_input, gates)
                self.pmgf[index] = answer

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
        print(f'for input data: ')
        display(self.starting_data, self.number_of_lines)

        for index, outs in enumerate(self.outputs):
            print(f'gate #{index + 1}: output data: ', end='')
            display(outs, self.number_of_lines)

    def print_faults(self):
        print(f'smgf:\n{self.smgf}')
        print(f'pmgf:\n{[f"{i:#0{self.number_of_lines + 2}b}" for i in self.pmgf]}')


def test0():
    circ = Circuit(3)
    mydata = [{'target': 0b001, 'controls': 0b110},
              {'target': 0b001, 'controls': 0b010},
              {'target': 0b001, 'controls': 0b100},
              {'target': 0b100, 'controls': 0b011},
              {'target': 0b100, 'controls': 0b001}]
    circ.circuit_maker(mydata)
    for i in range(2 ** 3):
        circ.set_starting_data(i)
        circ.circuit_user()
        circ.print_outputs()
        circ.print_faults()
