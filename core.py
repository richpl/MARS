#! /usr/bin/python

"""
A class representing the core within which Red Code programs
can run. The core consists of an ordered list of words, each
either empty or containing a single Red Code instruction.
Addresses in the core run from 0 to coresize-1, with the
expectation that the core will wrap around so that the
address above coresize-1 is 0.

>>> from core import Core
>>> from assemblytoken import AssemblyToken as Token
>>> core = Core()
>>> opcode = Token.MOV
>>> a_field_mode = Token.DIRECT
>>> a_field_val = 0
>>> b_field_mode = Token.DIRECT
>>> b_field_val = 1
>>> core.put(opcode, a_field_mode, a_field_val, b_field_mode, b_field_val, 4000)
>>> print (core.coresize)
8000
>>> core.print_instruction(4000)
MOV 0, 1
"""

from assemblytoken import AssemblyToken as Token


class Core:

    """
    Initialise the core with a specified size. The core
    will initially be filled with NULLs.
    """
    def __init__(self, size=8000):

        assert isinstance(size, int)

        self.__core = [[Token.NULL, Token.NULL, Token.NULL,
                        Token.NULL, Token.NULL]
                       for index in range(size)]

    """
    Returns the size of the core.
    """
    @property
    def coresize(self):

        return len(self.__core)

    """
    Returns the opcode value (given by AssemblyToken) at the specified address.
    """
    def opcode(self, address):

        if address < 0 or address > self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][0]

    """
    Returns the A-field addressing mode value (given by AssemblyToken) 
    at the specified address.
    """
    def a_field_mode(self, address):

        if address < 0 or address > self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][1]

    """
    Returns the A-field value
    at the specified address.
    """
    def a_field_val(self, address):

        if address < 0 or address > self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][2]

    """
    Returns the B-field addressing mode value (given by AssemblyToken) 
    at the specified address.
    """
    def b_field_mode(self, address):

        if address < 0 or address > self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][3]

    """
    Returns the B-field value
    at the specified address.
    """
    def b_field_val(self, address):

        if address < 0 or address > self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][4]

    """
    Puts the specified instruction in the
    specified word position. The instruction
    is assumed to be valid, and the original
    contents of the word are overwritten.
    
    :param opcode: The numeric value representing the opcode
    :param a_field_mode: A-field addressing mode
    :param a_field_val: A-field value
    :param b_field_mode: B-field addressing mode
    :param b_field_val: B-field value
    :param address: The address at which to insert the instruction
    """
    def put(self,  opcode, a_field_mode, a_field_val,
            b_field_mode, b_field_val, address):

        if address < 0 or address > self.coresize:
            raise IndexError('Invalid address specified')

        self.__core[address] = [opcode, a_field_mode, a_field_val,
                                b_field_mode, b_field_val]

    """
    Pretty prints the instruction at the specified address
    """
    def print_instruction(self, address):

        if address < 0 or address > self.coresize:
            raise IndexError('Invalid address specified')

        [opcode, a_field_mode, a_field_val,
         b_field_mode, b_field_val] = self.__core[address]

        # Generate a string to represent the A-field
        # addressing mode
        a_mode_str = ''  # IMMEDIATE mode

        if a_field_mode == Token.IMMEDIATE:
            a_mode_str = '#'

        elif a_field_mode == Token.A_INDIRECT:
            a_mode_str = '*'

        elif a_field_mode == Token.A_INDIRECT_PRE:
            a_mode_str = '{'

        elif a_field_mode == Token.A_INDIRECT_POST:
            a_mode_str = '}'

        # Generate a string to represent the B-field
        # addressing mode
        b_mode_str = ''  # IMMEDIATE mode

        if b_field_mode == Token.IMMEDIATE:
            b_mode_str = '#'

        elif b_field_mode == Token.B_INDIRECT:
            b_mode_str = '@'

        elif b_field_mode == Token.B_INDIRECT_PRE:
            b_mode_str = '<'

        elif b_field_mode == Token.B_INDIRECT_POST:
            b_mode_str = '>'

        print(Token.catnames[opcode], end='')

        if a_field_val != Token.NULL:
            print (' ', end='')
            print(a_mode_str, end='')
            print(a_field_val, end='')

        if b_field_val != Token.NULL:
            if opcode == Token.DAT and a_field_val == Token.NULL:
                print(' ', end='')

            else:
                print(', ', end='')

            print(b_mode_str, end='')
            print(b_field_val)

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
