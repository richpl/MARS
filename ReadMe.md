# MARS
CoreWars Red Code simulator written in Python, unfinished

Roughly 88 standard, with immediate (#), direct ($) and B-field indirect (@)
addressing modes (although lexical analyser can recognise ICWS '94 standard
addressing modes).

Valid instructions:

JMP #A
JMP $A

MOV #A, #B
MOV $A, #B
MOV #A, $B
MOV #A, @B
MOV $A, $B
MOV $A, @B
