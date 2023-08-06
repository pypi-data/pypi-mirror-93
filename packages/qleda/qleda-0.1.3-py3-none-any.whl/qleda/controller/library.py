from ..model.basic import PartLibrary, Part, Pin
from ..model.schmodel import SymbolLibrary, SchRepresentation, Gate, get_unique_part_symbol, PinMatchingStrategy


def build_schematic_instance(session, reference_part: Part, copy_symbols: bool, match_type: PinMatchingStrategy,
                             symbol_libary: SymbolLibrary) -> Part:
    """
    builds a schematic part instance. takes the reference_part copies it and connects the symbol given from the
    schematic representations, if
    @param session: db session
    @param reference_part:
    @param copy_symbols: True: schematic representation, symbols, gates are copied. False, only Part and pins are copied.
    @param match_type:
    @return: copied part, ready for schematic placement
    """
    # TODO use Part().copy function
    ret_part = Part(
        name=reference_part.name,
        footprint_name=reference_part.footprint_name,
        properties={k: v for k, v in reference_part.properties.items()},
        pins={ref_pin.designator:
            Pin(
                name=ref_pin.name,
                designator=ref_pin.designator,
                swap_group=ref_pin.swap_group
            ) for ref_pin in reference_part.pins.values()
        }
    )
    if copy_symbols:
        tmp_pin_lookup = {pin.designator: pin for pin in ret_part.pins.values()}
        if len(tmp_pin_lookup) != len(ret_part.pins):
            raise ValueError
        for sch_rep in reference_part.sch_representations:
            new_schrep = SchRepresentation(
                name=sch_rep.name,
                part=ret_part
            )
            for ref_gate in sch_rep.gates:
                new_gate = Gate(
                    name=ref_gate.name,
                    pins=[tmp_pin_lookup[pin.designator] for pin in ref_gate.pins],
                    sch_representation=new_schrep,
                    part_symbols=[
                        get_unique_part_symbol(session, symbol.name, symbol_libary.name).copy()
                        for symbol in ref_gate.part_symbols]
                )
                new_gate.connect_part_symbol_pins_with_part(match_type, True)
    return ret_part


def connect_part_library_with_symbol_library(part_library: PartLibrary, symbol_libary: SymbolLibrary):
    """
    Connects the given part_library with the symbol_library
    @param part_library:
    @param symbol_libary:
    @return:
    """
    raise NotImplementedError