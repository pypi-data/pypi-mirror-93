"""
Number Base Converter by v01d

MIT License

Copyright (c) 2019 - 2021 v01d

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math
import string
import doctest


SYMBOLS = string.digits + string.ascii_uppercase


def convert(
    number: str,
    to_base: int,
    from_base=10,
    max_fractional_part_length=4
) -> str:
    """
    :param number: from_base number (as String) to convert
    :param to_base: New base [2; 36]
    :param from_base: Old base [2; 36]
    :param max_fractional_part_length: length of fractional_part (if it != 0)
    :returns: to_base number as a String

    >>> convert('15', 2)
    '1111'
    >>> convert('10F', to_base=8, from_base=16)
    '417'
    >>> convert('1', 30)
    '1'
    >>> convert('17', 16)
    '11'
    >>> convert('0', 2)
    '0'
    >>> convert('2904.2904', 16, max_fractional_part_length=10)
    'B58.4A57A786C2'
    >>> convert('2904.2904', 8)
    '5530.2245'
    """

    if not (2 <= to_base <= 36 and 2 <= from_base <= 36):
        raise ValueError("2 <= to_base, from_base <= 36")

    if number.startswith("-"):
        raise ValueError("Number must be non-negative")

    if "." in number:
        integer_part_repr, fractional_part_repr = number.split(".")
        parsed_number = (
            int(integer_part_repr, from_base)
            +
            sum(
                from_base ** i * int(digit, from_base)
                for i, digit in zip(
                    range(-1, -len(fractional_part_repr) - 1, -1),
                    fractional_part_repr
                )
            )
        )
    else:
        parsed_number = int(number, from_base)

    fractional_part, integer_part = math.modf(parsed_number)
    integer_part = int(integer_part)

    integer_symbols = []
    if integer_part:
        while integer_part > 0:
            integer_symbols.append(SYMBOLS[integer_part % to_base])
            integer_part //= to_base
    else:
        integer_symbols.append("0")

    result = "".join(reversed(integer_symbols))
    
    if fractional_part:
        fractional_symbols = ["."]
        for _ in range(max_fractional_part_length):
            fractional_part *= to_base
            fractional_part, integer_part = math.modf(fractional_part)
            integer_part = int(integer_part)

            fractional_symbols.append(SYMBOLS[integer_part % to_base])
        
        result += "".join(fractional_symbols)   

    return result


if __name__ == "__main__":
    doctest.testmod()
