"""
Executes a Red Code program by interpreting the assembled instructions
in the core
"""

from core import Core
from assemblytoken import AssemblyToken as Token

class Interpreter:

    def __init__(self, core):
        """
        Initialises the interpreter with the given core.

        :param core: The core in which the program to be executed resides

        """

        self.__core = core

    def __next(self, address):
        """
        Returns the next address in the core after the specified
        address, taking into account the need to wrap around.

        :param address: The address

        :return: The subsequent address
        """

        if address == self.__core.coresize - 1:
            # Need to wrap around
            return 0

        else:
            return address + 1

    def execute(self, address):
        """
        Executes an instruction, and returns the address of the
        next instruction to be executed. If an attempt is made to
        execute a DAT, raises

        :param address: The address of the instruction

        :return: The new address of the program counter.
        """

        opcode = self.__core.opcode(address)

        if opcode == Token.NOP:
            # Instruction has no effect
            return self.__next(address)

        elif opcode == Token.DAT:
            # Cannot execute a DAT
            raise RuntimeError('Attempt to execute DAT')

        elif opcode == Token.MOV:
            #TODO
            pass

        elif opcode == Token.ADD:
            #TODO
            pass

        elif opcode == Token.SUB:
            #todo
            pass

        elif opcode == Token.MUL:
            #todo
            pass

        elif opcode == Token.DIV:
            #todo
            pass

        elif opcode == Token.MOD:
            #todo
            pass

        elif opcode == Token.JMP:
            #todo
            pass

        elif opcode == Token.JMZ:
            #todo
            pass

        elif opcode == Token.JMN:
            #todo
            pass

        elif opcode == Token.DJN:
            #todo
            pass

        elif opcode == Token.SPL:
            #todo
            pass

        elif opcode == Token.CMP:
            #todo
            pass

        elif opcode == Token.SEQ:
            #todo
            pass

        elif opcode == Token.SNE:
            #todo
            pass

        elif opcode == Token.SLT:
            #todo
            pass

        elif opcode == Token.LDP:
            #todo
            pass

        elif opcode == Token.STP:
            #todo
            pass

        else:
            raise RuntimeError('Unrecognised opcode')
