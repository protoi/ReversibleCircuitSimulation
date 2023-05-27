import json
from operator import itemgetter
from typing import Dict, Set

from circuit_solver import read_file, string_to_binary, fix_target_and_controls
import binary_implementation as binimp
import utilities as utils


def set_diff(most_faults: tuple[int, set[int], int], current_element: tuple[int, set[int], int]) -> tuple[int, set[
    int], int] | None:
    """
    Performs a set difference on two (int, set, int) tuples
    :param most_faults:
    :type most_faults:
    :param current_element:
    :type current_element:
    :return: HeapElement with updated faults parameter, if no faults it returns a None
    :rtype: HeapElement | None
    """
    f = current_element[1].difference(most_faults[1])
    return (current_element[0], f, len(f)) if bool(f) else None


def greedily_pick_best_fit(fault_data: dict[int, set[int]]) -> list[int]:
    """
    Greedily picks circuit inputs so that at the end, the inputs cover every single fault possible for a given circuit
    :param fault_data: (input <-> fault) mapping for a circuit
    :type fault_data: dict[int, set[int]
    :return: an array of input values for the circuit for which all faults will be covered
    :rtype: list[int]
    """

    input_fault_mappings: list[tuple[int, set[int], int]] = [(k, v, len(v)) for k, v in
                                                             fault_data.items()]  # (input_vector, fault_set, len(fault_set) tuple

    selection, answer = set(), []

    while bool(input_fault_mappings):
        # picking element with the largest len(fault set).
        # Apparently item getter is more efficient than a lambda function
        # like key = lambda elem : len(elem[1])
        # print(selection)
        most_faults_identified: tuple[int, set[int], int] = max(input_fault_mappings, key=itemgetter(2))

        answer.append(most_faults_identified[0])  # pushing input vector to answer
        selection.update(most_faults_identified[1])  # updating faults that are being covered

        # performing set diff on every element in the list, dropping that element if set diff yields a None
        input_fault_mappings = [diff for x in input_fault_mappings if
                                (diff := set_diff(most_faults_identified, x)) is not None]

    # print("============")

    return answer


def greedily_pick_best_fit_experimental(fault_data: dict[int, set[int]]) -> list[int]:
    """
    Greedily picks circuit inputs so that at the end, the inputs cover every single fault possible for a given circuit
    :param fault_data: (input <-> fault) mapping for a circuit
    :type fault_data: dict[int, set[int]
    :return: an array of input values for the circuit for which all faults will be covered
    :rtype: list[int]
    """

    print(f" fault data ++++++++ ++++++++")
    for k, v in fault_data.items():
        print(k, '-> ', v)
    print("++++++++++++++++")

    input_fault_mappings: list[tuple[int, set[int], int]] = [(k, v, len(v)) for k, v in
                                                             fault_data.items()]  # (input_vector, fault_set, len(fault_set) tuple

    selection, answer = set(), []

    while bool(input_fault_mappings):
        # picking element with the largest len(fault set).
        # Apparently item getter is more efficient than a lambda function
        # like key = lambda elem : len(elem[1])
        # print(selection)
        most_faults_identified: tuple[int, set[int], int] = max(input_fault_mappings, key=itemgetter(2))

        answer.append(most_faults_identified[0])  # pushing input vector to answer
        selection.update(most_faults_identified[1])  # updating faults that are being covered

        # performing set diff on every element in the list, dropping that element if set diff yields a None
        input_fault_mappings = [diff for x in input_fault_mappings if
                                (diff := set_diff(most_faults_identified, x)) is not None]

    # print("============")

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


def map_faults_only_pmgf(fault_mappings: dict, pmgf: list[int]) -> set[int]:
    """
    returns a set with all possible faults contained in the pmgf list after referencing
    it in the fault_mapping dictionary
    :param fault_mappings: the fault mapping, fault mapped with a unique integer
    :type fault_mappings: dict
    :param pmgf: A list of length = No of gates in the circuit.
        Each element in pmgf is a binary number, for which the set bit location = pmgf fault being caught
    :type pmgf: list[int]
    :return: a set of faults being identified
    :rtype: set[int]
    """
    faults_numbers = set()

    for index, fault in enumerate(pmgf):
        if fault == 0b0:
            continue
        pmgf_tuple = (index, fault)
        faults_numbers.add(fault_mappings.get(pmgf_tuple, 0))

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
        circuit.circuit_user(s=False, m=False)

        # current_faults = map_faults(fault_mapping, circuit.smgf, circuit.pmgf, circuit.mmgf)
        current_faults = map_faults_only_pmgf(fault_mapping, circuit.pmgf)
        total_faults_encountered.update(current_faults)
        faults_encountered[input_vector] = current_faults

    while (len(total_faults_encountered) != no_of_total_faults) and (left_pointer <= right_pointer):
        feed_input(left_pointer)
        feed_input(right_pointer)

        left_pointer += 1
        right_pointer -= 1

        """
            the current value of left_pointer and right_pointer are very important because these inputs caught faults
            that have not been identified by (0 <-> left_pointer - 1) and (right_pointer+1 <-> 2^n-1)
            So we HAVE to include these in our final result, but check if they are sub sets of each other if possible 
            
        """

    return faults_encountered


def encounter_faults_experimental(circuit: binimp.Circuit, fault_mapping: dict, no_of_total_faults: int) -> dict[
    int, set[int]]:
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
    :return: a dict of all faults encountered for a given range of circuit inputs, last left input, last right input
    :rtype: tuple[dict[int, set[int]], int, int]
    """

    # print("number of faults to encounter: ", no_of_total_faults)
    no_of_lines = circuit.number_of_lines

    total_faults_encountered = set()
    faults_encountered = dict()

    # current_input = (1 << no_of_lines) - 1
    left_pointer, right_pointer = 0, (1 << no_of_lines) - 1
    last_left_pointer, last_right_pointer = 0, 0  # will be updated by the while loop
    is_left_unique, is_right_unique = False, False

    # print(" fault mappings |||||||||||||||||||||||||||")
    # for k, v in fault_mapping.items():
    #     print(v, " -> ", k)
    # print("|||||||||||||||||||||||||||")

    def use_input(left_vector, right_vector) -> set[int]:
        """
        Simulate the circuit for both left_vector and right_vector.
        Then checks if they are a subset of one another.

        IF
            left superset of right: faults_encountered[left_vector] = left_faults
            right superset of left: faults_encountered[right_vector] = right_faults
            equal                 : faults_encountered[right_vector] = right_faults
            not related           : faults_encountered[left], faults_encountered[right] = left_faults, right_faults

        :param left_vector: left pointer
        :type left_vector: int
        :param right_vector: right pointer
        :type right_vector: int
        :return: None
        :rtype: None
        """
        circuit.set_starting_data(left_vector)
        circuit.circuit_user()

        # left_faults = map_faults(fault_mapping, circuit.smgf, circuit.pmgf, circuit.mmgf)
        left_faults = map_faults_only_pmgf(fault_mapping, circuit.pmgf)

        circuit.set_starting_data(right_vector)
        circuit.circuit_user()

        # right_faults = map_faults(fault_mapping, circuit.smgf, circuit.pmgf, circuit.mmgf)
        right_faults = map_faults_only_pmgf(fault_mapping, circuit.pmgf)

        # now check if one is the others subset or not

        # left is a subset of right
        if len(left_faults) > len(right_faults) and right_faults.issubset(left_faults):
            total_faults_encountered.update(left_faults)
            faults_encountered[left_vector] = left_faults

        # right is a subset of left
        elif len(left_faults) < len(right_faults) and left_faults.issubset(right_faults):
            total_faults_encountered.update(right_faults)
            faults_encountered[right_vector] = right_faults

        # same no of faults caught and faults caught by left and right are exactly the same
        elif len(left_faults) == len(right_faults) and left_faults.issubset(right_faults):
            # we don't need both, just use right_input
            total_faults_encountered.update(right_faults)
            faults_encountered[right_vector] = right_faults

        # they weren't subsets, so include both
        else:
            total_faults_encountered.update(right_faults.union(left_faults))
            faults_encountered[left_vector] = left_faults
            faults_encountered[right_vector] = right_faults

        return total_faults_encountered

    while (len(total_faults_encountered) != no_of_total_faults) and (left_pointer <= right_pointer):
        total_faults_encountered = use_input(left_pointer, right_pointer)
        left_pointer += 1
        right_pointer -= 1

    """
        the current value of left_pointer and right_pointer are very important because these inputs caught faults
        that have not been identified by (0 <-> left_pointer - 1) and (right_pointer+1 <-> 2^n-1)
        So we HAVE to include these in our final result, but check if they are sub sets of each other if possible 

    """

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

    fault_map, no_of_total_faults, count_smgf, count_pmgf, count_mmgf = utils.map_fault_with_index(
        circuit_layout_bin_string_to_integer)

    # we don't build a fault table because it will take 2^n time

    # map_faults_with_index starts counting from 1, so we subtract a 1 to make up for it

    print(f"smgf, pmgf, mmgf: {count_smgf}, {count_pmgf}, {count_mmgf}")
    # fault_data, left_bound, right_bound = encounter_faults_experimental(circuit, fault_map, count_smgf + count_pmgf + count_mmgf)
    fault_data = encounter_faults_experimental(circuit, fault_map, count_pmgf)

    fault_data_set_covered = greedily_pick_best_fit_experimental(fault_data)

    # fault_data_set_covered = greedily_pick_best_fit(fault_data)

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


def runmax() -> None:
    data = '''
    [    
          {
    "name": "MOD 10r",
    "circuit_layout": [
      {
        "target": "0b0010",
        "controls": "0b1000"
      },
      {
        "target": "0b0001",
        "controls": "0b1110"
      },
      {
        "target": "0b0100",
        "controls": "0b1011"
      },
      {
        "target": "0b1000",
        "controls": "0b0111"
      },
      {
        "target": "0b0010",
        "controls": "0b1000"
      },
      {
        "target": "0b0010",
        "controls": "0b1001"
      },
      {
        "target": "0b0100",
        "controls": "0b0011"
      },
      {
        "target": "0b0010",
        "controls": "0b0001"
      },
      {
        "target": "0b0001",
        "controls": "0b1010"
      },
      {
        "target": "0b0001",
        "controls": "0b0000"
      }
    ],
    "circuit_specs": {
      "lines": 4,
      "gates": 10
    },
    "link": "http://www.informatik.uni-bremen.de/rev_lib/doc/real/mod10_171.jpg"
  },
  {
    "name": "mod10",
    "link": "http://www.informatik.uni-bremen.de/rev_lib/doc/real/mod10_171.jpg",
    "circuit_specs": {
      "lines": 4,
      "gates": 10
    },
    "circuit_layout": [
      {
        "target": "0b0010",
        "controls": "0b1000"
      },
      {
        "target": "0b0001",
        "controls": "0b1110"
      },
      {
        "target": "0b0100",
        "controls": "0b1011"
      },
      {
        "target": "0b1000",
        "controls": "0b0111"
      },
      {
        "target": "0b0010",
        "controls": "0b1000"
      },
      {
        "target": "0b0010",
        "controls": "0b1001"
      },
      {
        "target": "0b0100",
        "controls": "0b0011"
      },
      {
        "target": "0b0010",
        "controls": "0b0001"
      },
      {
        "target": "0b0001",
        "controls": "0b1010"
      },
      {
        "target": "0b0001",
        "controls": "0b0000"
      }
    ]
  }
    ]
    '''
    circuit_data = json.loads(data)
    minimal_sets = [simulate_circuit(x) for x in circuit_data]

    print(json.dumps(minimal_sets, indent=4))


# experimental_bi_runner()
runmax()
