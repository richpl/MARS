#! /usr/bin/python

"""Class to represent a token for the Red Code
assembly language. A token consists of
two items:

category    Category of the token
lexeme      Token in string form
"""


class AssemblyToken:

        """AssemblyToken categories"""

        # Opcodes

        DAT = 0
        MOV = 1
        ADD = 2
        SUB = 3
        MUL = 4
        DIV = 5
        MOD = 6
        JMP = 7
        JMZ = 8
        JMN = 9
        DJN = 10
        SPL = 11
        CMP = 12
        SEQ = 13
        SNE = 14
        SLT = 15
        LDP = 16
        STP = 17
        NOP = 18

        # Address modes

        IMMEDIATE = 19
        DIRECT = 20
        A_INDIRECT = 21
        B_INDIRECT = 22
        A_INDIRECT_PRE = 23
        B_INDIRECT_PRE = 24
        A_INDIRECT_POST = 25
        B_INDIRECT_POST = 26

        # Displayable names for each token category
        catnames = ['DAT', 'MOV', 'ADD', 'SUB', 'MUL',
                    'DIV', 'MOD', 'JMP', 'JMZ', 'JMN', 'DJN', 'SPL',
                    'CMP', 'SEQ', 'SNE', 'SLT', 'LDP', 'STP', 'NOP',
                    'IMMEDIATE', 'DIRECT', 'A_INDIRECT',
                    'B_INDIRECT', 'A_INDIRECT_PRE', 'B_INDIRECT_PRE',
                    'A_INDIRECT_POST', 'B_INDIRECT_POST']

        smalltokens = {'#': IMMEDIATE, '$': DIRECT,
                       '*': A_INDIRECT, '@': B_INDIRECT,
                       '{': A_INDIRECT_PRE, '<': B_INDIRECT_PRE,
                       '}': A_INDIRECT_POST, '>': B_INDIRECT_POST}

        # Dictionary of BASIC reserved words
        keywords = {'DAT': DAT, 'MOV': MOV,
                    'ADD': ADD, 'SUB': SUB, 'MUL': MUL,
                    'DIV': DIV, 'MOD': MOD, 'JMP': JMP,
                    'JMZ': JMZ, 'JMN': JMN, 'DJN': DJN,
                    'SPL': SPL, 'CMP': CMP, 'SEQ': SEQ,
                    'SNE': SNE, 'SLT': SLT, 'LDP': LDP,
                    'STP': STP, 'NOP': NOP}

        def __init__(self, category, lexeme):

            self.category = category  # Category of the token
            self.lexeme = lexeme      # Token in string form

        def pretty_print(self):
            """Pretty prints the token
            """
            print('Category:', self.catnames[self.category],
                  'Lexeme:', self.lexeme)

        def print_lexeme(self):
            print(self.lexeme, end=' ')
