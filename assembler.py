"""
Implements both an assembler, which converts Red Code instructions to a form
suitable for the Core, and a loader, which maps the assembled instructions into
the Core with a specified base address.

>>> from assemblytoken import AssemblyToken as Token
>>> from core import Core
>>> from assembler import Assembler
>>> core = Core()
>>> assembler = Assembler()
>>> opcode_token = Token(Token.MOV, 'MOV', 1, 1)
>>> a_val_token = Token(Token.INT, '0', 1, 1)
>>> comma_token = Token(Token.COMMA, ',', 1, 1)
>>> b_val_token = Token(Token.INT, '1', 1, 1)
>>> newline_token = Token(Token.NEWLINE, '\\n', 1, 1)
>>> eof_token = Token(Token.EOF, '', 1, 1)
>>> tokenlist = [opcode_token, a_val_token, comma_token, b_val_token, newline_token, eof_token]
>>> assembler.assemble(tokenlist, 1, core)
>>> core.print_instruction(1)
MOV 0, 1
>>> opcode_token = Token(Token.JMP, 'JMP', 1, 1)
>>> a_val_token = Token(Token.INT, '3', 1, 1)
>>> tokenlist = [opcode_token, a_val_token, newline_token, eof_token]
>>> assembler.assemble(tokenlist, 2, core)
>>> core.print_instruction(2)
JMP 3
>>> opcode_token = Token(Token.NOP, 'NOP', 1, 1)
>>> tokenlist = [opcode_token, newline_token, eof_token]
>>> assembler.assemble(tokenlist, 3, core)
>>> core.print_instruction(3)
NOP
>>> opcode_token = Token(Token.DAT, 'DAT', 1, 1)
>>> tokenlist = [opcode_token, b_val_token, newline_token, eof_token]
>>> assembler.assemble(tokenlist, 4, core)
>>> core.print_instruction(4)
DAT 1
>>> tokenlist = [opcode_token, a_val_token, comma_token, b_val_token, newline_token, eof_token]
>>> assembler.assemble(tokenlist, 5, core)
>>> core.print_instruction(5)
DAT 3, 1
"""

from assemblytoken import AssemblyToken as Token


class Assembler:

    def __init__(self):

        self.__tokenlist = []
        self.__tokenindex = 0
        self.__token = None
        self.__core = None
        self.__next_addr = 0  # The core address into which to map the instruction

    def __advance(self):
        """
        Advances to the next token
        """
        # Move to the next token
        self.__tokenindex += 1

        # Acquire the next token if there any left
        if not self.__tokenindex >= len(self.__tokenlist):
            self.__token = self.__tokenlist[self.__tokenindex]

    def __consume(self, expected_category):
        """
        Consumes a token from the list
        """
        if self.__token.category == expected_category:
            self.__advance()

        else:
            raise RuntimeError('Expecting ' + Token.catnames[expected_category] +
                               ' in line ' + str(self.__token.line))

    def assemble(self, tokenlist, address, core):
        """
        Assembles a Red Code program, and loads it into the
        core at the specified base address.

        :param tokenlist: The list of tokens representing a
        Red Code program
        :param address: The base address
        :param core: The core in which to install the program
        """

        if address < 0 or address > core.coresize:
            raise IndexError('Invalid core address specified')

        self.__tokenlist = tokenlist
        self.__tokenindex = 0
        self.__core = core
        self.__next_addr = address

        # Assign the first token
        self.__token = self.__tokenlist[self.__tokenindex]

        # Assemble all instructions until the end of file is
        # reached
        while self.__token.category != Token.EOF:
            self.__instruction()
            self.__consume(Token.NEWLINE)

            # Increment the address pointer
            if self.__next_addr == self.__core.coresize - 1:
                self.__next_addr = 0

            else:
                self.__next_addr += 1

    def __instruction(self):
        """
        Assembles the Red Code program given a list of tokens,
        and maps to the core at the specified base address.
        """

        if self.__token.category in [Token.MOV, Token.SEQ, Token.SNE, Token.CMP,
                                     Token.ADD, Token.SUB, Token.MUL, Token.DIV,
                                     Token.MOD]:
            # Assemble all instructions that take two operands
            self.__two_instr()

        elif self.__token.category in [Token.SLT, Token.LDP, Token.STP, Token.JMP,
                                       Token.JMZ, Token.JMN, Token.DJN, Token.SPL]:
            # Assemble all instructions that take one operand
            self.__one_instr()

        elif self.__token.category in [Token.NOP]:
            # Assemble all instructions that take no operands
            self.__zero_instr()

        elif self.__token.category in [Token.DAT]:
            # DAT is a special case, may take either one or two
            # operands
            self.__dat_instr()

        else:
            raise RuntimeError('Invalid opcode in line ', self.__token.line)

    def __two_instr(self):
        """
        Assembles a two operand instruction
        """

        # Record the opcode
        opcode = self.__token.category
        self.__advance()  # Advance past the opcode

        # Record the A-field addressing mode
        a_field_mode = self.__address_mode()

        # Record the A-field value
        a_field_val = self.__operand()

        self.__consume(Token.COMMA)

        # Record the B-field addressing mode
        b_field_mode = self.__address_mode()

        # Record the B-field value
        b_field_val = self.__operand()

        # Map the instruction into the core at the next address
        self.__core.put(opcode, a_field_mode, a_field_val,
                        b_field_mode, b_field_val, self.__next_addr)

    def __one_instr(self):
        """
        Assembles a one operand instruction
        """

        # Record the opcode
        opcode = self.__opcode()

        # Record the A-field addressing mode
        a_field_mode = self.__address_mode()

        # Record the A-field value
        a_field_val = self.__operand()

        # Map the instruction into the core at the next address
        self.__core.put(opcode, a_field_mode, a_field_val,
                        Token.NULL, Token.NULL, self.__next_addr)

    def __zero_instr(self):
        """
        Assembles a zero operand instruction
        """

        # Record the opcode
        opcode = self.__opcode()

        # Map the instruction into the core at the next address
        self.__core.put(opcode, Token.NULL, Token.NULL,
                        Token.NULL, Token.NULL, self.__next_addr)

    def __dat_instr(self):
        """
        Assembles a DAT instruction, which may take either one or
        two operands.
        """

        # Record the opcode
        opcode = self.__opcode()

        # Record the A-field addressing mode
        a_field_mode = self.__address_mode()

        # Record the A-field value
        a_field_val = self.__operand()

        if self.__token.category == Token.COMMA:
            # We have two operands
            self.__advance()  # Advance past the comma

            # Record the B-field addressing mode
            b_field_mode = self.__address_mode()

            # Record the B-field value
            b_field_val = self.__operand()

        else:
            # We only have one operand. By convention, DAT
            # with one operand places this in the B-field.
            b_field_mode = a_field_mode
            b_field_val = a_field_val

            a_field_mode = Token.NULL
            a_field_val = Token.NULL

        # Map the instruction into the core at the next address
        self.__core.put(opcode, a_field_mode, a_field_val,
                        b_field_mode, b_field_val, self.__next_addr)

    def __opcode(self):
        """
        Assembles an opcode

        :return: The opcode value
        """

        # Record the opcode
        opcode = self.__token.category
        self.__advance()  # Advance past the opcode

        return opcode

    def __address_mode(self):
        """
        Assembles an oprand addressing mode

        :return: The addressing mode value
        """

        if self.__token.category == Token.INT:
            # No addressing mode specified, so assume the default
            # mode of direct
            mode = Token.DIRECT

        elif self.__token.category in [Token.IMMEDIATE, Token.DIRECT, Token.INDIRECT]:
            mode = self.__token.category
            self.__advance()  # Advance past the addressing mode

        else:
            raise RuntimeError('Invalid A-field addressing mode in line ', self.__token.line)

        return mode

    def __operand(self):
        """
        Assembles an operand value.

        :return: The value of the operand
        """

        negative = False
        if self.__token.category == Token.MINUS:
            negative = True
            self.__advance()  # Advance past the unary minus

        if self.__token.category == Token.INT:
            operand = self.__token.lexeme
            self.__advance()  # Advance past the operand

            if negative:
                # Negate the operand
                operand = operand - (2 * operand)

            return operand

        else:
            raise RuntimeError('Invalid operand in line ', self.__token.line)

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
