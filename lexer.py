#! /usr/bin/python

"""
This class implements a lexical analyser capable
of consuming BASIC statements and commands and returning
a corresponding list of tokens.
"""

from assemblytoken import AssemblyToken as Token


class Lexer:

    def __init__(self):

        self.__program = ''     # Program being processed
        self.__programindex = 0 # Index into program
        self.__line = 0         # Current line number
        self.__column = 0       # Current column number
        self.__tokenlist = []   # List of tokens created by tokenizer
        self.__prevchar = '\n'  # '\n' in prevchar signals start of new line
        self.__blankline = True # Reset to false if line is not blank

    def tokenize(self, file):
        """
        Returns a list of tokens obtained by
        lexical analysis of the specified
        file.
        """

        # Read the Red Code from a file
        try:
            with open(file, 'r') as infile:
                self.__program = infile.read()
                infile.close()

        except OSError:
            raise OSError("Could not read Red Code file")

        # If file not terminated by a newline, then add one
        if self.__program[-1] != '\n':
            self.__program = self.__program + '\n'

        # Process every character until we
        # reach the end of the program file
        c = ' '  # Prime current character with a space
        while True:

            # Skip any preceding whitespace but not newlines
            while c != '\n' and c.isspace():
                c = self.__get_next_char()

            # Construct a token, with placeholders for category
            # and lexeme
            token = Token(None, '', self.__column, self.__line)

            # Process numbers that may appear in immediate operands
            if c.isdigit():
                token.category = Token.INT

                # Consume all of the digits
                while True:
                    token.lexeme += c  # Append the current char to the lexeme
                    c = self.__get_next_char()

                    # Break if next character is not a digit
                    if not c.isdigit():
                        break

            # Process opcodes
            elif c.isalpha():
                # Consume all of the letters
                while True:
                    token.lexeme += c  # append the current char to the lexeme
                    c = self.__get_next_char()

                    # Break if not a letter
                    if not c.isalpha():
                        break

                # Normalise opcodes to upper case
                token.lexeme = token.lexeme.upper()

                # Determine if the lexeme is a variable name or a
                # reserved word
                if token.lexeme in Token.keywords:
                    token.category = Token.keywords[token.lexeme]

                else:
                    raise SyntaxError('Invalid opcode')

            # Process operand addressing modes and EOF
            elif c in Token.smalltokens:
                token.category = Token.smalltokens[c]
                token.lexeme = c
                c = self.__get_next_char()  # Advance to next character after token

            # We do not recognise this token
            else:
                raise SyntaxError('Syntax error')

            # Append the new token to the list
            self.__tokenlist.append(token)
            token.pretty_print()

            if token.category == Token.EOF:  # Stop lexical analysis at EOF
                break

        return self.__tokenlist

    def __get_next_char(self):
        """
        Returns the next character in the
        file, unless the last character has already
        been processed, in which case, a space is
        returned.
        """

        # Check if starting a new line
        if self.__prevchar == '\n':  # Signals start of a new line
            self.__line += 1                # Adjust line number
            self.__column = 0               # Reset column number
            self.__blankline = True         # Initialise blankline

        if self.__programindex >= len(self.__program):  # At end of file?
            self.__column = 1     # Set EOF column to 1
            self.__prevchar = ''  # Save current char for next call
            return ''             # Null string signals end of file

        next_char = self.__program[self.__programindex] # Get next character from program
        self.__programindex += 1                        # Increment to next character
        self.__column += 1                              # Adjust column number

        if not next_char.isspace(): # Next character is not whitespace
            self.__blankline = False

        # Save the current character
        self.__prevchar = next_char

        # If at end of blank line, return space in place of '\n'
        if next_char == '\n' and self.__blankline:
            return ' '

        else:
            return next_char


if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.tokenize('chang1')
    for token in tokens:
        token.pretty_print()
