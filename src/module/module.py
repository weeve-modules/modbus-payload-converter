"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
import time
import math
from .constants import BYTE_LEN, WORD_LEN, DOUBLE_WORD_LEN
from .params import PARAMS
import re


log = getLogger("module")

#  Set module settings
__TYPE__ = PARAMS['TYPE']
__OFFSET__ = PARAMS['OFFSET']
__FORMAT__ = PARAMS['FORMAT']
__SWAP__ = PARAMS['SWAP']
__INPUT_LABEL__ = PARAMS['INPUT_LABEL']
__OUTPUT_LABEL__ = PARAMS['OUTPUT_LABEL']

SWAP_OPTIONS = {
    "no-swap": "abcd",
    "byte-swap": "badc",
    "word-swap": "cdab",
    "byte-word-swap": "dcba"
}


def change_type(data) -> str:
    """
    Data is split to selected type (bit, byte, word, double word).
    """

    if type(data) == int:
        binary = f'{data:b}'

    elif type(data) == str:
        binary = f'{int(data,16):0{len(data)*4}b}'

    bytes = hex(int(binary, 2))[2:]

    if __TYPE__ == 'bit':
        return binary

    elif __TYPE__ == 'byte':
        fill = math.ceil(len(bytes) / BYTE_LEN) * BYTE_LEN
        return bytes.zfill(fill)

    elif __TYPE__ == 'word':
        fill = math.ceil(len(bytes) / WORD_LEN) * WORD_LEN
        return bytes.zfill(fill)

    elif __TYPE__ == 'double-word':
        fill = math.ceil(len(bytes) / DOUBLE_WORD_LEN) * DOUBLE_WORD_LEN
        return bytes.zfill(fill)


def check_offset(len_data, offset):
    """
    Check if the offset is in range.
    """

    if (offset > len_data - 1):
        raise Exception(f'Offset of {offset} is out of range')


def apply_offset(data) -> str:
    """
    Returns offset bit or byte or word or double word.
    """

    offset = __OFFSET__

    if __TYPE__ == 'bit':
        check_offset(len(data), offset)
        return data[offset:offset + 1]

    elif __TYPE__ == 'byte':
        check_offset(len(data) / BYTE_LEN, offset)
        return data[offset * BYTE_LEN:offset * BYTE_LEN + BYTE_LEN]

    elif __TYPE__ == 'word':
        check_offset(len(data) / WORD_LEN, offset)
        return data[offset * WORD_LEN:offset * WORD_LEN + WORD_LEN]

    elif __TYPE__ == 'double-word':
        check_offset(len(data) / DOUBLE_WORD_LEN, offset)
        return data[offset * DOUBLE_WORD_LEN:offset * DOUBLE_WORD_LEN + DOUBLE_WORD_LEN]


def swap_data(data: "list[str]", swap_size) -> "list[str]":
    """
    Swaps the data in the list according to the "swap_size".
    """

    for i in range(0, len(data), swap_size * 2):
        t = data[i:i + swap_size]
        data[i:i + swap_size] = data[i + swap_size:i + swap_size + swap_size]
        data[i + swap_size:i + swap_size + swap_size] = t
    return data


def apply_swap(data: str) -> str:
    """
    Returns rearranged data according to "Swap".
    """

    temp_list = list(data)
    if __SWAP__ == SWAP_OPTIONS['no-swap']:
        pass

    if __SWAP__ == SWAP_OPTIONS['byte-swap']:
        temp_list = swap_data(temp_list, swap_size=2)

    elif __SWAP__ == SWAP_OPTIONS['word-swap']:
        temp_list = swap_data(temp_list, swap_size=4)

    elif __SWAP__ == SWAP_OPTIONS['byte-word-swap']:
        temp_list = swap_data(temp_list, swap_size=2)
        temp_list = swap_data(temp_list, swap_size=4)

    return ''.join(temp_list)


def hex_to_float_ieee754(data: str) -> float:
    """
    Returns hex data in float ieee754 single precision format.
    """

    bits = f'{int(data,16):032b}'

    sign = int(bits[0])        # sign,     1 bit
    exponent = int(bits[1:9], 2)    # exponent, 8 bits
    mantissa = int(bits[9:], 2)  # mantissa, len(bits)-9 bits

    return (-1)**sign * 2**(exponent - 127) * (1 + mantissa / (2**23))


def format_data(data: str):
    """
    Returns converted data according to "Format".
    """

    if __TYPE__ == 'bit':
        data = hex(int(data, 2))[2:]

    if __FORMAT__ == 'hex-string':
        return data

    elif __FORMAT__ == 'integer':
        return int(data, 16)

    elif __FORMAT__ == 'float-ieee754':
        return hex_to_float_ieee754(data)

    elif __FORMAT__ == 'string':
        data = data.zfill(BYTE_LEN)
        text = bytearray.fromhex(data).decode('unicode_escape')
        return re.sub(r'[^\t\n\r\x20-\x7F\xA1-\xFF]', u'', text)  # remove non-printable characters


def process_data(data):
    """
    Process data step by step. The data is split to selected "Type". After, the offsetted bit or byte
    or word etc is selected for conversion depending on the "Offset". Taking into account
    the "Swap", the bytes are rearranged and the payload converted according to "Format".
    """

    data = data[__INPUT_LABEL__]
    processed_data = {}

    # split by type
    data = change_type(data)

    # apply offset
    data = apply_offset(data)

    # # swap
    data = apply_swap(data)

    # # format
    data = format_data(data)

    processed_data[__OUTPUT_LABEL__] = data
    processed_data['timestamp'] = round(time.time())
    # processed_data['timestamp'] = 123

    return processed_data


def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        any: Processed data that are ready to be sent to the next module or None if error occurs.
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    try:
        # YOUR CODE HERE
        output_data = []
        if type(received_data) == dict:
            output_data.append(process_data(received_data))

        if type(received_data) == list:
            for item in received_data:
                output_data.append(process_data(item))

        return output_data, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"
