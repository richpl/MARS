#! /usr/bin/python

"""
A class representing the core within which Red Code programs
can run. The core consists of an ordered list of words, each
either empty or containing a single Red Code instruction. The
core wraps so that writing a sequence of words that overruns
the end of the core will result in the write wrapping around
to the beginning of the core.
"""

class Core:

    """
    Default CORESIZE is 10000 words.
    """
    CORESIZE = 10000

    # The actual core, represented as a list.
    # Empty strings represent unallocated words
    # within the core. Allocated words will
    # be represented as strings containing
    # instructions.
    core = ['' for index in range(CORESIZE)]

    """
    Initialise the core with a specified size.
    """
    def __init__(self, size):
        CORESIZE = size

    """
    Returns the size of the core.
    """
    @property
    def CORESIZE(self):
        return self.CORESIZE

    """
    Returns the instruction at the specified
    word position in the core, represented as a string.
    An empty string denotes an unallocated word.
    """
    @property
    def instruction(self, index):
        return self.core[index]

    """
    Puts the specified instruction in the
    specified word position. The instruction
    is assumed to be valid, and the original
    contents of the word are overwritten.
    """
    def put(self, instruction, index):
        self.core[index] = instruction

    """
    Add a program to the Core, specified as a list
    of instructions, and with the first instruction
    placed at the Core position specified by the index.
    """
    def add_program(self, instructions, index):
        #TODO
