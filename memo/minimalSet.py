import json
from functools import lru_cache

with open("../RESULTS/JSONS/Circuit #10_dense_JSON.json") as data:
    table = json.load(data)

restructured_table = [
    {"circuit_input": index, "faults": {*circuit_input["smgf"], *circuit_input["pmgf"], *circuit_input["mmgf"]}} for
    index, circuit_input in enumerate(table)]

no_of_lines = len(restructured_table)
combinations = []


@lru_cache
def gen_combinations(selection, index):
    if index == no_of_lines:
        combinations.append(selection)
        return

    gen_combinations(selection, index + 1)
    gen_combinations((*selection, index), index + 1)


# arr = [1,2,3,4,5], n = 6 -> [*ar, n] = [1,2,3,4,5,6]
gen_combinations((), 0)
yields = []

for combos in combinations:
    temp_set = set()
    for c_inp in combos:
        temp_set.update(restructured_table[c_inp]["faults"])
    yields.append({"combo_length": len(combos), "combos": combos, "set_coverage": len(temp_set)})

yields.sort(key=lambda elem: (- elem["set_coverage"], elem["combo_length"]))

for y in yields[:10]:
    print(y)
