import sys
sys.path.insert(0,"../..")

import ply.lex as lex
from ply.lex import TOKEN

# Reserved words
reserved = (
    'BREAK', 'CHAR', 'CONST', 'CONTINUE', 'DO',
    'ELSE', 'FLOAT', 'FOREACH', 'FOR', 'GOTO', 'IN', 'IF', 'INT', 
    'RETURN', 'SIZEOF', 'STATIC', 'STRUCT', 
      'VOID',  'WHILE', 'DEFINE'
    )
    
tokens = reserved + (
    # Literals (identifier, integer constant, float constant, string constant, char const)
    'ID', 'TYPEID', 'ICONST', 'FCONST', 'SCONST', 'CCONST',

    # Operators (+,-,*,/,%, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    #'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    
    # Assignment (<--)
    'EQUALS',

    # Increment/decrement (++,--)
    #'PLUSPLUS', 'MINUSMINUS',

    # Structure FIELD (-->)
    'ARROW',

    
    # Delimeters ( ) [ ] { } , . ; : $[
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON', 'FUNCALL',

	# Preprocessing macros
	'MACRO'
	)

# Completely ignored characters
t_ignore           = ' \t\x0c'

# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MOD              = r'%'
#t_OR               = r'\|'
#t_AND              = r'&'
#t_NOT              = r'~'
#t_XOR              = r'\^'
#t_LSHIFT           = r'<<'
#t_RSHIFT           = r'>>'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operators

t_EQUALS           = r'<-'

# ->
t_ARROW            = r'->'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'
t_FUNCALL		   = r'\$'
#t_ELLIPSIS         = r'\.\.\.'

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"ID")
    return t

# Integer literal
t_ICONST = r'\d+'

# Floating literal
t_FCONST = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'c' or L'c'
t_CCONST = r'\'([^\\\n]|(\\.))*?\''

# Comments (ignored)
def t_comment(t):
    r'(/\*(.|\n)*?\*/)|(//[^\n]*)'
    t.lexer.lineno += t.value.count('\n')

# Preprocessor directive (ignore)
t_MACRO = r'\#(.)*?\n'
@TOKEN(t_MACRO)
def t_macro(t):
	#t.type='MACRO'
	t.lexer.lineno += 1
	#return t;

def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)
    
#lexer = lex.lex(optimize=1)
lexer = lex.lex()
print "Lexer generated"
if __name__ == "__main__":
    lex.runmain(lexer)

    

