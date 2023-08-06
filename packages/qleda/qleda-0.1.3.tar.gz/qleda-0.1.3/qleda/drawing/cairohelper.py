from typing import NamedTuple
from .textcolordefs import DEFAULT_FONT_KEY, DEFAULT_FONT, TextFormat
import cairo

PT_TO_MM = 0.352778

# xbearing: x distance from upper left point of text boundingbox
# ybearing: y distance from upper left point of text boundingbox
# width:    width of the bounding box
# height:   height of the bounding box
# xadvance: suggested next x value of the next reference point (additonal text).
# yadvance: suggested next y value of the next reference point (additonal text).
TextExtentsCairo = NamedTuple('TextExtentsCairo', (('xbearing', float), ('ybearing', float),
                                                   ('width', float), ('height', float), ('xadvance', float),
                                                   ('yadvance', float)))
# fascent: y offset for line above text, without touching any text. used for top alignment
# fdescent: y offset for line below text, without touching any text
# fheight: font height
# fxadvance: suggested next reference point x distance
# fyadvance: suggested next reference point y distance
# src http://www.tortall.net/mu/wiki/CairoTutorial#line-width
FontExtentsCairo = NamedTuple('FontExtentsCairo', (('fascent', float), ('fdescent', float), ('fheight', float),
                              ('fxadvance', float), ('fyadvance', float)))


def italic_to_cairo_slant(italic: bool):
    return cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL


def bold_to_cairo_weight(bold: bool):
    return cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL

def setup_cairo_font(context, textformat: TextFormat):
    font = DEFAULT_FONT if textformat.font == DEFAULT_FONT_KEY else textformat.font
    context.select_font_face(font, italic_to_cairo_slant(textformat.italic),
                             bold_to_cairo_weight(textformat.bold))
    context.set_font_size(textformat.fontsize)


def font_extents(textformat: TextFormat) -> FontExtentsCairo:
    """
        src: http://blog.mathieu-leplatre.info/text-extents-with-python-cairo.html
    :param fontsize:
    :return: TextExtentsCairo
    """
    surface = cairo.SVGSurface(None, 1280, 200)
    cr = cairo.Context(surface)
    setup_cairo_font(cr, textformat)
    return FontExtentsCairo(*tuple([PT_TO_MM*x/1000 for x in cr.font_extents()]))


def text_extents(text: str, textformat: TextFormat) -> TextExtentsCairo:
    """
        src: http://blog.mathieu-leplatre.info/text-extents-with-python-cairo.html
    :param fontsize:
    :return: TextExtentsCairo
    """
    surface = cairo.SVGSurface(None, 1280, 200)
    cr = cairo.Context(surface)
    setup_cairo_font(cr, textformat)
    return TextExtentsCairo(*tuple([PT_TO_MM*x/1000 for x in cr.text_extents(text)]))

def get_default_font_extents(font) -> FontExtentsCairo:
    defaults_value = {
        'Noto Sans': FontExtentsCairo(fascent=1.069, fdescent=0.293, fheight=1.362, fxadvance=2.84, fyadvance=0.0)
    }
    if font not in defaults_value:
        return FontExtentsCairo(fascent=0.92822265625, fdescent=0.23583984375, fheight=1.1640625,
                                fxadvance=1.8740234375, fyadvance=0.0)
    else:
        return defaults_value[font]
