"""
Executes a list of Red Code programs by interpreting the assembled instructions
in the core. All programs will be executed until there are none
with any processes left.

Each program will be permitted to execute one
process in turn before relinquishing control to the next
process, e.g.

        program A, process 1
        program B, process 1
        program A, process 2
        program B, process 2
        program A, process 1
        program B, process 3
        ...

A process is terminated when it attempts to execute
either a DAT instruction or attempts to execute
an instruction using a core address which holds no valid
instruction (the core is initialised with
null values).
"""

from core import Core
from assemblytoken import AssemblyToken as Token


class Program:
    """
    Class to model a program, which is a list
    of processes (defined by the program counter for
    that process) and an index into that list.
    """

    def __init__(self, base_address):
        """
        Initialise the program

        :param base_address: The core base address of the program
        """

        # Maintain a list of processes
        self.__processes = [base_address]

        # Index into the list, initialised at
        # the first entry
        self.__index = 0

    def add_process(self, address):
        """
        Adds a new process to the process list
        for this program.

        :param address: The base address of the process
        """

        self.__processes.append(address)

    def current_process_pc(self):
        """
        Returns the program counter
        of the current process

        :return: The program counter of the current process
        """

        if len(self.__processes) == 0:
            raise IndexError('No more processes to run')

        return self.__processes[self.__index]

    def next_process(self):
        """
        Moves to the next process in the process list,
        if there is one.
        """

        if len(self.__processes) == 0:
            raise IndexError('No next process')

        # Increment the index, wrapping around to
        # the start of the list if necessary
        if self.__index == len(self.__processes) - 1:
            self.__index = 0

        else:
            self.__index += 1

    def kill_current_process(self):
        """
        Kill the current process and remove it from
        the process list.
        """

        if len(self.__processes) == 0:
            raise IndexError('No more processes to kill')

        del self.__processes[self.__index]

    def update_current_process_pc(self, address):
        """
        Updates the program counter of the current
        process with the new address.

        :param address: New program counter value
        """

        if len(self.__processes) == 0:
            raise IndexError('No more processes to update')

        self.__processes[self.__index] = address


class Interpreter:

    def __init__(self, core, base_addresses):
        """
        Initialises the interpreter with the given core.

        :param core: The core in which the program to be executed resides
        :param base_addresses: List of base addresses at which programs reside

        """

        self.__core = core

        # Initialise a dictionary to map programs to processes that they have spawned,
        # where each process is defined by its program counter. Upon creation
        # there will be just one process per program, starting at the base address
        self.__programs = []
        for base_address in base_addresses:
            self.__programs[base_address] = Program(base_address)

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

        elif opcode == Token.NULL:
            raise RuntimeError('Attempt to execute null instruction')

        else:
            raise RuntimeError('Unrecognised opcode')

    def run(self):
        """
        Executes all of the programs in the core.
        """

        # Keep executing programs for as long
        # as they have processes
        for program in self.__programs:
            try:
                address = program.current_process_pc()

                try:
                    new_address = self.execute(address)
                    program.update_current_process_pc(new_address)

                    # Move to the next process
                    program.next_process()

                except RuntimeError:
                    # Exception in program execution, kill
                    # the current process
                    program.kill_current_process()

            except IndexError:
                # No processes left for this
                # program, so remove it
                index = self.__programs.index(program)
                del self.__programs[index]

