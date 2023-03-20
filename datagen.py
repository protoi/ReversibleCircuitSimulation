import random
import json
from binary_implementation import DataSet

data = []
for gate_no in range(1, 101):
    circuit = dict()
    circuit["name"] = f'Circuit #{gate_no}'
    no_of_lines = random.randint(2, 6)
    no_of_gates = random.randint(3, 8)

    dataset = DataSet(no_of_lines, no_of_gates)
    circuit["circuit_layout"] = dataset.generate_test_sets()
    circuit["circuit_specs"] = {"lines": no_of_lines, "gates": no_of_gates}

    data.append(circuit)

with open(f"./RESULTS/generated_data.json", "w") as write:
    json.dump(data, write, indent=2)
