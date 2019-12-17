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
>>> core.put_instr(opcode, a_field_mode, a_field_val, b_field_mode, b_field_val, 4000)
>>> print (core.coresize)
8000
>>> core.print_instruction(4000)
MOV 0, 1
"""

from assemblytoken import AssemblyToken as Token


class Core:

    def __init__(self, size=8000):
        """
        Initialise the core with a specified size. The core
        will initially be filled with NULLs.
        """

        assert isinstance(size, int)

        self.__core = [[Token.NULL, Token.NULL, Token.NULL,
                        Token.NULL, Token.NULL]
                       for index in range(size)]

    @property
    def coresize(self):
        """
        Returns the size of the core.
        """

        return len(self.__core)

    def opcode(self, address):
        """
        Returns the opcode value (given by AssemblyToken) at the specified address.
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][0]

    def a_field_mode(self, address):
        """
        Returns the A-field addressing mode value (given by AssemblyToken)
        at the specified address.
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][1]

    def a_field_val(self, address):
        """
        Returns the A-field value
        at the specified address.
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][2]

    def b_field_mode(self, address):
        """
        Returns the B-field addressing mode value (given by AssemblyToken)
        at the specified address.
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][3]

    def b_field_val(self, address):
        """
        Returns the B-field value
        at the specified address.
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        return self.__core[address][4]

    def put_instr(self, opcode, a_field_mode, a_field_val,
            b_field_mode, b_field_val, address):
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

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        self.__core[address] = [opcode, a_field_mode, a_field_val,
                                b_field_mode, b_field_val]

    def put_opcode(self, opcode, address):
        """
        Puts the specified opcode in the
        specified word position. The opcode
        is assumed to be valid, and the original
        contents are overwritten.

        :param opcode: The numeric value representing the opcode
        :param address: The address at which to insert the opcode
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        self.__core[address][0] = opcode

    def put_a_field_mode(self, a_field_mode, address):
        """
        Puts the specified A-field mode in the
        specified word position. The A-field mode
        is assumed to be valid, and the original
        contents are overwritten.

        :param a_field_mode: A-field addressing mode
        :param address: The address at which to insert the mode
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        self.__core[address][1] = a_field_mode

    def put_a_field_val(self, a_field_val, address):
        """
        Puts the specified A-field value in the
        specified word position. The A-field value
        is assumed to be valid, and the original
        contents are overwritten.

        :param a_field_val: A-field value
        :param address: The address at which to insert the value
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        self.__core[address][2] = a_field_val

    def put_b_field_mode(self, b_field_mode, address):
        """
        Puts the specified B-field mode in the
        specified word position. The B-field mode
        is assumed to be valid, and the original
        contents are overwritten.

        :param b_field_mode: B-field addressing mode
        :param address: The address at which to insert the mode
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        self.__core[address][3] = b_field_mode

    def put_b_field_val(self, b_field_val, address):
        """
        Puts the specified B-field value in the
        specified word position. The B-field value
        is assumed to be valid, and the original
        contents are overwritten.

        :param b_field_val: B-field value
        :param address: The address at which to insert the value
        """

        if address < 0 or address >= self.coresize:
            raise IndexError('Invalid address specified')

        self.__core[address][4] = b_field_val

    def print_instruction(self, address):
        """
        Pretty prints the instruction at the specified address
        """

        if address < 0 or address >= self.coresize:
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
