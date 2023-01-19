# this was wrong, don't use this
# it returned 1 for every location input = 1 and control = 0 instead of control = 1 and input = 0
def generate_pmgf(current_input: int, gate):
    """
    Example:
    control =   1111 1100
    input =     1010 1010
    set answer's corresponding bit to 1 for every location where control was 1 but input was 0
    which means answer = 0101 0100

    :param current_input: input to the gate, represented by an integer.
    :type current_input: int
    :param gate: Gate object which denotes the current gate of the circuit.
    :type gate: Gate
    :return: which pmgf is being identified by the gate
    :rtype:  int
    """
    temp_controls = gate.controls  # a binary number
    bits_read = 0
    answer = 0
    flag = False

    print("old implementation:")
    print(current_input, gate.controls)

    while temp_controls != 0 or current_input != 0:
        isolator = 0b1
        current_last = current_input & isolator  # extracting the last bit
        gates_last = temp_controls & isolator  # extracting the last bit
        if gates_last == 1 and current_last == 0:
            if flag:  # this is done to remove higher order pmgfs, we only want 1st order pmgfs
                print("answer", 0)
                return 0b0
            answer = answer | 2 ** bits_read  # make this 0b1 << bits_read instead 💀💀💀
            flag = True

        temp_controls = temp_controls >> 1
        current_input = current_input >> 1
        bits_read += 1
    print("answer", answer)

    return answer
