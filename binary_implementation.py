import copy
import random

import utilities as utils


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
        self.inverted_target = utils.bit_flipper(target, number_of_lines)
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
        masked_input = input_lines
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
        print(utils.display(self.controls, self.number_of_lines))


def generate_pmgf(current_input: int, controls: int):
    """
        Example:
        control =   1111 1100
        input =     1010 1010
        set answer's corresponding bit to 1 for every location where control was 1 but input was 0
        which means answer = 0101 0100,
        but we want to drop any higher order pmgfs (any answer with more than 1 set bit)

        :param current_input: input to the gate, represented by an integer.
        :type current_input: int
        :param controls: a binary number which denotes the current gate of the circuit.
        :type controls: int
        :return: which pmgf is being identified by the gate
        :rtype:  int
    """

    answer = ~current_input & controls
    if answer.bit_count() > 1:  # counting set bit
        return 0
    return answer


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
    number_of_lines, cascade_of_gates, starting_data, outputs, smgf, pmgf, mmgf = None, None, None, None, None, None, None

    # pmgf_new = None

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
        self.cascade_of_gates = [Gate(config_data['target'], config_data['controls'], self.number_of_lines) for
                                 config_data in gate_config]

    def circuit_user(self, s=True, p=True, m=True):
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
                mmgf: an empty list that will grow to (no_of_gatesC2) where every element is a 
                    pair (starting gate, ending gate) such that this pair represents the range of gates that
                    goes missing.
        '''
        no_of_gates = len(self.cascade_of_gates)
        self.outputs = [0 for _ in range(no_of_gates)]
        if s:
            self.smgf = [False for _ in range(no_of_gates)]
        if p:
            self.pmgf = [0 for _ in range(no_of_gates)]
        # self.pmgf_new = copy.copy(self.outputs)

        # self.mmgf = [(0, 0) for _ in range((no_of_gates * (no_of_gates - 1)) // 2)]
        if m:
            self.mmgf = []

        current_output = self.starting_data

        # UNCOMMENT FOR STEP-WISE CIRCUIT INPUT
        # print(f"INPUT: {current_output}")

        for index, gate in enumerate(self.cascade_of_gates):
            '''
                iterating over gate cascade and using
                the previous output of a gate as the input for the next gate
            '''
            current_input = copy.copy(current_output)
            current_output = gate.generate_output(current_output)

            # UNCOMMENT FOR STEP-WISE CIRCUIT OUTPUT
            # print(f"{index+1} OUTPUT: {current_output}")

            self.outputs[index] = current_output
            '''
                if every place where controls had a 1 bit, is also 1 in the input.
                This is a test for smgf
            '''
            if current_input & gate.controls == gate.controls:
                if s:
                    self.smgf[
                        index] = True  # need to append current input to this list instead of setting to true or false
                '''
                                                      7 = 00111
                        {'target': 0b10000, 'controls': 0b00111}, -> 0b10111
                        {'target': 0b01000, 'controls': 0b10111}, -> 0b11111
                '''  # print(f'----> for input {current_input}, gate# {index + 1} smgf is handled')
            # otherwise we check if it is a test for pmgf or not
            else:
                # below line was faulty
                if p:
                    self.pmgf[index] = generate_pmgf(current_input, gate.controls)

        # checking for mmgfs
        if m:
            for starting_gate in range(no_of_gates - 1):  # where the gates go missing from
                for ending_gate in range(starting_gate + 1, no_of_gates):  # upto which gate is everything missing
                    output_after_first_gate_removed = self.outputs[starting_gate - 1]

                    # if 1st[0th index] gate goes missing, the circuits original input is propagated up to ending_gate+1
                    if starting_gate == 0:
                        output_after_first_gate_removed = self.starting_data

                    # check for output of  starting_gate - 1 != output of ending_gate -> fault is detectable
                    if output_after_first_gate_removed != self.outputs[ending_gate]:
                        self.mmgf.append((starting_gate, ending_gate))

    def print_outputs(self):
        print(f'for input data: {utils.display(self.starting_data, self.number_of_lines)}')

        for index, outs in enumerate(self.outputs):
            print(f'gate #{index + 1}: output data: ', end='')
            print(utils.display(outs, self.number_of_lines))

    def print_faults(self):
        print(f'smgf:\n{self.smgf}')
        print(f'pmgf:\n{[utils.display(i, self.number_of_lines) for i in self.pmgf]}')
        print(f'mmgf:\n{self.mmgf}')


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
                f'gate #{index + 1}: target: {utils.display(gate["target"], self.no_of_lines)}\t controls: {utils.display(gate["controls"], self.no_of_lines)}')

    def generate_test_sets(self) -> list:
        # creating a placeholder list of empty dictionaries
        self.gate_cascade = [{} for _ in range(self.no_of_gates)]

        for index in range(self.no_of_gates):
            target = 2 ** random.randint(0, self.no_of_lines - 1)  # binary numbers like 1, 10, 100, 1000...
            inverted_target = utils.bit_flipper(target, self.no_of_lines)

            # generate a random number that is not a multiple of 2
            controls = random.randint(0, 2 ** self.no_of_lines - 1)

            # to make sure target location is always 0 for control, we AND it with inverted target
            controls = controls & inverted_target
            self.gate_cascade[index] = {'target': bin(target), 'controls': bin(controls)}
        return self.gate_cascade


def test0():
    no_of_lines = 3
    no_of_gates = 5
    circ = Circuit(3)
    mydata = [{'target': 0b001, 'controls': 0b110},  # 010, 100 -> fault #6 & 7
              {'target': 0b001, 'controls': 0b010},  # 010 -> fault #8
              {'target': 0b001, 'controls': 0b100},  # 100 -> fault #9
              {'target': 0b100, 'controls': 0b011},  # 001, 010 -> fault 10,11
              {'target': 0b100, 'controls': 0b001}]  # 001 -> fault #12
    circ.circuit_maker(mydata)

    fault_map, no_of_total_faults = utils.map_fault_with_index(mydata)
    fault_table = [{"smgf": [], "pmgf": [], "mmgf": []} for _ in range(2 ** no_of_lines)]
    print('_______________________________________________________')
    for circuit_input in range(2 ** no_of_lines):
        # print(utils.display(circuit_input, no_of_lines))
        circ.set_starting_data(circuit_input)
        circ.circuit_user()
        circ.print_outputs()
        # print("=================")
        # circ.print_faults()
        utils.fault_extractor(circ.smgf, circ.pmgf, circ.mmgf, circuit_input, fault_map, fault_table)
        print("pmgf")
        print(circ.pmgf)  # print("new pmgf")  # print(circ.pmgf_new)  # print("=================")
    print(fault_table)
    print(fault_map)
    utils.fault_map_printer(fault_map, no_of_lines)
    utils.plot_graph(fault_table, no_of_lines, no_of_gates, no_of_total_faults - 1)


def test0_0():
    no_of_lines = 5
    no_of_gates = 2
    circ = Circuit(no_of_gates)
    mydata = [{'target': 0b10000, 'controls': 0b00111}, {'target': 0b01000, 'controls': 0b10111}, ]  # 001 -> fault #12
    circ.circuit_maker(mydata)

    fault_map, no_of_total_faults = utils.map_fault_with_index(mydata)
    fault_table = [{"smgf": [], "pmgf": [], "mmgf": []} for _ in range(2 ** no_of_lines)]
    print('_______________________________________________________')
    for circuit_input in range(2 ** no_of_lines):
        # print(utils.display(circuit_input, no_of_lines))
        circ.set_starting_data(circuit_input)
        circ.circuit_user()
        circ.print_outputs()
        # print("=================")
        # circ.print_faults()
        utils.fault_extractor(circ.smgf, circ.pmgf, circ.mmgf, circuit_input, fault_map, fault_table)
        print("pmgf")
        print(circ.pmgf)
        print("SMGF:")
        print(circ.smgf)  # print("new pmgf")  # print(circ.pmgf_new)  # print("=================")
    print(fault_table)
    print(fault_map)
    utils.fault_map_printer(fault_map, no_of_lines)
    utils.plot_graph(fault_table, no_of_lines, no_of_gates, no_of_total_faults - 1)


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


def test4(no_of_lines, no_of_gates):
    ds = DataSet(no_of_lines, no_of_gates)
    ds.generate_test_sets()
    circ = Circuit(no_of_lines)
    circ.circuit_maker(ds.gate_cascade)

    fault_map, no_of_total_faults = utils.map_fault_with_index(ds.gate_cascade)
    fault_table = [{"smgf": [], "pmgf": [], "mmgf": []} for _ in range(2 ** no_of_lines)]

    for circuit_input in range(2 ** no_of_lines):
        circ.set_starting_data(circuit_input)
        circ.circuit_user()
        utils.fault_extractor(circ.smgf, circ.pmgf, circ.mmgf, circuit_input, fault_map, fault_table)

    # print(fault_table)
    # print(fault_map)
    # print(no_of_total_faults - 1)

    utils.plot_graph(fault_table, no_of_lines, no_of_gates, no_of_total_faults - 1)


'''

# this is after just changing the signature to accept an int and slapping njit on it:
from numba import njit

@njit
def generate_pmgf_numba(current_input: int, temp_controls: int):
    bits_read = 0
    answer = 0
    flag = False

    while temp_controls != 0 or current_input != 0:
        isolator = 0b1
        current_last = current_input & isolator  # extracting the last bit
        gates_last = temp_controls & isolator  # extracting the last bit
        if gates_last == 1 and current_last == 0:
            if flag:  # this is done to remove higher order pmgfs, we only want 1st order pmgfs (only a single 1 bit)
                return 0b0
            answer = answer | 2**bits_read
            flag = True

        temp_controls = temp_controls >> 1
        current_input = current_input >> 1
        bits_read += 1

    return answer





yeah, that seems to be just
def generate_pmgf_simple(current_input: int, temp_controls: int) -> int:
    res = ~current_input & temp_controls
    if res.bit_count()>1:
        return 0
    return res
at least, this hypothesis test was unable to find any falsifying examples:
@given(st.integers(0,2**31-1), st.integers(0,2**31-1))
def test_equiv(inp, cont):
    res1 = generate_pmgf(inp, cont)
    res2 = generate_pmgf_simple(inp, cont)
    assert res1==res2, (res1,res2)


'''
