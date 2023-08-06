import string_to_int_to_string as stits

###### Example of converting a string to an int, and back to a string ######
example_string = "orange"
example_int = stits.string_to_int(example_string)
back_to_string = stits.int_to_string(example_int)
print("{} {} {}".format(example_string, example_int, back_to_string))
