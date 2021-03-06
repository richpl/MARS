#! /usr/bin/python

"""
Class to represent a token for the Red Code
assembly language. A token consists of
four items:

category    Category of the token
lexeme      Token in string form
column      Column in which token starts
line        Line in the file on which token appears
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

        IMMEDIATE =       19
        DIRECT =          20
        INDIRECT =        21

        # Immediate values

        INT =   22
        MINUS = 23

        # File markers

        EOF =     24
        NEWLINE = 25

        # Punctuation

        COMMA = 26
        NULL =  27  # Denotes a null field

        # Displayable names for each token category
        catnames = ['DAT', 'MOV', 'ADD', 'SUB', 'MUL',
                    'DIV', 'MOD', 'JMP', 'JMZ', 'JMN', 'DJN', 'SPL',
                    'CMP', 'SEQ', 'SNE', 'SLT', 'LDP', 'STP', 'NOP',
                    'IMMEDIATE', 'DIRECT', 'INDIRECT', 'INT',
                    'MINUS', 'EOF', 'NEWLINE', 'COMMA', 'NULL']

        smalltokens = {'#': IMMEDIATE, '$': DIRECT,
                       '@': INDIRECT, '': EOF,
                       '\n': NEWLINE, ',': COMMA, '-': MINUS}

        # Dictionary of opcodes
        keywords = {'DAT': DAT, 'MOV': MOV,
                    'ADD': ADD, 'SUB': SUB, 'MUL': MUL,
                    'DIV': DIV, 'MOD': MOD, 'JMP': JMP,
                    'JMZ': JMZ, 'JMN': JMN, 'DJN': DJN,
                    'SPL': SPL, 'CMP': CMP, 'SEQ': SEQ,
                    'SNE': SNE, 'SLT': SLT, 'LDP': LDP,
                    'STP': STP, 'NOP': NOP}

        def __init__(self, category, lexeme, column, line):

            self.category = category  # Category of the token
            self.lexeme = lexeme      # Token in string form
            self.column = column      # Column in which token starts
            self.line = line          # Line on which token appears

        def pretty_print(self):
            """Pretty prints the token"""

            print('Column:', self.column,
                  'Line', self.line,
                  'Category:', self.catnames[self.category],
                  'Lexeme:', self.lexeme)

        def print_lexeme(self):
            print(self.lexeme, end=' ')
