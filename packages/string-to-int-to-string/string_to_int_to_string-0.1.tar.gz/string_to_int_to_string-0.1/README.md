# string-to-int-to-string
One-to-one & deterministic functions for converting any string to an int, and any int to a string. 

## Description
```string_to_int(s)``` is a one-to-one function that converts any string to an int. Conversely, ```int_to_string(i)``` is a one-to-one function that converts an int to a string.
These two functions are both deterministic, meaning they produce identical outputs for identical inputs.
Thus, we can convert a string,```"foo"```, to an int with:
```foo_int = string_to_int("foo")``` <br/>
We can then convert this back to the original string, ```"foo"```, with:
```int_to_string(foo_int)``` <br/>
Thus, for any string, ```s```:
```s = int_to_string(string_to_int(s))```

## Installation
Install with pip: 
```pip install string_to_int_to_string```

## API Reference
* ```string_to_int(string_to_convert)```
    * Converts string to a base 10 integer, deterministically, using the unicode values of the characters in the string.
    * Arguments: ```string_to_convert```: any string (no limit to character types of size)
    * Returns: An integer representation of the input string

* ```int_to_string(int_to_convert)```
    * Converts an integer to a string, deterministically. Uses the reverse process as ```string_to_int()```.
    * Arguments: ```int_to_convert```: any int (no limit on size)
    * Returns: A string representation of the input integer

## Example
Import into python file with: <br/>
 ```import string_to_int_to_string as stits``` <br/><br/>
Convert a string, say ```bar```, to an integer with: <br/>
 ```bar_int = stits.string_to_int("bar")``` <br/><br/>
Convert this integer back to the original string: <br/>
```original_string = sits.int_to_string(bar_int)``` <br/>
