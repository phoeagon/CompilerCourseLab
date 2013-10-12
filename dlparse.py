# -----------------------------------------------------------------------------
# cparse.py
#
# Simple parser for ANSI C.  Based on the grammar in K&R, 2nd Ed.
# -----------------------------------------------------------------------------

import sys
import dllex
import ply.yacc as yacc

# Get the token map
tokens = dllex.tokens

# translation-unit:

def p_translation_unit(t):
	'''translation_unit	: external_decl
			| translation_unit external_decl
			'''
	pass
	
def p_external_decl(t):
	'''external_decl : function_definition
				| decl
				'''
	pass

def p_function_definition(t):
	'function_definition : type_spec  declarator  compound_stat'
	pass

def p_decl(t):
	'decl	: type_spec declarator SEMI'
	pass

def p_decl_list(t):
	'''
	decl_list : decl 
		| decl decl_list
	'''
	pass

def p_type_spec(t):
	'''type_spec	: VOID
				| CHAR
				| INT 
				| FLOAT
				| struct_spec
	'''		
	pass

def p_struct_spec(t):	
	'''struct_spec : STRUCT ID  LBRACE  struct_decl_list  RBRACE
				| STRUCT  LBRACE  struct_decl_list  RBRACE
				| STRUCT ID
	'''
	pass

def p_struct_decl_list(t):
	'''struct_decl_list : struct_decl 
				| struct_decl_list  struct_decl
	'''
	pass

def p_struct_dec(t):
	'struct_decl	: declarator_list  SEMI'
	pass

def p_declarator_list(t):
	'''declarator_list	: declarator
				| declarator_list  COMMA  declarator
				'''
	pass

def p_declarator(t):
	'''declarator	: TIMES  direct_declarator
				| direct_declarator
				'''
	pass

def p_direct_declarator(t):
	'''direct_declarator : ID
				| LPAREN  declarator  RPAREN
				| direct_declarator  LBRACKET  logical_exp  RBRACKET
				| FUNCALL LBRACKET  direct_declarator  COLON  param_list  RBRACKET
				| FUNCALL LBRACKET  direct_declarator  RBRACKET
				'''
	pass

def p_param_list(t):
	'''param_list	: param_decl
				| param_list  COMMA  param_decl'''
	pass

def p_param_decl(t):
	'param_decl	: type_spec  declarator'
	pass

def p_stat(t):
	'''stat		: exp_stat
				| compound_stat
				| selection_stat
				| iteration_stat
				| jump_stat'''
	pass

def p_exp_stat(t):
	'''exp_stat	: exp SEMI
				| SEMI '''
	pass

def p_compound_stat(t):
	'''compound_stat	: LBRACE  decl_list  stat_list  RBRACE
				| LBRACE  stat_list  RBRACE
				| LBRACE  decl_list  RBRACE
				| LBRACE  RBRACE'''
	pass

def p_stat_list(t):
	'''stat_list	: stat
				| stat_list  stat'''
	pass

def p_selection_stat(t):
	'''selection_stat	: IF  LPAREN  exp  RPAREN  stat
				| IF  LPAREN  exp  RPAREN  stat ELSE  stat'''
	pass

def p_iteration_stat(t):
	'''iteration_stat	: WHILE  LPAREN  exp  RPAREN  stat
				| DO  stat  WHILE  LPAREN  exp  RPAREN  SEMI
				| FOR  LPAREN  exp SEMI  exp  SEMI exp  RPAREN  stat
				| FOREACH  LPAREN ID IN  stat  RPAREN  stat'''
	pass

def p_jump_stat(t):
	'''jump_stat	: CONTINUE  SEMI
				| BREAK  SEMI
				| RETURN  exp  SEMI
				| RETURN	 SEMI'''
	pass

def p_exp(t):
	'''exp		: logical_exp
				| unary_exp  EQUALS assignment_exp'''
	pass

def p_assignment_exp(t):
	'''assignment_exp	: logical_exp
			| unary_exp EQUALS assignment_exp'''
	pass
	
def p_logical_exp(t):
	'''logical_exp	: relational_exp
				| logical_exp LOR relational_exp
				| logical_exp LAND relational_exp'''
	pass

def p_relational_exp(t):
	'''relational_exp	: additive_exp
				| relational_exp LT additive_exp
				| relational_exp GT additive_exp
				| relational_exp LE additive_exp
				| relational_exp GE additive_exp
				| relational_exp EQ additive_exp
				| relational_exp NE additive_exp
				'''
	pass

def p_additive_exp(t):
	'''additive_exp	: mult_exp
				| additive_exp PLUS mult_exp
				| additive_exp MINUS mult_exp'''
	pass

def p_mult_exp(t):
	'''mult_exp	: cast_exp
				| mult_exp TIMES cast_exp
				| mult_exp DIVIDE cast_exp
				| mult_exp MOD cast_exp'''
	pass

def p_cast_exp(t):
	'''cast_exp	: unary_exp
				| LPAREN type_spec RPAREN cast_exp'''
	pass

def p_unary_exp(t):
	'''unary_exp	: postfix_exp
				| unary_operator cast_exp'''
	pass
	
def p_unary_operator(t):
	'''unary_operator	:  TIMES 
		| PLUS 
		| MINUS 
		| LNOT'''
	pass

def p_postfix_exp(t):
	'''postfix_exp	: primary_exp
				| postfix_exp  LBRACKET  exp RBRACKET
				| FUNCALL LBRACKET  postfix_exp COLON argument_exp_list RBRACKET
				| FUNCALL LBRACKET  postfix_exp  RBRACKET
				| postfix_exp ARROW ID '''
	pass

def p_primary_exp(t):
	'''primary_exp	: ID
				| const 
				| SCONST
				| LPAREN  exp  RPAREN'''
	pass

def p_argument_exp_list(t):
	'''argument_exp_list : assignment_exp
				| argument_exp_list COMMA assignment_exp'''
	pass

def p_const(t):
	'''const		: ICONST
				| CCONST
				| FCONST'''
	pass


def p_empty(t):
    'empty : '
    pass


def p_error(t):
    print("Whoa. We're hosed")

import profile
# Build the grammar

yacc.yacc(method='SLR')

#profile.run("yacc.yacc(method='LALR')")



