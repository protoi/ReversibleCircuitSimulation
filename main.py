# import binary_implementation as binimp
# import integer_implementation as intimp
import circuit_solver as cs
import experimental as exp
import time

if __name__ == "__main__":
    in_loc, out_loc = "./RESULTS/generated_data.json", "./RESULTS/MINIMAL_SETS/mini_set.json"
    time_start_old = time.time()
    cs.runner()
    time_end_old = time.time()

    time_start_new = time.time()
    exp.experimental_runner()
    time_end_new = time.time()

    print(f"OLD -> {time_end_old - time_start_old}")
    print(f"NEW -> {time_end_new - time_start_new}")

    pass
