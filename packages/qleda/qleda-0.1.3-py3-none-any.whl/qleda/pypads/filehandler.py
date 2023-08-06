# helper functions to parse pads files
from typing import Dict
from pathlib import Path
from typing import NamedTuple
import re

PADS_FILE_ENCODING = 'windows-1252'





# def pads_f_to_sections(p_file: str) -> Dict[str, str]:
#     """
#
#     @param p_file:  a typical pads ascii file with several sections. E.g. schematic, netlist or pcb. It is expected
#                     to only have linux line ending
#
#                     typically start with *PRIMARY-KEYWORD*\sSECONDARY-KEYWORD
#
#     """
#     lines = p_file.replace('\r', '')
#     sections = {}
#     while lines:
#         line = lines.pop()
#
