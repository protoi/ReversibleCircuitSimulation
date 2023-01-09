import copy
import random
import utilities as utils


def display(num: int, formatting: int) -> str:
    """
    binary representation of a number in string format
    :param num: a number whose binary form is to be displayed
    :type num: int
    :param formatting: number of bits in the binary representation
    :type formatting: int
    :return: a binary string of length formatting which is the binary representation of num
    :rtype: str
    """
    return f'{num:#0{formatting + 2}b}'[2:]


def bit_flipper(num: int, no_of_bits: int) -> int:
    """
    Example: num = 100 and no_of_bits = 5.
    The number is essentially 00100 and the
    flipped version is 11011.
    :param num: the number to be flipped.
    :type num: int
    :param no_of_bits: total number of bits (including leading 0's)
    :type no_of_bits: int
    :return: a flipped version of num
    :rtype: int
    """
    temp = 2 ** (no_of_bits + 1) - 1
    return temp ^ num


class Gate:
    """
    Representation of a single reversible gate.

    Attributes:
        target: an integer whose binary representation denotes which control point is the target of the reversible gate.
            ONLY a single bit in target is 1 and the rest are 0.
            For example: 1000 or 0001000 or 000001 or 00010000000000000.

        inverted_target: bit flipped version of target.
            Used for masking and removing the target bit in `controls`.
            If target is 000100, inverted_target will be 111011.

        controls: an integer whose binary representation denotes what lines are used as the control inputs for the
        reversible gate. For example: 1100101 which means control #0,1,4,6 are used to determine the activation of
        the gate

        number_of_lines: represents how many lines are in the circuit

    """
    target, inverted_target, controls, number_of_lines = None, None, None, None

    def __init__(self, target: int, controls: int, number_of_lines: int):
        self.target = target  # binary number with only one 1-bit
        self.inverted_target = bit_flipper(target, number_of_lines)
        self.controls = controls  # which lines are influence the output
        self.number_of_lines = number_of_lines  # number of input lines total

    def generate_output(self, input_lines: int) -> int:
        """
        :param input_lines: integer whose binary representation denotes the input given to the gate
        :type input_lines: int
        :return: Output of the reversible gates given a certain input.
        :rtype:int
        """

        # inverted_target AND input will set the bit at target location to 0
        masked_input = self.inverted_target & input_lines
        viable_input = masked_input & self.controls
        '''
            when viable_input will be exactly equal to controls if
            every place where controls had a 1, viable input also had a 1
            let's say input: 10010 & controls: 11000
            10010 & 11000 = 10000 which is != controls
            happens because input's 2nd bit is 0 but controls 2nd bit was 1
            if condition fails, gate will not activate (inversion does not happen)
        '''
        if viable_input == self.controls:  # inversion is supposed to happen
            '''
                performing a XOR will invert the bit at targets position(the place where target's 1-bit is present)
                if input_lines = 11101 and target = 00100
                the 3rd bit will get flipped turning into 11001
            '''
            return input_lines ^ self.target
        else:
            return input_lines

    def print_gate_info(self):
        print(display(self.controls, self.number_of_lines))


class Circuit:
    """Representation of a Reversible Circuit

    Attributes:
        number_of_lines: integer that represents the number of control lines in the entire circuit

        cascade_of_gates: a list of Gate class objects.

        starting_data: initial inputs to the circuit, denoted by the binary representation of an integer.

        outputs: a list of outputs of each Gate object in the circuit, where the n-1th output is the nth input.

        smgf: a list of single missing gate faults which can be identified by the starting input.
            It is a boolean list.

        pmgf: a list of partial missing gate faults which can be identified by the starting input.
            It is a list of integers whose binary representation denote which control line can be identified.

    """
    number_of_lines, cascade_of_gates, starting_data, outputs, smgf, pmgf = None, None, None, None, None, None

    def __init__(self, number_of_lines: int):
        self.number_of_lines = number_of_lines  # number of lines in the circuit

    def set_starting_data(self, starting_data: int):
        self.starting_data = starting_data

    def circuit_maker(self, gate_config: list):
        """
        Created a list of Gate objects and stores them in cascade_of_gates
        :param gate_config: a list of dictionaries which contains 2 integers, target and controls.
        :type gate_config: list
        :return: None
        :rtype: None
        """
        self.cascade_of_gates = [
            Gate(config_data['target'], config_data['controls'], self.number_of_lines)
            for config_data in gate_config]

    def circuit_user(self):
        """
        fills the values for smgf and pmgf for a certain gate
        :return: None
        :rtype: None
        """
        '''
            initializing 
                outputs: to be a list of integers pre-initialized to 0
                    and of the same length as number of gates in the circuit.
                smgf: a list of booleans pre-initialized to be False 
                    and have the same length as number of gates in the circuit.
                pmgf: a shallow-copy of outputs
        '''
        self.outputs = [0 for _ in range(len(self.cascade_of_gates))]
        self.smgf = [False for _ in range(len(self.cascade_of_gates))]
        self.pmgf = copy.copy(self.outputs)

        current_output = self.starting_data

        for index, gates in enumerate(self.cascade_of_gates):
            '''
                iterating over gate cascade and using
                the previous output of a gate as the input for the next gate
            '''
            current_input = copy.copy(current_output)
            current_output = gates.generate_output(current_output)
            self.outputs[index] = current_output
            '''
                if every place where controls had a 1 bit, is also 1 in the input.
                This is a test for smgf
            '''
            if current_input & gates.controls == gates.controls:
                self.smgf[index] = True
            # otherwise we check if it is a test for pmgf or not
            else:
                self.pmgf[index] = self.generate_pmgf(current_input, gates)

    def generate_pmgf(self, current_input: int, gates: Gate):
        """
        Example:
        control =   1111 1100
        input =     1010 1010
        set answer's corresponding bit to 1 for every location where control was 1 but input was 0
        which means answer = 0101 0100

        :param current_input: input to the gate, represented by an integer.
        :type current_input: int
        :param gates: Gate object which denotes the current gate of the circuit.
        :type gates: Gate
        :return: which pmgf is being identified by the gate
        :rtype:  int
        """
        temp_controls = gates.controls
        bits_read = 0
        answer = 0
        flag = False

        while temp_controls != 0 or current_input != 0:
            isolator = 0b1
            current_last = current_input & isolator  # extracting the last bit
            gates_last = temp_controls & isolator  # extracting the last bit
            if gates_last == 1 and current_last == 0:
                if flag:  # this is done to remove higher order pmgfs, we only want 1st order pmgfs
                    return 0b0
                answer = answer | 2 ** bits_read
                flag = True

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
    """Random Data set Generator

    Attributes:
        no_of_lines: Number of lines in the circuit.

        no_of_gates: Number of gates in the circuit.

        gate_cascade: A list of Gate objects.
    """
    no_of_lines, no_of_gates = None, None
    gate_cascade = None

    def __init__(self, no_of_lines: int, no_of_gates: int):
        self.no_of_lines = no_of_lines
        self.no_of_gates = no_of_gates

    def display_test_set(self):
        for index, gate in enumerate(self.gate_cascade):
            print(
                f'gate #{index + 1}: target: {display(gate["target"], self.no_of_lines)}\t controls: {display(gate["controls"], self.no_of_lines)}')

    def generate_test_sets(self) -> list:
        # creating a placeholder list of empty dictionaries
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
    # for i in range(2 ** 3):

    # TODO: remove higher order pgmfs
    print('_______________________________________________________')
    for i in range(2 ** 3):
        circ.set_starting_data(i)
        circ.circuit_user()
        circ.print_outputs()
        circ.print_faults()
        print("=================")
        print(circ.smgf)
        print(circ.pmgf)
        print("=================")


def test1():
    ds = DataSet(5, 6)  # 5 input lines and 6 gates
    ds.generate_test_sets()
    ds.display_test_set()


def test2():
    circuit = Circuit(9)
    mydat = [{'target': 0b000010000, 'controls': 0b011000110}]
    circuit.circuit_maker(mydat)
    circuit.set_starting_data(0b011010110)
    circuit.circuit_user()
    circuit.print_outputs()
    circuit.print_faults()
    pass
