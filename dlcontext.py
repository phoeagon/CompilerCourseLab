import sys
import dllex
import ply.yacc as yacc
import copy 

import pickle


import dlparse 

from dlcheck2 import *

from dltrans import *


if __name__ == "__main__":
	outputFormat = 'json'
	for arg in sys.argv:
		if arg=="--xml":
			outputFormat = 'xml'
		elif arg=="--pobj":
			outputFormat = 'pobj'
    
	from dlang import *
	import dlang
	walk( obj , context )
        print context
