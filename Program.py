#! /usr/bin/python

"""
This class represents a Red Code program
running within the Core. The program may
have multiple execution threads associated
with it, each of which is represented by
an instruction pointer referencing a
particular word position in the core.
"""

class Program:

    # A list of program counters to
    # support multithreaded operation, where
    # each program counter is a word position
    # in the core
    pc = []

    """
    Initialise the process to begin
    execution at the specified Core
    address. It is assumed that the
    specified index is a valid
    address for the core. A negative
    index will cause an IndexError
    to be raised.
    """
    def __init__(self, core, index):

        if index < 0:
            raise IndexError("Invalid core address")
        else:
            self.pc.append(index)

    """
    Returns a list of the program counters
    associated with all of the executing threads
    for this program.
    """
    def pcs(self):
        return pc


