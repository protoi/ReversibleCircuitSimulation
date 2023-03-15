import json

with open("../RESULTS/JSONS/Circuit #10_sparse_JSON.json") as data:
    table = json.load(data)

# list(
#     map(lambda circuit_input: [
#         *circuit_input["smgf"],
#         *circuit_input["pmgf"],
#         *circuit_input["mmgf"]
#     ], table))

restructured_table = [
    {"circuit_input": index, "faults": {*circuit_input["smgf"], *circuit_input["pmgf"], *circuit_input["mmgf"]}} for
    index, circuit_input in enumerate(table)]

print([x["faults"] for x in restructured_table])

# only done to store inputs for the c++ code
with open("./restructured_table.json", "w") as table_file:
    print([x["faults"] for x in restructured_table], file=table_file)

reverse_sorted_by_elements = sorted(restructured_table, reverse=True, key=lambda elem: len(elem["faults"]))

# print(reverse_sorted_by_elements)

print([x["circuit_input"] for x in reverse_sorted_by_elements])
# needed = set(x for x in range(1, 36))

selection = set()
answers = []

while len(reverse_sorted_by_elements) != 0:
    # pick the first element
    best_for_now = reverse_sorted_by_elements[0]["faults"]
    # adding the picked input to the set of answer
    answers.append(reverse_sorted_by_elements[0]["circuit_input"])

    # push everything inside of best_for_now into the selection
    selection.update(best_for_now)
    # print(f'still required:\n{needed.difference(selection)}')

    # setting the first element to None because everything in it has been selected anyway
    for index, element in enumerate(reverse_sorted_by_elements):
        # removing picked elements
        reverse_sorted_by_elements[index]["faults"] = element["faults"].difference(best_for_now)
        if len(reverse_sorted_by_elements[index]["faults"]) == 0:
            reverse_sorted_by_elements[index] = None

    # removing None elements from the list
    reverse_sorted_by_elements = list(filter(lambda x: x is not None, reverse_sorted_by_elements))
    reverse_sorted_by_elements = sorted(reverse_sorted_by_elements, reverse=True, key=lambda elem: len(elem["faults"]))

print(answers)
print(len(selection))
