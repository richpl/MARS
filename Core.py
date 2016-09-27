#! /usr/bin/python

"""
A class representing the core within which Red Code programs
can run. The core consists of an ordered list of words, each
either empty or containing a single Red Code instruction. The
core wraps so that writing a sequence of words that overruns
the end of the core will result in the write wrapping around
to the beginning of the core.

>>> core = Core(5000)
>>> core.put([Instruction.MOV, 0, 1], 4000)
>>> print (core.CORESIZE)
5000
>>> print (core.instruction(4000))
[mov, 0, 1]
>>> program[0] = [Instruction.MOV, 0, 1]
>>> program[1] = [Instruction.MOV, 1, 0]
>>> core.add_program(program, 4500)
>>> print (core.instruction(4500))
[mov, 0, 1]
>>> print (core.instruction(4501))
[mov, 1, 0]
"""


class Core:

    """
    Default CORESIZE is 10000 words.
    """
    CORESIZE = 10000

    """
    Initialise the core with a specified size.
    """
    def __init__(self, size):

        self.CORESIZE = size

        # The actual core, represented as a list.
        # Empty strings represent unallocated words
        # within the core. Allocated words will
        # be represented as strings containing
        # instructions.
        core = ['' for index in range(self.CORESIZE)]

    """
    Returns the size of the core.
    """
    @property
    def CORESIZE(self):

        return self.CORESIZE

    """
    Returns the instruction at the specified
    word position in the core, represented as a triple
    held within the list. The triple consists of
    opcode, A-field operand and B-field operand.
    Each component of the list is a string.
    An empty list denotes an unallocated word.
    """
    @property
    def instruction(self, address):

        assert isinstance(address, int)
        return self.core[address]

    """
    Puts the specified instruction in the
    specified word position. The instruction
    is assumed to be valid, and the original
    contents of the word are overwritten.
    """
    def put(self, instruction, address):

        self.core[address] = instruction

    """
    Add a program to the Core, specified as a list
    of instructions, and with the first instruction
    placed at the Core position specified by the index.
    Each individual instruction is a three element list,
    consisting of opcode, A-field and B-field.

    The instructions will be written to sequential
    locations in the core, irrespective of what is
    already stored there. If the instruction sequence
    would overrun the end of the core, then the
    sequence is wrapped around to the start of the core.
    """
    def add_program(self, instructions, address):

        if address < 0 or address > self.CORESIZE:
            raise IndexError("Invalid core address")
        else:
            current_address = address

            assert isinstance(instructions, list)
            for instruction in instructions:
                if current_address < self.CORESIZE:
                    self.core[current_address] = instruction
                    current_address = current_address + 1
                else:
                    # We need to wrap around
                    self.core[0] = instruction
                    current_address = 1

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
