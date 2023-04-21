import json

with open('./raw_data.json', 'r') as f:
    data = json.load(f)


def map_variables_with_index(variables: str) -> dict[str, int]:
    mapping = dict()
    for index, var in enumerate(variables.split(' ')):
        mapping[var] = index
    return mapping


def parse_gates(array_of_gates: list[str], no_of_lines: int, var_index_mapping: dict[str, int]) -> list[dict[
    str, str]] | None:
    no_of_gates = len(array_of_gates)

    gate_config = [{"target": "", "controls": ""} for _ in range(no_of_gates)]

    for index, gate in enumerate(array_of_gates):
        target_and_controls = gate.split(' ')
        target_array, controls_array = ["0"] * no_of_lines, ["0"] * no_of_lines
        tar = var_index_mapping.get(target_and_controls[-1], -1)
        cont = [var_index_mapping.get(x, -1) for x in target_and_controls[1:-1]]
        if tar == -1:
            return None
        target_array[tar] = "1"

        gate_config[index]['target'] = f"0b{''.join(target_array)}"

        for c in cont:
            if c == -1:
                return None
            controls_array[c] = "1"
        gate_config[index]['controls'] = f"0b{''.join(controls_array)}"

    return gate_config


def write_data(circuits):
    with open("./parsed_data.json", 'w') as parsed_data_file:
        json.dump(circuits, parsed_data_file, indent=2)


ans = []
for d in data:
    circ_name, circ_url, circ_lines, circ_vars, circ_gates = d['name'], d['url'], d['lines'], d['variables'], d['gates']

    var_mapping = map_variables_with_index(circ_vars)

    print(var_mapping)

    temp = {"name": circ_name, "link": circ_url, "circuit_specs": {"lines": circ_lines, "gates": len(circ_gates)},
            "circuit_layout": parse_gates(circ_gates, circ_lines, var_mapping)}

    ans.append(temp)

write_data(ans)
