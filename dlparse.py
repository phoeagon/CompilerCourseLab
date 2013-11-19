# -----------------------------------------------------------------------------
# cparse.py
#
# Simple parser for ANSI C.  Based on the grammar in K&R, 2nd Ed.
# -----------------------------------------------------------------------------

import sys
import dllex
import ply.yacc as yacc

noCollapse = False;

class Node:
	def __init__(self,type,val_type,children=None):
		 self.type = type
		 self.val_type = val_type
		 self.val = '';
		 if children:
			  self.children = children
		 else:
			  self.children = [ ]

	def __str__(self):
		 ans = "{\n"+\
				"\t type: '"+str(self.type)+"',\n"+\
				"\t val: '"+str(self.val)+"',\n"+\
				"\t val_type: '"+str(self.val_type)+"',\n"+\
				"\t children: [\n";
		 cnt = 0;
		 for i in self.children:
			 if ( (cnt)>0 ):
				 ans+=','
			 else:
				cnt = 1
			 ans += '\t'+i.__str__() + '\n';
		 ans += "\t]\n}"
		 return ans;

# Get the token map
tokens = dllex.tokens

def collapse(t):
	if ( (len(t)==2) and (not noCollapse) ):
		t[0]=t[1]
		return True
		
# translation-unit:
def p_translation_unit(t):
	'''translation_unit	: external_decl
					| translation_unit external_decl'''
	if ( collapse(t) ):
		return
	t[0]=Node("translation_unit","", t[1:] )
	
def p_external_decl(t):
	'''external_decl : function_definition
				| decl
				'''
	if ( collapse(t) ):
		return
	t[0]=Node("external_decl","", t[1:] )

def p_function_definition(t):
	'function_definition : type_spec  declarator  compound_stat'
	if ( collapse(t) ):
		return
	t[0]=Node("function_definition","", t[1:] )

def p_decl(t):
	'decl	: type_spec declarator SEMI'
	if ( collapse(t) ):
		return
	t[0]=Node("decl","", t[1:] )

def p_decl_list(t):
	'''
	decl_list : decl 
		| decl decl_list
	'''
	if ( collapse(t) ):
		return
	t[0]=Node("decl_list","", t[1:] )

def p_type_spec_1(t):
	'''type_spec	: VOID
				| CHAR
				| INT 
				| FLOAT
	'''
	t[0] = Node( "type_spec" , "" , [ t[1] ] )
	
def p_type_spec_2(t):
	'''type_spec	: struct_spec
	'''
	t[0] = Node( "type_spec" , "" , [ t[1] ] )
	
def p_struct_spec(t):	
	'''struct_spec : STRUCT ident  LBRACE  struct_decl_list  RBRACE
				| STRUCT ident
	'''
	if ( collapse(t) ):
		return
	t[0]=Node("struct_spec","", t[1:] )

def p_struct_decl_list(t):
	'''struct_decl_list : struct_decl 
				| struct_decl_list  struct_decl
	'''
	if ( collapse(t) ):
		return
	t[0]=Node("struct_decl_list","", t[1:] )

def p_struct_decl(t):
	'struct_decl	: type_spec declarator  SEMI'
	if ( collapse(t) ):
		return
	t[0]=Node("struct_decl","", t[1:] )

def p_declarator(t):
	'''declarator	: TIMES  direct_declarator
				| direct_declarator
				'''
	if ( collapse(t) ):
		return
	t[0]=Node("declarator","", t[1:] )

def p_direct_declarator(t):
	'''direct_declarator : ident
				| LPAREN  declarator  RPAREN
				| direct_declarator  LBRACKET  logical_exp  RBRACKET
				| FUNCALL LBRACKET  direct_declarator  COLON  param_list  RBRACKET
				| FUNCALL LBRACKET  direct_declarator  RBRACKET
				'''
	if ( collapse(t) ):
		return
	t[0]=Node("direct_declarator","", t[1:] )

def p_param_list(t):
	'''param_list	: param_decl
				| param_list  COMMA  param_decl'''
	# Cannot collapse: must create frame for param_decl in checker
	t[0]=Node("param_list","", t[1:] )

def p_param_decl(t):
	'param_decl	: type_spec  declarator'
	if ( collapse(t) ):
		return
	t[0]=Node("param_decl","", t[1:] )

def p_stat(t):
	'''stat		: exp_stat
				| compound_stat
				| selection_stat
				| iteration_stat
				| jump_stat'''
	if ( collapse(t) ):
		return
	t[0]=Node("stat","", t[1:] )

def p_exp_stat(t):
	'''exp_stat	: exp SEMI
				| SEMI '''
	t[0]=Node("exp_stat","", t[1:] )

def p_compound_stat(t):
	'''compound_stat	: LBRACE  decl_list  stat_list  RBRACE
				| LBRACE  stat_list  RBRACE
				| LBRACE  decl_list  RBRACE
				| LBRACE  RBRACE'''
	if ( collapse(t) ):
		return
	t[0]=Node("compound_stat","", t[1:] )

def p_stat_list(t):
	'''stat_list	: stat
				| stat_list  stat'''
	if ( collapse(t) ):
		return
	t[0]=Node("stat_list","", t[1:] )

def p_selection_stat(t):
	'''selection_stat	: IF  LPAREN  exp  RPAREN  stat
				| IF  LPAREN  exp  RPAREN  stat ELSE  stat'''
	if ( collapse(t) ):
		return
	t[0]=Node("selection_stat","", t[1:] )

def p_iteration_stat(t):
	'''iteration_stat	: WHILE  LPAREN  exp  RPAREN  stat
				| DO  stat  WHILE  LPAREN  exp  RPAREN  SEMI
				| FOR  LPAREN  exp SEMI  exp  SEMI exp  RPAREN  stat
				| FOREACH  LPAREN ident IN  exp  RPAREN  stat'''
	if ( collapse(t) ):
		return
	t[0]=Node("iteration_stat","", t[1:] )

def p_jump_stat(t):
	'''jump_stat	: CONTINUE  SEMI
				| BREAK  SEMI
				| RETURN  exp  SEMI
				| RETURN	 SEMI'''
	if ( collapse(t) ):
		return
	t[0]=Node("jump_stat","", t[1:] )

def p_exp(t):
	'''exp		:  assignment_exp'''
	if ( collapse(t) ):
		return
	t[0]=Node("exp","", t[1:] )

def p_assignment_exp(t):
	'''assignment_exp	: logical_exp
			| unary_exp EQUALS assignment_exp'''
	# no collapse : to facilitate parameter type check
	t[0]=Node("assignment_exp","", t[1:] )
	
def p_logical_exp(t):
	'''logical_exp	: relational_exp
				| logical_exp LOR relational_exp
				| logical_exp LAND relational_exp'''
	if ( collapse(t) ):
		return
	t[0]=Node("logical_exp","", t[1:] )

def p_relational_exp(t):
	'''relational_exp	: additive_exp
				| relational_exp LT additive_exp
				| relational_exp GT additive_exp
				| relational_exp LE additive_exp
				| relational_exp GE additive_exp
				| relational_exp EQ additive_exp
				| relational_exp NE additive_exp
				'''
	if ( collapse(t) ):
		return
	t[0]=Node("relational_exp","", t[1:] )

def p_additive_exp(t):
	'''additive_exp	: mult_exp
				| additive_exp PLUS mult_exp
				| additive_exp MINUS mult_exp'''
	if ( collapse(t) ):
		return
	t[0]=Node("additive_exp","", t[1:] )
	pass

def p_mult_exp(t):
	'''mult_exp	: cast_exp
				| mult_exp TIMES cast_exp
				| mult_exp DIVIDE cast_exp
				| mult_exp MOD cast_exp'''
	if ( collapse(t) ):
		return
	t[0]=Node("mult_exp","", t[1:] )

def p_cast_exp(t):
	'''cast_exp	: unary_exp
				| LPAREN type_spec RPAREN cast_exp'''
	if ( collapse(t) ):
		return
	t[0]=Node("cast_exp","", t[1:] )

def p_unary_exp(t):
	'''unary_exp	: postfix_exp
				| unary_operator cast_exp'''
	if ( collapse(t) ):
		return
	t[0]=Node("cast_exp","", t[1:] )
	
def p_unary_operator(t):
	'''unary_operator	:  TIMES 
		| PLUS 
		| MINUS 
		| LNOT'''
	if ( collapse(t) ):
		return
	t[0]=Node("unary_operator","", t[1:] )

def p_postfix_exp(t):
	'''postfix_exp	: primary_exp
				| postfix_exp  LBRACKET  exp RBRACKET
				| FUNCALL LBRACKET  ident COLON argument_exp_list RBRACKET
				| FUNCALL LBRACKET  ident  RBRACKET
				| postfix_exp ARROW ident '''
	if ( collapse(t) ):
		return
	t[0]=Node("postfix_exp","", t[1:] )


def p_primary_exp(t):
	'''primary_exp	: ident
				| const 
				| LPAREN  exp  RPAREN'''
	if ( collapse(t) ):
		return
	t[0]=Node("primary_exp","", t[1:] )


def p_argument_exp_list(t):
	'''argument_exp_list : assignment_exp
				| argument_exp_list COMMA assignment_exp'''
	if ( collapse(t) ):
		return
	t[0]=Node("argument_exp_list","", t[1:] )

def p_const_1(t):
	'''const		: ICONST'''
	t[0]=Node("const","int",[ t[1] ])

def p_const_2(t):
	'''const		: CCONST'''
	t[0]=Node("const","char",[ t[1] ])

def p_const_3(t):
	'''const		:  FCONST'''
	t[0]=Node("const","float",[ t[1] ])

def p_const_4(t):
	'''const		:  SCONST'''
	t[0]=Node("const",'float',[ t[1] ])
	
def p_empty(t):
	'empty : '
	if ( collapse(t) ):
		return
	t[0]=Node("empty","",[])

def p_ident(t):
	'''ident	: ID'''
	t[0] = Node("id",'',[ t[1] ]);

def p_error(t):
	if t:
		print("Syntax error at '%s' (Line %d)" % (t.value , t.lineno ) )
	else:
		print("Syntax error at EOF")




# Build the grammar

yacc.yacc(method='SLR')
print "Parser generated"

#from pprint import pprint
#pprint( vars( obj ) )
#profile.run("yacc.yacc(method='LALR')")



