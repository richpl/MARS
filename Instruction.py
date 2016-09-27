#! /usr/bin/python

"""
This class provides a representation for Red Code
instructions, and implements the logic behind
those instructions. Each instruction is represented
as a triple (held within a list), consisting of
opcode, A-field operand and B-field operand.
"""

import re

class Instruction:

    # Possible opcodes
    DAT = 'dat'
    MOV = 'mov'
    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'
    MOD = 'mod'
    JMP = 'jmp'
    JMZ = 'jmz'
    JMN = 'jmn'
    DJN = 'djn'
    SPL = 'spl'
    CMP = 'cmp'
    SEQ = 'seq'
    SNE = 'sne'
    SLT = 'slt'
    LDP = 'ldp'
    STP = 'stp'
    NOP = 'nop'

    """
    Regular expression with which to
    validate operands, with capture
    groups to acquire addressing mode
    and value
    """
    __operand_format = re.compile(r'([#$*@{<}>]?)(\d+)')

    """
    Regular expression with which to
    validate opcodes.
    """
    __opcode_format = re.compile(r'dat|mov|sub|mul|' +
                                 r'div|mod|jmp|jmz|' +
                                 r'jmn|djn|spl|cmp|' +
                                 r'seq|sne|slt|ldp|' +
                                 r'stp|nop')

    """
    Immediate addressing
    """
    IMMEDIATE = '#'

    """
    Direct addressing
    """
    DIRECT = '$'

    """
    A-field indirect addressing
    """
    A_INDIRECT = '*'

    """
    B-field indirect addressing
    """
    B_INDIRECT = '@'

    """
    A-field indirect addressing with
    predecrement
    """
    A_INDIRECT_PRE = '{'

    """
    B-field indirect addressing with
    predecrement
    """
    B_INDIRECT_PRE = '<'

    """
    A-field indirect addressing with
    postincrement
       """
    A_INDIRECT_POST = '}'

    """
    B-field indirect addressing with
    postincrement
    """
    B_INDIRECT_POST = '>'

    """
    Returns the addressing mode of the
    specified operand, which is represented
    as a string. If no addressing mode is
    specified, the default mode of direct
    is assumed.

    If the operand is improperly formatted,
    then a SyntaxError is raised.
    """
    def __address_mode(self, operand):

        # Validate the operand
        m = self.__operand_format.match(operand)
        if not m:
            raise SyntaxError('Invalid operand')

        # Check if the addressing mode is
        # missing, in which case direct is
        # implied
        mode = m.groups()[0]
        if mode:
            return mode
        else:
            return self.DIRECT

    """
    Returns the value of the
    specified operand, which is represented
    as an integer.

    If the operand is improperly formatted,
    then a SyntaxError is raised.
    """
    def __operand_val(self, operand):

        # Validate the operand
        m = self.__operand_format.match(operand)
        if not m:
            raise SyntaxError('Invalid operand')

        return int(m.groups()[1])

    """
    Returns the opcode for this instruction,
    which is assumed to be a three element
    list containing the opcode, A-field and
    B-field in that order.
    If the opcode is not recognised, or the
    instruction is malformed, a
    SyntaxError is raised
    """
    @classmethod
    def opcode(self, instruction):

        if not len(instruction == 3):
            raise SyntaxError("Invalid instruction")

        # Validate the opcode
        opcode = instruction[0]
        m = self.__opcode_format(opcode)
        if not m:
            raise SyntaxError("Invalid opcode")

        return opcode

    """
    Returns the addressing mode of the A-field
    in the specified instruction, as a string.
    Raises a SyntaxError if the A-field is malformed.
    """
    @classmethod
    def a_field_mode(self, instruction):

        if not len(instruction == 3):
            raise SyntaxError("Invalid instruction")

        return self.__address_mode(instruction[1])


    """
    Returns the value of the A-field
    in the specified instruction, as an integer.
    Raises a SyntaxError if the A-field is malformed.
    """
    @classmethod
    def a_field_val(self, instruction):

        if not len(instruction == 3):
            raise SyntaxError("Invalid instruction")

        return self.__operand_val(instruction[1])

    """
    Returns the addressing mode of the B-field
    in the specified instruction, as a string.
    Raises a SyntaxError if the B-field is malformed.
    """
    @classmethod
    def b_field_mode(self, instruction):

        if not len(instruction == 3):
            raise SyntaxError("Invalid instruction")

        return self.__address_mode(instruction[2])

    """
    Returns the value of the B-field
    in the specified instruction, as an integer.
    Raises a SyntaxError if the B-field is malformed.
    """
    @classmethod
    def b_field_val(self, instruction):

        if not len(instruction == 3):
            raise SyntaxError("Invalid instruction")

        return self.__operand_val(instruction[2])