"""
Executes a list of Red Code programs by interpreting the assembled instructions
in the core. All programs will be executed until there are none
with any processes left.

Each program will be permitted to execute one
process in turn before relinquishing control to the next
program, e.g.

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

>>> #
>>> # Test the program dictionary
>>> #
>>> from interpreter import Program
>>> program = Program(1000)
>>> print(program.current_process_pc())
1000
>>> program.add_process(2000)
>>> program.next_process()
>>> print(program.current_process_pc())
2000
>>> program.update_current_process_pc(3000)
>>> print(program.current_process_pc())
3000
>>> program.next_process()
>>> print(program.current_process_pc())
1000
>>> program.kill_current_process()
>>> print(program.current_process_pc())
3000
>>> #
>>> # Test the interpreter
>>> #
>>> from core import Core
>>> from assemblytoken import AssemblyToken as Token
>>> from interpreter import Interpreter
>>> core = Core()
>>> interpreter = Interpreter(core, [4000])
>>> # Test processing of MOV $0, $1 instruction
>>> core.put_instr(Token.MOV, Token.DIRECT, 0, Token.DIRECT, 1, 4000)
>>> core.print_instruction(4000)
MOV 0, 1
>>> core.print_instruction(4001)
NULL
>>> next_address = interpreter.execute(4000)
>>> print(next_address)
4001
>>> # Expect entire instruction to be copied to next address
>>> core.print_instruction(4001)
MOV 0, 1
>>> # Test processing of MOV #0, #1
>>> core.put_a_field_mode(Token.IMMEDIATE, 4001)
>>> core.put_b_field_mode(Token.IMMEDIATE, 4001)
>>> core.print_instruction(4001)
MOV #0, #1
>>> next_address = interpreter.execute(4001)
>>> print(next_address)
4002
>>> # Expect A-field to be copied to B-field
>>> core.print_instruction(4001)
MOV #0, #0
>>> # Test processing of MOV -1, #0
>>> core.put_a_field_mode(Token.DIRECT, 4001)
>>> core.put_a_field_val(-1, 4001)
>>> core.print_instruction(4001)
MOV -1, #0
>>> next_address = interpreter.execute(4001)
>>> # Expect B-field of prior instruction to be
>>> # copied to B-field of this instruction
>>> core.print_instruction(4001)
MOV -1, #1
>>> # Test processing of MOV 2, @2
>>> core.put_instr(Token.MOV, Token.DIRECT, 2, Token.INDIRECT, 2, 5000)
>>> core.print_instruction(5000)
MOV 2, @2
>>> core.put_instr(Token.DAT, Token.IMMEDIATE, 0, Token.IMMEDIATE, 4, 5002)
>>> next_address = interpreter.execute(5000)
>>> core.print_instruction(5006)
DAT #0, #4
>>> # Test processing of MOV @-2, 0
>>> core.put_instr(Token.MOV, Token.INDIRECT, -2, Token.DIRECT, 0, 6000)
>>> core.print_instruction(6000)
MOV @-2, 0
>>> core.put_instr(Token.DAT, Token.IMMEDIATE, -1, Token.IMMEDIATE, 0, 5998)
>>> core.put_instr(Token.DAT, Token.IMMEDIATE, 4, Token.IMMEDIATE, 0, 5997)
>>> next_address = interpreter.execute(6000)
>>> core.print_instruction(6000)
DAT #4, #0
>>> # Test processing of JMP #2000
>>> core.put_instr(Token.JMP, Token.IMMEDIATE, 2000, Token.NULL, Token.NULL, 4002)
>>> core.print_instruction(4002)
JMP #2000
>>> next_address = interpreter.execute(4002)
>>> print(next_address)
2000
"""

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
        # there will be just one process per program, with the base address as key.
        self.__programs = {}
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

    def __get_direct_address(self, direct_val, address):
        """
        Resolve the absolute address pointed to by the direct value,
        relative to the specified address

        :param direct_val: A direct addressing mode value
        :param address: The address from which to calculate the address being
        pointed to

        :return: The absolute address which is being pointed to
        """

        if address < 0 or address >= self.__core.coresize:
            raise IndexError('Invalid address specified')

        return (direct_val + address) % self.__core.coresize

    def __execute_add(self, address):
        """
        Executes the ADD instruction.

        :param address: The address of the ADD instruction

        :return: The address of the next instruction
        """

        # Acquire operand modes and values
        a_mode = self.__core.a_field_mode(address)
        a_val = self.__core.a_field_val(address)

        b_mode = self.__core.b_field_mode(address)
        b_val = self.__core.b_field_val(address)

        if a_mode == Token.IMMEDIATE:
            if b_mode == Token.IMMEDIATE:
                # Add A-field to B-field
                self.__core.put_b_field_val(b_val + a_val, address)

            elif b_mode == Token.DIRECT:
                # Add A-field to instruction pointed to by B-field
                dest_address = self.__get_direct_address(b_val, address)
                b_val = self.__core.b_field_val(dest_address)
                self.__core.put_b_field_val(b_val + a_val, dest_address)

            elif b_mode == Token.INDIRECT:
                # TODO
                pass

        elif a_mode == Token.DIRECT:
            if b_mode == Token.IMMEDIATE:
                # Add instruction pointed to by A-field to B-field
                src_address = self.__get_direct_address(a_val, address)
                src_b_val = self.__core.b_field_val(src_address)
                self.__core.put_b_field_val(b_val + src_b_val, address)

            elif b_mode == Token.DIRECT:
                pass

            elif b_mode == Token.INDIRECT:
                pass

        else:  # A-field is INDIRECT
            if b_mode == Token.IMMEDIATE:
                pass

            elif b_mode == Token.DIRECT:
                pass

            elif b_mode == Token.INDIRECT:
                pass

        # Return the next instruction address
        return self.__next(address)

    def __execute_jmp(self, address):
        """
        Executes the JMP instruction. Only the A-field is used.
        Addressing mode is expected to be either immediate or
        direct.

        :param address: The address of the JMP instruction

        :return: The address to which to jump
        """

        # Acquire operand modes and values
        a_mode = self.__core.a_field_mode(address)
        a_val = self.__core.a_field_val(address)

        if a_mode == Token.IMMEDIATE:
            return self.__core.a_field_val(address)

        elif a_mode == Token.DIRECT:
            dest_address = self.__get_direct_address(a_val, address)
            return self.__core.a_field_val(dest_address)

        else:
            raise RuntimeError('Invalid JMP addressing mode')

    def __execute_mov(self, address):
        """
        Executes the MOV instruction.

        :param address: The address of the MOV instruction

        :return: The address of the next instruction
        """

        # Acquire operand modes and values
        a_mode = self.__core.a_field_mode(address)
        a_val = self.__core.a_field_val(address)

        b_mode = self.__core.b_field_mode(address)
        b_val = self.__core.b_field_val(address)

        if a_mode == Token.IMMEDIATE:
            if b_mode == Token.IMMEDIATE:
                self.__core.put_b_field_val(a_val, address)

            elif b_mode == Token.DIRECT:
                dest_address = self.__get_direct_address(b_val, address)
                self.__core.put_b_field_val(a_val, dest_address)

            elif b_mode == Token.INDIRECT:
                intermediate_address = self.__get_direct_address(b_val, address)
                intermediate_b_val = self.__core.b_field_val(intermediate_address)
                dest_address = self.__get_direct_address(b_val + intermediate_b_val, address)
                self.__core.put_b_field_val(a_val, dest_address)

        elif a_mode == Token.DIRECT:
            src_address = self.__get_direct_address(a_val, address)

            if b_mode == Token.IMMEDIATE:
                b_val = self.__core.b_field_val(src_address)
                self.__core.put_b_field_val(b_val, address)

            elif b_mode == Token.DIRECT:
                dest_address = self.__get_direct_address(b_val, address)
                self.__core.put_instr(self.__core.opcode(src_address),
                                      self.__core.a_field_mode(src_address),
                                      self.__core.a_field_val(src_address),
                                      self.__core.b_field_mode(src_address),
                                      self.__core.b_field_val(src_address),
                                      dest_address)

            elif b_mode == Token.INDIRECT:
                intermediate_address = self.__get_direct_address(b_val, address)
                intermediate_b_val = self.__core.b_field_val(intermediate_address)
                dest_address = self.__get_direct_address(b_val + intermediate_b_val, address)
                self.__core.put_instr(self.__core.opcode(src_address),
                                      self.__core.a_field_mode(src_address),
                                      self.__core.a_field_val(src_address),
                                      self.__core.b_field_mode(src_address),
                                      self.__core.b_field_val(src_address),
                                      dest_address)

        else:  # A-field is INDIRECT
            intermediate_address = self.__get_direct_address(a_val, address)
            intermediate_a_val = self.__core.a_field_val(intermediate_address)
            src_address = self.__get_direct_address(a_val + intermediate_a_val, address)

            if b_mode == Token.IMMEDIATE:
                src_a_val = self.__core.a_field_val(src_address)
                self.__core.put_b_field_val(src_a_val, address)

            elif b_mode == Token.DIRECT:
                dest_address = self.__get_direct_address(b_val, address)
                self.__core.put_instr(self.__core.opcode(src_address),
                                      self.__core.a_field_mode(src_address),
                                      self.__core.a_field_val(src_address),
                                      self.__core.b_field_mode(src_address),
                                      self.__core.b_field_val(src_address),
                                      dest_address)

            elif b_mode == Token.INDIRECT:
                intermediate_address = self.__get_direct_address(b_val, address)
                intermediate_b_val = self.__core.b_field_val(intermediate_address)
                dest_address = self.__get_direct_address(b_val + intermediate_b_val, address)
                self.__core.put_instr(self.__core.opcode(src_address),
                                      self.__core.a_field_mode(src_address),
                                      self.__core.a_field_val(src_address),
                                      self.__core.b_field_mode(src_address),
                                      self.__core.b_field_val(src_address),
                                      dest_address)

        # Return the next instruction address
        return self.__next(address)

    def execute(self, address):
        """
        Executes an instruction, and returns the address of the
        next instruction to be executed. If an attempt is made to
        execute a DAT, raises

        :param address: The address of the instruction

        :return: The new address of the program counter.
        """

        if address < 0 or address >= self.__core.coresize:
            raise RuntimeError('Attempt to execute instruction at invalid address')

        opcode = self.__core.opcode(address)

        if opcode == Token.NOP:
            # Instruction has no effect
            return self.__next(address)

        elif opcode == Token.DAT:
            # Cannot execute a DAT
            raise RuntimeError('Attempt to execute DAT')

        elif opcode == Token.MOV:
            return self.__execute_mov(address)

        elif opcode == Token.ADD:
            # TODO
            pass

        elif opcode == Token.SUB:
            # todo
            pass

        elif opcode == Token.MUL:
            # todo
            pass

        elif opcode == Token.DIV:
            # todo
            pass

        elif opcode == Token.MOD:
            # todo
            pass

        elif opcode == Token.JMP:
            return self.__execute_jmp(address)

        elif opcode == Token.JMZ:
            # todo
            pass

        elif opcode == Token.JMN:
            # todo
            pass

        elif opcode == Token.DJN:
            # todo
            pass

        elif opcode == Token.SPL:
            # todo
            pass

        elif opcode == Token.CMP:
            # todo
            pass

        elif opcode == Token.SEQ:
            # todo
            pass

        elif opcode == Token.SNE:
            # todo
            pass

        elif opcode == Token.SLT:
            # todo
            pass

        elif opcode == Token.LDP:
            # todo
            pass

        elif opcode == Token.STP:
            # todo
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
                del self.__programs[program]
