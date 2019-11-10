#! /usr/bin/python

"""
This class represents a Red Code program
running within the Core. The program may
have multiple execution threads associated
with it, each of which is represented by
an instruction pointer referencing a
particular word position in the core.
"""

class Process:

    """
    A list of program counters to
    support multithreaded operation, where
    each program counter is a word position
    in the core.
    """
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
    def __init__(self, core, address):

        if address < 0 or address > core.CORESIZE:
            raise IndexError("Invalid core address")
        else:
            self.pc.append(address)

    """
    Returns a list of the program counters
    associated with all of the executing threads
    for this program.
    """
    @property
    def pc(self):

        return self.pc

    """
    Modifies the specified program counter
    to the new core address. Raises an
    IndexError if the specified core address
    is not valid.
    The index provides an offset into the list
    of program counters to select the one to be
    modified, while the address is the new core
    address to which it is to be set.
    """
    def set_pc(self, index, address, core):

        if index < 0 or index > len(self.pc):
            raise IndexError("Invalid PC offset")
        elif address < 0 or address > core.CORESIZE:
            raise IndexError("Invalid core address")
        else:
            self.pc[index] = address