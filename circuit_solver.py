import json
import binary_implementation as binimp
import utilities as utils


def read_file(file_location="./RESULTS/REVLIB/INPUTS/data revlib.json") -> list[dict]:
    """
    reads the data.json file for circuit information
    :return: an array of circuit information
    :rtype: list[dict]
    """
    with open(file_location, 'r') as f:
        data = json.load(f)
    return data


def string_to_binary(s):
    """
    converts a binary string to an integer for example "0b111" -> 0b111 -> 7
    :param s: binary string
    :type s: str
    :return: integer version of binary string
    :rtype: int
    """
    return int(s, 2)


def fix_target_and_controls(t_and_c):
    """
    converts target & control pair's binary string formatting to integers using string_to_binary function
    :param t_and_c: a single dictionary of the format {"target": "0bxyx", "controls": "0byxx"} where x is 0 and y is 1
    :type t_and_c: dict
    :return: dictionary of format {"target": 0bxyx, "controls": 0byxx}, notice how they are not strings anymore
    :rtype: dict
    """
    return {"target": string_to_binary(t_and_c["target"]), "controls": string_to_binary(t_and_c["controls"])}


def greedy_set_cover(fault_data):
    """
    Greedily picks circuit inputs so that at the end, the inputs cover every single fault possible for a given circuit
    :param fault_data: (input <-> fault) mapping for a circuit
    :type fault_data: dict[int, set[int]
    :return: an array of input values for the circuit for which all faults will be covered
    :rtype: list[int]
    """

    restructured_table = [
        {"circuit_input": index, "faults": {*circuit_input["smgf"], *circuit_input["pmgf"], *circuit_input["mmgf"]}} for
        index, circuit_input in enumerate(fault_data)]

    reverse_sorted_table = sorted(restructured_table, reverse=True, key=lambda elem: len(elem["faults"]))

    selection = set()
    answer = []

    while len(reverse_sorted_table) > 0:
        most_faults_identified = reverse_sorted_table[0]["faults"]
        answer.append(reverse_sorted_table[0]["circuit_input"])

        selection.update(most_faults_identified)

        for index, element in enumerate(reverse_sorted_table):
            reverse_sorted_table[index]["faults"] = element["faults"].difference(most_faults_identified)
            if len(reverse_sorted_table[index]["faults"]) == 0:
                reverse_sorted_table[index] = None

        reverse_sorted_table = list(filter(lambda x: x is not None, reverse_sorted_table))
        reverse_sorted_table = sorted(reverse_sorted_table, reverse=True, key=lambda elem: len(elem["faults"]))

    return answer


def simulate_circuit(circuit_data: dict) -> dict:
    """
    building and running a certain circuit and saving the visualization of the circuit, and it's fault mappings
    :param circuit_data: dicts containing control and target information, no of lines, gates and circuit name
    :type circuit_data: dict
    :return: None
    :rtype: None
    """
    circuit_name = circuit_data["name"]
    circuit_reference = circuit_data.get("link", "no link")

    no_of_lines = circuit_data["circuit_specs"]["lines"]
    no_of_gates = circuit_data["circuit_specs"]["gates"]

    circuit_layout = circuit_data["circuit_layout"]

    # we will be passing in the string representation of the binary numbers instead, easier to work with
    # saving a visual representation of the circuit

    utils.save_circuit(circuit_layout, no_of_lines, no_of_gates, circuit_name, circuit_reference)

    # turning "0b111" into 0b111, it was stored as a string in JSON format
    circuit_layout_corrected = list(map(fix_target_and_controls, circuit_layout))

    # creating the circuit
    circuit = binimp.Circuit(no_of_gates)

    # initializing the circuit with its targets and controls
    circuit.circuit_maker(circuit_layout_corrected)

    # mapping every possible fault with a unique number starting from 1
    fault_map, no_of_total_faults = utils.map_fault_with_index(circuit_layout_corrected)

    # filling the fault table, which input config produces which smgf, pmgf and mmgf fault
    fault_table = [{"smgf": [], "pmgf": [], "mmgf": []} for _ in range(1 << no_of_lines)]

    # iterating over all input combinations -> 2 ^ no_of_lines
    for circuit_input in range(1 << no_of_lines):
        # setting a circuits input
        circuit.set_starting_data(circuit_input)
        # firing up the circuit
        circuit.circuit_user()
        # extracts faults encountered
        utils.fault_extractor(circuit.smgf, circuit.pmgf, circuit.mmgf, circuit_input, fault_map, fault_table)

    # saving the fault mappings
    # --->
    utils.save_graph(fault_table, no_of_lines, no_of_gates, no_of_total_faults - 1, circuit_name, circuit_reference)

    # saving the fault mappings as a json
    # --->
    utils.save_faults_json(fault_table, circuit_name, circuit_reference)

    fault_data_set_covered = greedy_set_cover(fault_table)

    return {'circuit_name': circuit_name, 'circuit_reference': circuit_reference , 'minimal_set_inefficient': fault_data_set_covered}


def runner() -> None:
    """
    builder of the specified circuits
    :return:
    :rtype: None
    """
    circuit_data = read_file()
    minimal_sets = list(map(simulate_circuit, circuit_data))

    # with open('./RESULTS/MINIMAL_SETS/old_greedy_algo.json', 'w') as file:
    with open('./RESULTS/REVLIB/MINIMAL_SETS/old_greedy_algo.json', 'w') as file:
        json.dump(minimal_sets, file, indent=2)
