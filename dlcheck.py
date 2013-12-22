import sys
import dllex
import ply.yacc as yacc
import copy 
from dlcheck2 import is_internal

import dlparse 

hla_return_type = {'stralloc':'string','stdin_gets':'string'};

current_routine_return_type='void';
Node=dlparse.Node

builtin_type = { 'int':'int' , 'float':'float' , 'char':'char' };

context = copy.copy( builtin_type );

rng= {'char':1 , 'int':2 , 'float':3 }

debug = 1;

def debug_node( node , context ):
	if ( debug ):
		print  node .__str__()
		print  context

def param_to_list( node , ll ):
	if ( not isinstance( node , Node ) ):
		return ;
	if  node.type == 'assignment_exp' :
		ll += [ node.val_type ]
	else:
		for i in node.children:
			param_to_list( i , ll )

def check_param_empty( func_name , context ):
	err_msg = 'Parameter list not fit for function '+func_name ;
	tmp = '@_func_'+func_name
	if tmp not in context:
		print "Fatal: ",err_msg
		exit(0)
	tmp2 = context[ tmp ];
	if  '@params-cnt' not in tmp2 :
		return True;
	params_cnt = tmp2[ '@params-cnt' ];
	if params_cnt > 0 :
		print "Fatal: ",err_msg
		exit(0)
	return True;
	
def check_param_type ( node , func_name , context ):
	#assert node.type == 'argument_exp_list'
	err_msg = 'Parameter list not fit for function '+func_name ;
	ll = [] ;
	#debug_node( node , context ); 
	param_to_list ( node , ll );
	tmp = '@_func_'+func_name
	if tmp not in context:
		print "Fatal: ",err_msg
		exit(0)
	tmp2 = context[ tmp ];
	if ( '@params-cnt' not in tmp2 or
		'@params' not in tmp2 ):
		print "Fatal: ",err_msg
		exit(0)
	param_cnt = tmp2[ '@params-cnt' ]
	if ( param_cnt != len(ll) ):
		print "Fatal: "+"Not of same length!\t"+err_msg;
		exit(0);
	for i in range( len(ll) ):
		if ll[i] != tmp2[ '@params' ][i] :
			if ( ll[i] not in rng  ) or \
				( tmp2['@params'][i] not in rng ):# or\
				#rng[ll[i]] > rng
				print "Fatal: ",  err_msg ;
				exit(0);
	return True;

def general_check( node , context ):
	if ( node.val_type==''):
		node.val_type = 'void'
	#
	#recurse
	if ( node.type=='compound_stat' or node.type=='function_definition'\
		or node.type=='struct_spec' ):
			pass
	else:
		for i in node.children:
			walk( i , context );
	#
		#some node must prevent local variables propogate to parent nodes
		# therefore we make a copy of the original mapping just in case.
		#
		# Most nodes have this:
		if ( len( node.children )== 1 and isinstance( node.children[0],Node ) ):
				node.val_type = node.children[0].val_type ;
		# Can be corrected later

def check_function_definition( node , context ):
	global current_routine_return_type
	if ( node.type=='function_definition' ): #TODO
		#type_spec  declarator  compound_stat
		sub_context = copy.copy( context );
		# typespec
		walk( node.children[0] , sub_context );
		node.val_type = node.children[0].val ;
		# declarator
		walk( node.children[1] , sub_context );
		node.val = node.children[1].val ;
		context[ node.val ] = node.val_type ;
		context[ '@_func_'+node.val ] = sub_context ; # throw out param list
		sub_context[ node.val ] = node.val_type ; #enable recursion
		current_routine_return_type = node.val_type ; #reserve for checks
		sub_context[ '@_func_'+node.val ] = sub_context ; # throw out param list
		# compound
		walk( node.children[2] , sub_context );
		if codegen:
			print "translate_function_definition"
			translate_function_definition( node , context  )
		return True;
	return False;

def check_direct_declarator( node , context ):
	if ( node.type=='direct_declarator' ): #TODO
		length = len(node.children)
		if ( length ==1 ): #Id
			node.val = node.children[0].children[0];
				#tmp_name is not applicable here because ID parser does not know whether
				#   it is in a expression or declarator, and maybe we are
				#   overriding a global name already in context[]
		elif ( node.children[0]=='(' ):
			# LPAREN  declarator  RPAREN
			node.val_type = node.children[1].val_type ;
			node.val = node.children[1].val ;
		elif ( node.children[0]=='$' ):
			node.val_type = node.children[2].val_type ;
			node.val = node.children[2].val ;
		elif ( node.children[1] == '[' ):
			# arr 
			node.val_type = node.children[0].val_type ;
			node.val = node.children[0].val ;
		return True;
	return False;
		
def check_struct_spec( node , context ):
	if ( node.type=='struct_spec' ): #TODO
			# struct id
		walk( node.children[1] , context );
		if ( len(node.children) == 2 ):
			node.val = '@struct_'+node.children[1].val;
		else:
			# STRUCT ident  LBRACE  struct_decl_list  RBRACE
			sub_context = copy.copy( context );
			node.val = '@struct_'+node.children[1].val;
			walk ( node.children[3] , sub_context );
			context[ node.val ] = sub_context ;
		return True ;
	return False;

def check_postfix_expr( node , context ):
	if ( node.type=='postfix_exp' ):
		if ( node.children[1] == '->' ): #TODO!!!!!!!!!!!!!!!
			err_msg = "Cannot find field "+str(node.children[2].val)\
					+" for object "+str(node.children[0].val) ;
			if ( node.children[0].val not in context ):
				print "Fatal: ",err_msg
				exit(0);
			tmp = context[ node.children[0].val ];
			if ( tmp not in context ):
				#print "tmp<-",tmp
				print "Fatal: ",err_msg
				exit(0);
			if ( '@fields' not in context[tmp] or
				node.children[2].val not in context[tmp]['@fields'] ):
				debug_node( node , context )
				print "Fatal: ",err_msg
				exit(0);
			node.val_type = context[tmp]['@fields'][ node.children[2].val ];
			#
		elif ( node.children[0]=='$'): #TODO: Check argument type
			# FUNCALL LBRACKET  ident COLON argument_exp_list RBRACKET
			tmp = node.children[2].val
			if is_internal( tmp ):
				if ( tmp[4:] in hla_return_type ):
					node.val_type = hla_return_type[ tmp[4:] ];
				else:
					node.val_type = 'int'
				return True
			node.val_type = context[ tmp ] ;
			if ( len(node.children) == 6 ):
				#debug_node( node , context );
				check_param_type( node.children[4] , tmp , context );
			else:
				check_param_empty( tmp , context );
			
		elif ( node.children[1]== '[' ): #CHECk TYPE
			node.val_type = node.children[0].val_type;
		return True;
	return False;

def walk( node , context ):
	if ( not isinstance( node , Node ) ):
		return ; # '1', 'a' like literal nodes
	general_check( node , context );
	if ( node.type=='compound_stat' or node.type=='function_definition'\
		or node.type=='struct_spec' ):
		context_backup = copy.copy( context );
	#
	# now check type for itself
	if check_function_definition( node , context  ):
		return
	elif check_struct_spec ( node , context ):
		return 
	elif check_direct_declarator( node , context ):
		return
	elif check_postfix_expr( node , context ):
		return
	elif ( node.type=='const' ):
		# type should already be assigned by parser
		return
	elif ( node.type=='id' ):
		node.val = node.children[0] 
		if node.children[0] in context:
			node.val_type = context[ node.children[0] ]
		#debug_node( node , context );
	#elif ( node.type=='empty' ):	return
	elif ( node.type=='decl' ): #TODO
		node.val_type = 'void';
		context[ node.children[1].val ] = node.children[0].val ;
	#elif ( node.type=='translation_unit' ): return ;
	#elif ( node.type=='external_decl' ): return ;
	elif ( node.type=='decl' ): #TODO
		if ( node.children[1].val_type == 'pointer'):
			context[ node.children[1].val ] = 'pointer'
		else:
			context[ node.children[1].val ] = node.children[1].val_type;
		node.val_type = 'void';
	#elif ( node.type=='decl_list' ): 
	elif ( node.type=='type_spec' ): #TODO
		if ( isinstance( node.children[0] , Node ) ):
			node.val = node.children[0].val ;
		else:
			node.val = node.children[0];
		return ;
		#
	elif ( node.type=='struct_decl' ): #TODO
		node.val_type = 'void';
		if node.children[1].val_type == 'pointer':
			node.children[0].val = 'pointer'
		context[ node.children[1].val ] = node.children[0].val ;
		if ( '@fields' not in context ):
			context[ '@fields' ] = {};
		context[ '@fields' ][ node.children[1].val  ] = node.children[0].val ;
	#elif ( node.type=='declarator_list' ): 
	elif ( node.type=='declarator' ):
		if ( node.children[0]=='*' ):
			node.val_type = 'pointer';
			node.val = node.children[1].val;
		else: # pass on
			node.val_type = node.children[0].val_type ;
			node.val = node.children[0].val;
	#elif ( node.type=='param_list' ): #TODO
	elif ( node.type=='param_decl' ): #TODO
		node.val_type = 'void';
		if ( ('@params' not in context) or ('@params-cnt' not in context)):			
			context[ '@params' ] = {};
			context[ '@params-cnt' ] = 0;
		context[ node.children[1].val ] = node.children[0].val ;
		context[ '@params' ] [ context[ '@params-cnt' ] ] = node.children[0].val;
		context[ '@params' ] [ "@pt_"+str(context[ '@params-cnt' ]) ] = node.children[1].val;
		context[ '@params-cnt' ] += 1
		#debug_node( node , context )
		#TODO!!!!!!!!!!!!! 
	elif ( node.type=='stat' ):
		node.val_type = 'void';
		return ;
	elif ( node.type=='exp_stat' ):
		if ( not isinstance( node.children[0],Node ) ):
			node.val_type = 'void';
	elif ( node.type=='iteration_stat' or \
		node.type=='selection_stat' ):
			if  node.children[0]=='while' :
				if  node.children[2].val_type == 'void' :
					print "Fatal: ","Invalid condition"
					exit(0);
			elif node.children[0] == 'do' :
				if  node.children[4].val_type == 'void' :
					print "Fatal: ","Invalid condition"
					exit(0);
	elif (  node.type=='jump_stat' or\
			 node.type=='stat_list' or\
			node.type=='compound_stat' ):
		if node.type=='jump_stat':
			if node.children[0] == 'return':
				if len(node.children)>2 and current_routine_return_type=='void':
					print "Fatal: Cannot return with value for current function (because has no ret value)"
					exit(0);
				elif len(node.children)>2 and node.children[1].val_type != current_routine_return_type :
					print "Fatal: Cannot return with value for current function (of return type "\
						+current_routine_return_type+")"
					exit(0);
					
		if ( node.type == 'compound_stat' ):
			for i in node.children:
				walk( i , context );
		node.val_type = 'void';
		if ( node.type == 'compound_stat' ):
			context = context_backup; # prevent identifier context propogate
	#elif ( node.type=='p_exp'): #DUMMY STUB
	elif ( node.type=='assignment_exp'):
		if ( len ( node.children ) > 1 ):
			if ( node.children[0].val_type == "string" and \
				node.children[2].val_type == "int" ) or \
				( node.children[2].val_type == "string" and \
				node.children[0].val_type == "int" ):
					print "Fatal: Incompatible type between string and int!"
					exit(0);
			# a <- exp
			node.val_type = node.children[0].val_type ;
	elif ( node.type=='relational_exp' or node.type=='logical_exp'):
		if ( len ( node.children ) > 1 ):
			type1 = node.children[0].val_type ;
			type2 = node.children[2].val_type ;
			pool = ( type1 , type2 )
			legal = ('int','char','float')
			for i in pool:
				if ( i not in legal ):
					#debug_node( node , context )
					print "Fatal:" + ('Operator '+node.children[1]+ \
						' not applicable to type '+i)
					exit(0);
			node.val_type = 'int' #default to int
		else:
			node.val_type = node.children[0].val_type ;			
	elif ( node.type=='mult_exp' or node.type=='additive_exp' ): 
		if ( len ( node.children ) > 1 ):
			# mult_exp TIMES cast_exp (ONLY APPLICABLE TO INT/FLOAT)
			type1 = node.children[0].val_type ;
			type2 = node.children[2].val_type ;
			pool = ( type1 , type2 )
			legal = ('int','char','float')
			for i in pool:
				if ( i not in legal ):
					#debug_node( node , context )
					print "Fatal: ",('Operator '+node.children[1]+ \
									' not applicable to type '+i)
					exit(0)
			if ( 'float' in pool ):			
				node.val_type = 'float'
			elif ( 'int' in pool ):
				node.val_type = 'int'
			else:
				node.val_type = 'char'
	elif ( node.type=='cast_exp' ): 
		if ( len ( node.children ) > 1 ):
			#LPAREN type_spec RPAREN cast_exp
			node.val_type = node.children[1].val ;
	elif ( node.type=='unary_exp' ): 
		if ( len ( node.children ) > 1 ):
			#unary_operator cast_exp
			node.val_type = node.children[1].val_type ;
	elif ( node.type=='unary_operator' ):
		if ( node.children[0] == '*' ):
			assert False;#force abort dereferencing pointer
	elif ( node.type=='primary_exp' ):
		if ( len( node.children ) > 1 ):
			node.val_type = node.children[1].val_type ;

codegen=0



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

	from dltrans import forbid_global_struct;
	forbid_global_struct( context );
	
	#debug_node( obj , context )
	if outputFormat=="xml":
		import gnosis.xml.pickle
		print "\n"
		print gnosis.xml.pickle.dumps(obj)
	elif outputFormat == 'json':
		import jsonpickle
		print "\n"
		print jsonpickle.encode(obj, unpicklable=False)
	elif outputFormat == 'pobj':
		print "\n"
		print obj
