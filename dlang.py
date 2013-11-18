import dllex
import dlparse

import sys
import ply.yacc as yacc
import ply.lex as lex


data = ''
while 1:
	try:
		s = raw_input("")
	except EOFError:
		break
	if not s: 
		continue
	data+=s+'\n';

# print data

obj=yacc.parse( data , tracking=True)

#from pprint import pprint
if __name__ == "__main__":
	print  obj
