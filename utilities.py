import matplotlib.pyplot as plt
import numpy as np

nibble_lookup = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]


def count_set_bits(num: int) -> int:
    count = 0
    if num == 0:
        return nibble_lookup[0]
    while num != 0:
        nibble = num & 0b1111
        count += nibble_lookup[nibble]
        num = num >> 4
    return count


def produce_multiples_of_2(n: int, length: int) -> list[int]:
    count = 0
    answer = []
    while count != length:
        if n & 0b1 == 1:
            answer.append(2 ** count)
        n = n >> 1
        count += 1
    return answer


def map_pmgf_with_fault(cascade_of_gates: list[dict], no_of_input_lines) -> dict:
    # count = len(cascade_of_gates) + 1  # we want to start numbering pmgfs after smgfs
    tempdict = {}
    count = 1
    for index in range(len(cascade_of_gates)):  # accommodating for smgf
        tempdict[index] = count
        count += 1
    for index, gate in enumerate(cascade_of_gates):  # accommodating for pmgf
        subparts = produce_multiples_of_2(gate['controls'], no_of_input_lines)
        for s in subparts:
            tempdict[(index, s)] = count
            count += 1
    # print(tempdict)

    return tempdict


def counter_controls(cascade_of_gates: list[dict]) -> int:
    counter = 0
    for gate in cascade_of_gates:
        counter += count_set_bits(gate['controls'])
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
    temp = 2 ** (no_of_bits + 1) - 1
    return temp ^ num


def fault_extractor(smgf, pmgf, circuit_input, fault_map, fault_table):
    for index, fault in enumerate(smgf):
        if fault:
            fault_table[circuit_input].append(fault_map.get(index, 0))
    for index, fault in enumerate(pmgf):
        if fault == 0b0:
            continue
        fault_table[circuit_input].append(fault_map.get((index, fault), 0))


def plot_graph(data):
    fig, ax = plt.subplots()
    x, y = [], []
    for i, sublst in enumerate(data):
        x.extend([i] * len(sublst))
        y.extend(sublst)
    plt.scatter(x, y, s=1)
    plt.show()

    pass
