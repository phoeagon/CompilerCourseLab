import dllex
import dlparse

import sys
import ply.yacc as yacc
import ply.lex as lex


data = ''
while 1:
	try:
		s = raw_input('dl> ')
	except EOFError:
		break
	if not s: 
		continue
	data+=s+'\n';

# print data

obj=yacc.parse( data )

#from pprint import pprint
print  obj