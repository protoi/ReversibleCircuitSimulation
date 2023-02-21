import json
import binary_implementation as binimp
import utilities as utils


def read_file() -> list[dict]:
    """
    reads the data.json file for circuit information
    :return: an array of circuit information
    :rtype: list[dict]
    """
    file_location = "./RESULTS/data.json"
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
    return {"target": string_to_binary(t_and_c["target"]),
            "controls": string_to_binary(t_and_c["controls"])}


def simulate_circuit(circuit_data: dict) -> None:
    """
    building and running a certain circuit and saving the visualization of the circuit, and it's fault mappings
    :param circuit_data: dicts containing control and target information, no of lines, gates and circuit name
    :type circuit_data: dict
    :return: None
    :rtype: None
    """
    circuit_name = circuit_data["name"]
    no_of_lines = circuit_data["circuit_specs"]["lines"]
    no_of_gates = circuit_data["circuit_specs"]["gates"]

    circuit_layout = circuit_data["circuit_layout"]

    # we will be passing in the string representation of the binary numbers instead, easier to work with
    utils.save_circuit(circuit_layout, no_of_lines, no_of_gates, circuit_name)

    # turning "0b111" into 0b111, it was stored as a string in JSON format
    circuit_layout_corrected = list(map(fix_target_and_controls, circuit_layout))

    # saving a visual representation of the circuit

    # creating the circuit
    circuit = binimp.Circuit(no_of_gates)

    # initializing the circuit with its targets and controls
    circuit.circuit_maker(circuit_layout_corrected)

    # mapping every possible fault with a unique number starting from 1
    fault_map, no_of_total_faults = utils.map_fault_with_index(circuit_layout_corrected)

    # filling the fault table, which input config produces which smgf, pmgf and mmgf fault
    fault_table = [{"smgf": [], "pmgf": [], "mmgf": []} for _ in range(1 << no_of_lines)]

    for circuit_input in range(1 << no_of_lines):
        # setting a circuits input
        circuit.set_starting_data(circuit_input)
        # firing up the circuit
        circuit.circuit_user()
        # extracts faults encountered
        utils.fault_extractor(circuit.smgf, circuit.pmgf, circuit.mmgf, circuit_input, fault_map, fault_table)

    # saving the fault mappings
    utils.save_graph(fault_table, no_of_lines, no_of_gates, no_of_total_faults - 1, circuit_name)


def runner() -> None:
    """
    builder of the specified circuits
    :return: None
    :rtype: None
    """
    circuit_data = read_file()
    list(map(simulate_circuit, circuit_data))
