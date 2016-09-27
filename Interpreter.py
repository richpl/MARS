#! /usr/bin/python

import Instruction

"""
This class implements a red code interpreter that
executes the instruction at the specified core
address, and also updates the program counter
accordingly.
"""

class Interpreter:

    """
    Initialises the interpreter to execute Red
    Code instructions within the specified core.
    """
    def __init__(self, core):

        self.core = core

    """
    Executes the instruction at the
    specified core address, and returns
    the new value of the program counter
    resulting from that instruction.

    Raises an IndexError if the
    specified address is not a valid core
    address.
    """
    def execute(self, address):

        if address < 0 or address > self.core.CORESIZE:
            raise IndexError("Invalid core address")
        else:
            # Extract entire instruction
            instruction = self.core.instruction(address)

            # Break out instruction opcode and
            # operands
            try:
                opcode = Instruction.opcode(instruction)
                a_field_mode = Instruction.a_field_mode(instruction)
                a_field_val = Instruction.a_field_val(instruction)
                b_field_mode = Instruction.b_field_mode(instruction)
                b_field_val = Instruction.b_field_val(instruction)

            except SyntaxError as err:
                raise SyntaxError(str(err))


