import matplotlib.pyplot as plt


def produce_multiples_of_2(n: int) -> list[int]:
    """
    takes a number like 110100 and returns a list containing [100000, 010000, 000100]
    When you perform a logical OR on the list or add these numbers up
    it results in the original value of n
    :param n: an integer
    :type n: int
    :return: a list of numbers(powers of 2) when added up produce n
    :rtype: list[int]
    """
    count = 0
    answer = []
    while n != 0:
        if n & 0b1 == 1:
            answer.append(2 ** count)
        n = n >> 1
        count += 1
    return answer


def fault_map_printer(fault_map, control_lines):
    for index, (key, val) in enumerate(fault_map.items()):
        if isinstance(key, int):
            print(f"fault No.{val} = smgf for gate No.{key + 1}")
        elif isinstance(key[0], int):
            print(f"fault No.{val} = pmgf for missing control {display(key[1], control_lines)} at gate {key[0] + 1}")
        else:
            print(f"fault No.{val} = mmgf for gate range {key[0]}, {key[1]}")


def map_fault_with_index(cascade_of_gates: list[dict]) -> tuple[dict[int | tuple[int, int], int], int]:
    """
    takes the gate cascade, and assigns every possible fault a number.
    If the gate cascade has G gates, integer between 1 and G are mapped with smgfs.
    Number of pmgfs for any gate = number of controls for that gate.
    Total number of pmgfs = summation of every gate's pmgfs.
    Each pmgf is represented as a tuple with 2 values, (gate number, which control line is faulty).
    We only consider 1st order Pmgfs.

    gate number -> 0 indexed.
    line is faulty -> binary representation for example 000100 is the 4th control line.

    :param cascade_of_gates: a list of dictionaries comprising targets and control lines for a gate.
    :type cascade_of_gates: list[dict[string: int, string: int]]
    :return: 1. a dictionary with fault - integer mapping. Mapping starts from 1 to no of total faults.
        If a circuit has G gates, first G faults are smgfs. Rest pmgfs.
        2. Count of total number of faults in the circuit.
    :rtype: dict
    """
    # count = len(cascade_of_gates) + 1  # we want to start numbering pmgfs after smgfs
    tempdict = {}

    count = 1
    for index in range(len(cascade_of_gates)):  # accommodating for smgf
        tempdict[index] = count
        count += 1
    for index, gate in enumerate(cascade_of_gates):  # accommodating for pmgf
        subparts = produce_multiples_of_2(gate['controls'])  # if input= 11010, output= [10000, 1000, 10]
        for s in subparts:
            tempdict[(index, s)] = count  # (3,4)
            count += 1

    for starting_gate in range(len(cascade_of_gates) - 1):
        for ending_gate in range(starting_gate + 1, len(cascade_of_gates)):
            tempdict[(f'G{starting_gate + 1}', f'G{ending_gate + 1}')] = count
            count += 1

    return tempdict, count


def counter_controls(cascade_of_gates: list[dict]) -> int:
    """
    counts the number of set bits in every gates 'control' for a given circuit.
    :param cascade_of_gates: a cascade of gates, basically a circuit
    :type cascade_of_gates: list[dict[string: int, string: int]]
    :return: number of set bits in the entire circuits controls
    :rtype: int
    """
    counter = 0
    for gate in cascade_of_gates:
        counter += (gate['controls']).bit_count()
    return counter


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
    flips the bits of the input and appends 1s to the front for specific lengths.
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
    temp = (1 << no_of_bits) - 1
    return temp ^ num


def fault_extractor(smgf: list[bool], pmgf: list[int], mmgf: list[tuple[int, int]], circuit_input: int, fault_map: dict,
                    fault_table: list[dict]) -> None:
    """
    Modifies fault_table so that fault_table[i] = {"smgf": [fault #s], "pmgf": [fault #s]}

    :param smgf: A list of length = No of gates in circuit.
        If smgf[G]  = True, current input catches a smgf in that Gth gate.
    :type smgf: list[boolean] # I could optimize this by turning smgf into a binary number instead
    :param pmgf: A list of length = No of gates in the circuit.
        Each element in pmgf is a binary number, for which the set bit location = pmgf fault being caught
    :type pmgf: list[int]
    :param circuit_input: an integer whose binary representation is the starting input to the circuit.
    :type circuit_input: int
    :param fault_map: mapping of faults to integers(starting from 1)
    :type fault_map: dict
    :param fault_table: Parameter is to be generated by this function.
        It is a list of length 2^No of control lines.
        fault_table[x] = {"smgf": list of smgf faults caught by current input,
            "pmgf": list of pmgf faults caught by current input}
    :type fault_table: list[dict]
    :return: None
    :rtype: None
    """

    for index, fault in enumerate(smgf):
        if fault:
            fault_table[circuit_input]["smgf"].append(fault_map.get(index, 0))
    for index, fault in enumerate(pmgf):
        if fault == 0b0:
            continue
        fault_table[circuit_input]["pmgf"].append(fault_map.get((index, fault), 0))

    for index, fault in enumerate(mmgf):
        if fault != (0, 0):
            temp_fault = (f'G{fault[0] + 1}', f'G{fault[1] + 1}')
            fault_table[circuit_input]["mmgf"].append(fault_map.get(temp_fault, 0))


def plot_graph(data: list[dict], no_of_lines: int, no_of_gates: int, no_of_total_faults: int) -> None:
    """
    plots the fault vs input graph
    :param data: a fault table. Each input maps to smgf and pmgf faults they detect.
    :type data: list[dict]
    :param no_of_lines: number of lines in the circuit.
    :type no_of_lines: int
    :param no_of_gates: number of gates in the circuit.
    :type no_of_gates: int
    :return: None
    :rtype: None
    """
    fig, ax = plt.subplots(ncols=1)
    smgf_x, smgf_y = [], []
    pmgf_x, pmgf_y = [], []
    mmgf_x, mmgf_y = [], []

    for i, sublist in enumerate(data):
        smgf_x.extend([i] * len(sublist["smgf"]))
        smgf_y.extend(sublist["smgf"])

        pmgf_x.extend([i] * len(sublist["pmgf"]))
        pmgf_y.extend(sublist["pmgf"])

        mmgf_x.extend([i] * len(sublist["mmgf"]))
        mmgf_y.extend(sublist["mmgf"])

    plt.xlabel("input configuration (in binary)")
    plt.ylabel("Fault Number")

    no_of_mmgf = (no_of_gates * (no_of_gates - 1)) // 2

    plt.title(f'''Fault vs Input graph for circuit with
    {no_of_gates} Gates and {no_of_lines} Control Lines.
    Total input combinations: {2 ** no_of_lines}.
    Total faults: (smgf: {no_of_gates}, pmgf: {no_of_total_faults - no_of_gates - no_of_mmgf}, mmgf: {no_of_mmgf}).''')

    dot_size = 1
    # doesn't make sense if it crosses around 35 faults, it gets too cluttered
    if no_of_total_faults <= 50:
        plt.yticks(range(1, no_of_total_faults + 1))
        plt.xticks(range(0, 1 << no_of_lines))

        dot_size = 200

        # horizontal lines to separate smgf, pmgf and mmgf regions
        ax.axhline(y=no_of_gates + 0.5, color='black', linestyle='dashed')
        ax.axhline(y=no_of_total_faults - no_of_mmgf + 0.5, color='black', linestyle='dashed')
        plt.grid()
        ax.set_axisbelow(True)
        fig.set_size_inches(10, 10)

    ax.scatter(mmgf_x, mmgf_y, s=dot_size, c='#00539CFF', label="mmgf")
    ax.scatter(pmgf_x, pmgf_y, s=dot_size, c='#006B38FF', label="pmgf")
    ax.scatter(smgf_x, smgf_y, s=dot_size, c='#FF3EA5FF', label="smgf")

    # to move the legend section outside the plot
    ax.legend(bbox_to_anchor=(1.15, 1), borderaxespad=0)

    fig.tight_layout()
    fig.subplots_adjust(right=0.85)

    plt.show()
