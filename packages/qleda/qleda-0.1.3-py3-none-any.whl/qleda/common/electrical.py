from enum import Enum, auto


class Polarity(Enum):
    """
        Electrical polarity of a Net of a Pin.
    """
    P = 0
    N = 1


class SimulationType(Enum):
    """
        see PySpice Spice Netlist
    """
    SPICE = auto() # Spice defined
    R = auto()  # Semiconductor resistor model
    L = auto()  # Inductor model
    C = auto()  # Semiconductor capacitor model
    D = auto()  # Diode model


class PinType(Enum):
    """
        PinType for IC pins.
    """
    In = auto()         # example an enable pin
    Out = auto()        # example a clock output
    IO = auto()         # example a uc pin
    Passive = auto()    # a resistor pin
    Power_in = auto()   # a vcc pin of a IC
    Power_out = auto()  # an LDO output or a SW pin of a switcher
    Gnd = auto()        # a GND pin of a IC


