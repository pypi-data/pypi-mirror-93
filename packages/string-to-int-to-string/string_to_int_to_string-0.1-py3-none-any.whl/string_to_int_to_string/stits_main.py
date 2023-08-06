from string_to_int_to_string import stits_utils

def string_to_int(string_to_convert):
    """
    Orchestrator function to convert a string to a base 10 integer, deterministically, using the 
    unicode values of the characters in the string. Obtains the unicode value for each character
    in the input string, converts the unicode value to an 8-bit binary represented as a list
    of 0's and 1's, concatenates the binaries represented as lists for each character in order,
    and converts the concatenated binary to an int of base 10.

    Args:
        string_to_convert: any string

    Returns:
        An integer representation of the input string
    """
    bit_list = stits_utils.string_to_bit_list(string_to_convert)
    int_form_bit_list = stits_utils.bit_list_to_int(bit_list)
    return int_form_bit_list


def int_to_string(integer_to_convert):
    """
    Orchestrator function to convert an integer of base 10 to a string, deterministically. Uses the
    reverse process as string_to_int(): it converts the input integer to binary, pads the binary
    number so that the binary is of minimum size such that size mod 8 = 0, converts each 8 bit 
    section of the padded binary to a base 10 int, converts that base 10 ito to its corresponding 
    unicode character, and finally concatenates the unicode characters together (maintaining left
    to right order).

    Args:
        integer_to_convert: any int

    Returns:
        A string representation of the input integer
    """
    # Convert integer_to_convert (of base 10) to binary, represented as a string
    binary = bin(integer_to_convert)[2:]
    bit_seq = stits_utils.binstring_to_bit_list(binary)
    bit_seq_size = len(bit_seq)
    # Desired size is the minimum size, such that size mod 8 = 0
    desired_bit_seq_size = bit_seq_size + (8-bit_seq_size % 8)
    padded_bit_seq = stits_utils.pad_bits(bit_seq, desired_bit_seq_size)
    converted_string = stits_utils.bit_list_to_string(padded_bit_seq)
    return converted_string
