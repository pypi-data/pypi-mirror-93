from pdfdata import *

def flag_decomposer(flags: int) -> dict:
    """
    Make font flags human readable.

    :param flags: integer indicating binary encoded font attributes
    :return: dictionary of attributes names and their activation state
    """

    # defaults
    l = {"superscript": 0, "italic": 0, "serifed": 0, "monospaced": 0, "bold": 0}

    # check for activation state
    if flags & 2 ** 0:
        l["superscript"] = 1

    if flags & 2 ** 1:
        l["italic"] = 1

    if flags & 2 ** 2:
        l["serifed"] = 1

    if flags & 2 ** 3:
        l["monospaced"] = 1

    if flags & 2 ** 4:
        l["bold"] = 1

    # return
    return l