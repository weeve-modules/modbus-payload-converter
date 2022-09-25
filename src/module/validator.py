"""
Validates whether the incoming data has an acceptable type and structure.

Edit this file to verify data expected by you module.
"""

from logging import getLogger

from .params import PARAMS

log = getLogger("validator")

__INPUT_LABEL__ = PARAMS['INPUT_LABEL']


def is_empty_payload(data):
    return len(data) == 0


def is_hex_string(data):
    try:
        int(data, 16)
        return True
    except Exception:
        return False


def is_integer(data):
    return (type(data) == int)


def data_validation(data: any) -> str:
    """
    Validate incoming data i.e. by checking if it is of type dict or list.
    Function description should not be modified.

    Args:
        data (any): Data to validate.

    Returns:
        str: Error message if error is encountered. Otherwise returns None.

    """

    log.debug("Validating ...")

    try:
        # YOUR CODE HERE

        allowed_data_types = [dict, list]

        if not type(data) in allowed_data_types:
            return f"Detected type: {type(data)} | Supported types: {allowed_data_types} | invalid!"

        if (is_empty_payload(data)):
            return "Data payload is empty."

        # check if data contains required label
        if type(data) == dict and not __INPUT_LABEL__ in data:
            return "Data does not contain required input label."

        elif type(data) == list:
            for item in data:
                if not __INPUT_LABEL__ in item:
                    return "Some data does not contain required input label."

        # check format of data
        if type(data) == dict:
            if not (is_hex_string(data[__INPUT_LABEL__])) and \
                    not is_integer(data[__INPUT_LABEL__]):
                return "Data is not hex string or integer."

        elif type(data) == list:
            for item in data:
                if not (is_hex_string(item[__INPUT_LABEL__])) and \
                        not is_integer(item[__INPUT_LABEL__]):
                    return "Some data is not hex string or integer."

        return None

    except Exception as e:
        return f"Exception when validating module input data: {e}"
