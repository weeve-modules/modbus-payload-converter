
"""
All constants specific to the application
"""
from os import getenv

PARAMS = {
    "INPUT_LABEL": getenv("INPUT_LABEL", "data"),
    "TYPE": getenv("TYPE", "byte"),
    "OFFSET": int(getenv("OFFSET", 0)),
    "FORMAT": getenv("FORMAT", "hex"),
    "SWAP": getenv("SWAP", "abcd"),
    "OUTPUT_LABEL": getenv("OUTPUT_LABEL", "output-data"),
}
