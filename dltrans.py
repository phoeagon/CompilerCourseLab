codegen=1
import sys
from dlparse import Node
import string
import random

global_vars = {};

def get_type( typename ):
	if typename =='int':
		return 'int32'
	elif typename == 'arr':
		return 'ArrayType'


def translate_postfix_exp(node):
	if len(node.children)==1:
		return translate(node.children[0]);
	elif len(node.children)==4:
		# a [ id ]
		tmp = [];
		tmp.extend( translate( node.children[0] ) )
		tmp.extend( translate( node.children[2] ) )
		tmp.extend( [ "pop(ebx)", "pop(eax)" ] )
		tmp.extend( ["add(ebx,eax)", "pushd([eax])"] )
		return tmp
	elif len(node.children)==3:
		#a->id
		pass
	elif len(node.children)==5:
		#FUNCALL LBRACKET  ident COLON argument_exp_list RBRACKET
		pass
	elif len(node.children)==4:
		#FUNCALL LBRACKET  ident  RBRACKET
		pass
	return [];

def translate_function_definition (node,context):
	#print context
	result=""
	func_name = node.val
	result="procedure "+func_name+"("
	tmp = '@_func_'+func_name
	if tmp not in context:
		print "fuck!!!!!"
	tmp2 = context[ tmp ];
	print "translate_func_def:"+str(tmp2)
	if ( '@params-cnt' not in tmp2 or
		'@params' not in tmp2 ): ##no arg needed
		#epilog
		result+= ");@nodisplay;"
		print "Procedure: ",result
		return result
	param_cnt = tmp2[ '@params-cnt' ]
	for i in range(param_cnt):
		if i==0:
			result=result+" Var ";
		else:
			result=result+";";
		#print tmp2['@params']
		result += tmp2['@params']["@pt_"+str(i)]+":"+get_type(tmp2['@params'][i]);
	#epilog
	result+= ");@nodisplay;"
	print "function_definition: "+result
	return result

def get_var_list( node , context , context_backup ):
	#print "get_var_list"
	result=""
	func_name = node.val
	cnt = 0
	for ele in context:
		if ( type(context[ele])==str ):
			if ( (ele not in context_backup ) or ( context[ele]!=context_backup[ele]) ):
				# now a hit
				if cnt==0 :
					result = "var \n"
				cnt=cnt+1;
				result = result + " "+ele +":" + get_type(context[ele])+";\n";
	print "get_var_list"+result;
	return result ;


def add_translation_method( node ):
	if ( node.type == 'translation_unit' ):
		node.translation = translate_translation_unit;
	elif ( node.type == 'function_definition' ):
		node.translation = translate_function_definition;
	elif ( node.type == 'compound_stat' ):
		node.translation = translate_compound;
	elif ( node.type == 'unary_ext' ):
		node.translation = translate_unary_exp;
	#elif ( node.type == 'function_definition' )
	#	node.translation = translate_function_definition;
	for chd in node.children:
		add_translation_method( node.children[chd] )

def get_random_tag(prefix="tag",size=6):
	chars=string.ascii_uppercase + string.digits
	return prefix.join(random.choice(chars) for x in range(size))

def translate_translation_unit( node ):
	pass


def translate_unary_exp( node ):
	tmp = [ "pop(eax)" ];
	if ( node.value=='-' ):
		tmp.append("neg(eax)");
	elif node.value=='+':
		pass
	tmp.append( "push(eax)" );
	return tmp 
	

def translate_const( node ):
	print "translate_const"
	# test if is
	tmp=[];
	if ( node.val_type=='int' ):
		tmp.append("pushd("+node.val+")");
	elif ( node.val_type=='float'):
		tmp.append("pushf("+node.val+")");
	return tmp

def translate_decl( node ):
	return [""]

def translate_iteration_stat( node ):
	tmp = [] ;
	print "translate_iteration_stat"
	if ( node.children[0]=='while' ):
		rand_tag = get_random_tag();
		tmp.extend( translate(node.children[2]) ); #condition
		tmp.append( "je "+rand_tag );
		tmp.extend( translate(node.children[4]) );#to write
		tmp.append( rand_tag+" :" );
		#WHILE  LPAREN  exp  RPAREN  stat
	elif ( node.children[0] == 'do' ):
		rand_tag = get_random_tag();
		tmp.append( rand_tag+" :" );
		tmp.extend( translate(node.children[4]) );#to write
		tmp.extend( translate(node.children[2]) ); #condition
		tmp.append( "jne "+rand_tag );
		#DO  stat  WHILE  LPAREN  exp  RPAREN  SEMI
		pass
	elif ( node.children[0] == 'for' ):
		#FOR  LPAREN  exp SEMI  exp  SEMI exp  RPAREN  stat
		rand_tag = get_random_tag();
		tmp.extend( translate(node.children[2]) );#to do
		tmp.extend( translate(node.children[4]) ); #test condition
		tmp.append( "je "+rand_tag );
		tmp.append( translate(node.children[8]) );#compound stat
		tmp.append( translate(node.children[6]) );#to update var
		tmp.append( rand_tag+" :" );
		pass
	elif ( node.children[0] == 'foreach' ):
		#FOREACH  LPAREN ident IN  exp  RPAREN  stat
		pass
	return tmp ;

def translate_compound( node ):
	tmp = [];
	for i in range(len(node.children)):
		tmp.extend( translate( node.children[i] ) )
	print "translate_compound:"+str(tmp)
	return tmp


def translate_rvalue_id( node ):
	return ["push ("+node.val+")"];
	
def translate_binary_exp( node ):
	if ( len(node.children)!=3 ):
		if ( isinstance( node ,Node ) ):
			return translate(node.children[0])
	#tmp = [ "movl "+node.children[0].rvalue()+", %eax" , \
	#	"movl "+node.children[2].rvalue()+", %ebx" ];
	tmp = [  ]; 
	tmp.extend( translate(node.children[0]) )
	tmp.extend( translate(node.children[2]) )
	tmp.extend( [ "pop(ebx)" , "pop(eax)"  ] )
	if  node.val == '+':
		tmp.append("add(ebx, eax)");
	elif node.val == '-':
		tmp.append("sub(ebx, eax)");
	elif node.val == '*':
		tmp.append("imul(ebx, eax)");
	elif node.val == '/':
		tmp.append("extend(edx)")
		tmp.append("xor (edx,edx)")
		tmp.append("idiv(ebx)")
		tmp.append("pop(edx)")
	elif node.val == '||':
		tmp.append("or(ebx, eax)");
	elif node.val == '&&':
		tmp.append("and (ebx, eax)");
	tmp.append("push (eax)");
	return tmp

def translate_assignment_exp( node ):
	if ( len(node.children)!=3 ):
		if ( isinstance( node ,Node ) ):
			return translate(node.children[0])
	tmp = []; 
	tmp.extend( translate_leftvalue(node.children[0]) )
	tmp.extend( translate(node.children[2]) )
	tmp.extend( [ "pop(ebx)","pop(eax)" ] )
	tmp.append("mov ( ebx, [eax] ) ");
	tmp.append("push (eax)");
	print "assignment_exp: ",tmp
	return tmp
	
def translate_leftvalue( node ):
	#print"translate_leftvalue: "+node.type
	if node.type=='id':
		return ["lea( eax,"+node.val+")","push(eax)"]
	elif node.type=='postfix_exp'and len(node.children)==4:
		tmp = [];
		# id [ sub ] 
		tmp.extend( translate_leftvalue( node.children[0] ) )
		tmp.extend( translate( node.children[2] ) )
		tmp.extend( [ "pop(ebx)", "pop(eax)" ] )
		tmp.extend( ["add(ebx,eax)", "push(eax)"] )
		return tmp;
	else:
		for i in len(node.children):
			if isinstance(node.children[i],Node):
				return translate_leftvalue(node.children[i])
		# here is 

def translate( node ):
	#print node
	if ( not isinstance(node,Node) ):
		return [];
	if  node.type=='translation_unit' :
		return translate_translation_unit( node );
	elif node.type=='postfix_exp':
		return translate_postfix_exp(node);
	elif node.type =="exp_stat":
		tmp=translate(node.children[0]);
		tmp.append("pop(eax)"); #clear last result
		return tmp;
	elif node.type=='mult_exp' or node.type=='additive_exp':
		return translate_binary_exp( node );
	elif  node.type=='assignment_exp':
		return translate_assignment_exp( node );
	elif node.type=='compound_stat':
		return translate_compound( node );
	elif node.type=='iteration_stat':
		return translate_iteration_stat( node );
	elif node.type == 'id':
		return translate_rvalue_id(node)
	elif node.type == 'const':
		return translate_const(node)
	elif node.type == 'decl':
		return [""]
	#return []
	#elif node.type=='stat':
	else:
		result = []
		if isinstance( node , Node ):
			for i in range(len(node.children)) :
				result.extend( translate( node.children[i] ) )
		return result
