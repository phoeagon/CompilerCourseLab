# -----------------------------------------------------------------------------
# cparse.py
#
# Simple parser for ANSI C.  Based on the grammar in K&R, 2nd Ed.
# -----------------------------------------------------------------------------

import sys
import clex
import ply.yacc as yacc

# Get the token map
tokens = clex.tokens

# translation-unit:




def p_empty(t):
    'empty : '
    pass

def p_error(t):
    print("Whoa. We're hosed")

import profile
# Build the grammar

yacc.yacc(method='LALR')

#profile.run("yacc.yacc(method='LALR')")



