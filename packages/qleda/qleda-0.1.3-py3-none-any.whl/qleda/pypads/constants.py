"""
    Constants used when working with PADS files
"""

DEF_PIECE_ENTRY_TYPES = [
    'OPEN',
    'CLOSED',
    'CIRCLE',
    'COPOPN', #Copper open
    'COPCLS', #copper closed
    'COPCIR', #Filled copper circle
    'BRDCUT',
    'BRDCCO',
    'KPTCLS',
    'KPTCIR',
    'COPCUT',
    'COPCCO',
    'TAG',

    #pcb decal not documented
    'BASPNT', # Dimension base-point
    'CIRCUT', # copper cutout (circle) #FIxme not correct implemented
    'ARWLN1', # Arrow-line 1
    'ARWLN2', # Arrow-line 2
    'ARWHD1',
    'ARWHD2',
    'EXTLN1',
    'EXTLN2'
]

PADS_FILE_ENCODING = 'windows-1252'
DRAFTING_LIB = '*PADS-LIBRARY-LINE-ITEMS-V9*'
SCHEMATIC_LIB  = '*PADS-LIBRARY-SCH-DECALS-V9*'
PCB_DECAL_LIB = '*PADS-LIBRARY-PCB-DECALS-V9*'
PART_LIB = '*PADS-LIBRARY-PART-TYPES-V9*'

SCHEMATIC_DECAL_LEGAL_TYPES = ['OPEN', 'CLOSED', 'CIRCLE', 'COPCLS']
PADS_DESIGNATOR_KEY = 'REF-DES'
PADS_NAME_KEY = 'PART-TYPE'

EMPTY_PIN_SYMBOL = 'PINEMPTY'

VALID_PADS_PINDECAL = ['PIN', 'PINB', 'PCLK', 'PCLKB', 'PINIEB', 'PINORB', 'PINSHORT', 'PINVRTS', EMPTY_PIN_SYMBOL]