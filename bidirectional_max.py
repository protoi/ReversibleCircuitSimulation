import json
from typing import Dict, Set

from circuit_solver import read_file, string_to_binary, fix_target_and_controls
import binary_implementation as binimp
import utilities as utils


def set_diff(most_faults: tuple[int, set[int]], current_element: tuple[int, set[int]]) -> tuple[int, set[int]] | None:
    """
    Performs a set difference on two (int, set) tuples
    :param most_faults:
    :type most_faults:
    :param current_element:
    :type current_element:
    :return: HeapElement with updated faults parameter, if no faults it returns a None
    :rtype: HeapElement | None
    """
    f = current_element[1].difference(most_faults[1])
    return (current_element[0], f) if bool(f) else None


def greedily_pick_best_fit(fault_data: dict[int, set[int]]) -> list[int]:
    """
    Greedily picks circuit inputs so that at the end, the inputs cover every single fault possible for a given circuit
    :param fault_data: (input <-> fault) mapping for a circuit
    :type fault_data: dict[int, set[int]
    :return: an array of input values for the circuit for which all faults will be covered
    :rtype: list[int]
    """

    heap_input_fault_mapping = [(k, v) for k, v in fault_data.items()]  # (input_vector, fault_set) tuple

    selection, answer = set(), []

    while bool(heap_input_fault_mapping):
        most_faults_identified: tuple[int, set[int]] = max(heap_input_fault_mapping,
                                                           key=lambda elem: len(
                                                               elem[1]))  # picking element with the largest fault set

        answer.append(most_faults_identified[0])  # pushing input vector to answer
        selection.update(most_faults_identified[1])  # updating faults that are being covered

        # performing set diff on every element in the list, dropping that element if set diff yields a None
        heap_input_fault_mapping = [diff for x in heap_input_fault_mapping if
                                    (diff := set_diff(most_faults_identified, x)) is not None]

    return answer


def map_faults(fault_mappings: dict, smgf: list[bool], pmgf: list[int], mmgf: list[tuple[int, int]]) -> set[int]:
    """
    returns a set with all possible faults contained in the smgf, pmgf and mmgf list after referencing
    it in the fault_mapping dictionary
    :param fault_mappings: the fault mapping, fault mapped with a unique integer
    :type fault_mappings: dict
    :param smgf: A list of length = No of gates in circuit.
        If smgf[G]  = True, current input catches a smgf in that Gth gate.
    :type smgf: list[boolean] # I could optimize this by turning smgf into a binary number instead
    :param pmgf: A list of length = No of gates in the circuit.
        Each element in pmgf is a binary number, for which the set bit location = pmgf fault being caught
    :type pmgf: list[int]
    :param mmgf: a list of integer tuples representing the starting and ending gates from which gates have gone missing.
    :type mmgf: list[tuple[int, int]]
    :return: a set of faults being identified
    :rtype: set[int]
    """
    faults_numbers = set()

    for index, fault in enumerate(smgf):
        if fault:
            faults_numbers.add(fault_mappings.get(index, 0))
    for index, fault in enumerate(pmgf):
        if fault == 0b0:
            continue
        pmgf_tuple = (index, fault)
        faults_numbers.add(fault_mappings.get(pmgf_tuple, 0))
    for fault in mmgf:
        if fault != (0, 0):
            mmgf_tuple = (f'G{fault[0] + 1}', f'G{fault[1] + 1}')
            faults_numbers.add(fault_mappings.get(mmgf_tuple, 0))

    return faults_numbers


def encounter_faults(circuit: binimp.Circuit, fault_mapping: dict, no_of_total_faults: int) -> dict[int, set[int]]:
    """
    starts from circuit input having the highest number of 1s
    and goes back one step at a time
    till it has encountered every single fault possible or till it reaches 0b0
    :param circuit: the reversible circuit
    :type circuit: Circuit
    :param fault_mapping: dictionary containing the faults mapped with a unique integer
    :type fault_mapping: dict
    :param no_of_total_faults: number of total faults possible for the circuit (smgf + pmgf + mmgf)
    :type no_of_total_faults: int
    :return: a dict of all faults encountered for a given range of circuit inputs
    :rtype: dict[int, set[int]]
    """
    no_of_lines = circuit.number_of_lines

    total_faults_encountered = set()
    faults_encountered = dict()

    # current_input = (1 << no_of_lines) - 1
    left_pointer, right_pointer = 0, (1 << no_of_lines) - 1

    def feed_input(input_vector):
        circuit.set_starting_data(input_vector)
        circuit.circuit_user()

        current_faults = map_faults(fault_mapping, circuit.smgf, circuit.pmgf, circuit.mmgf)
        total_faults_encountered.update(current_faults)
        faults_encountered[input_vector] = current_faults

    while (len(total_faults_encountered) != no_of_total_faults) and (left_pointer <= right_pointer):
        feed_input(left_pointer)
        feed_input(right_pointer)

        left_pointer += 1
        right_pointer -= 1

    return faults_encountered


def simulate_circuit(circuit_data: dict) -> dict:
    """
    generates a circuit using the provided circuit configuration data and activates it with
    various inputs for the minimal set.
    :param circuit_data: input configuration for a single circuit
    :type circuit_data: dict
    :return: mapping between circuit name and it's predicted minimal set
    :rtype: dict
    """
    circuit_name = circuit_data["name"]
    print("bidir just max simulating ", circuit_name)
    circuit_reference = circuit_data.get('link', "no link")

    no_of_lines, no_of_gates = circuit_data["circuit_specs"]["lines"], circuit_data["circuit_specs"]["gates"]

    circuit_layout = circuit_data["circuit_layout"]

    circuit_layout_bin_string_to_integer = list(map(fix_target_and_controls, circuit_layout))

    # initializing the circuit with starter values
    circuit = binimp.Circuit(no_of_lines)
    circuit.circuit_maker(circuit_layout_bin_string_to_integer)

    fault_map, no_of_total_faults = utils.map_fault_with_index(circuit_layout_bin_string_to_integer)

    # we don't build a fault table because it will take 2^n time

    # map_faults_with_index starts counting from 1, so we subtract a 1 to make up for it
    fault_data = encounter_faults(circuit, fault_map, no_of_total_faults - 1)

    fault_data_set_covered = greedily_pick_best_fit(fault_data)

    return {"circuit_name": circuit_name, "circuit_reference": circuit_reference,
            "minimal_set_bidirectional": fault_data_set_covered, 'set_length': len(fault_data_set_covered)}


def experimental_bi_runner() -> None:
    """
    Runs multiple circuits for the configs present inside the data.json file
    :return: Nothing
    :rtype: None
    """
    circuit_data = read_file()
    minimal_sets = list(map(simulate_circuit, circuit_data))

    # with open("./RESULTS/MINIMAL_SETS/mini_set.json", "w") as file:
    with open("./RESULTS/REVLIB/MINIMAL_SETS/mini_set_bidirectional_no_datastructure.json", "w") as file:
        json.dump(minimal_sets, file, indent=2)
