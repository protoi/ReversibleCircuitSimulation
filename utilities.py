import pickle
import numpy


def serialize_data(data):
    outputs = numpy.array(data)
    with open('outputs/outputs.num', 'wb') as output_file:
        pickle.dump(outputs, output_file)

    with open('outputs/outputs.num', 'rb') as output_file:
        ans = pickle.load(output_file)
        print(ans)
