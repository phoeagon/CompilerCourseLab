codegen=1
import sys

global_vars = {};

def get_type( typename ):
	if typename =='int':
		return 'int32'
	elif typename == 'arr':
		return 'ArrayType'

def translate_function_definition \
		(node,context):
	print context
	result=""
	func_name = node.val
	result="procedure "+func_name+"("
	tmp = '@_func_'+func_name
	if tmp not in context:
		print "fuck!!!!!"
	tmp2 = context[ tmp ];
	print tmp2
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
		print tmp2['@params']
		result += tmp2['@params']["@pt_"+str(i)]+":"+get_type(tmp2['@params'][i]);
	#epilog
	result+= ");@nodisplay;"
	print result
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
	print result;
	return result ;


def add_translation_method( node ):
	if ( node.type == 'translation_unit' )
		node.translation = translate_translation_unit;
	elif ( node.type == 'function_definition' )
		node.translation = translate_function_definition;
	elif ( node.type == 'compound_stat' )
		node.translation = translate_compound;
	elif ( node.type == 'unary_ext' )
		node.translation = translate_unary_exp;
	#elif ( node.type == 'function_definition' )
	#	node.translation = translate_function_definition;
	for chd in node.children
		add_translation_method( node.children[chd] )

def get_random_tag(prefix="tag",size=6):
	chars=string.ascii_uppercase + string.digits
	return prefix.join(random.choice(chars) for x in range(size))

def translate_translation_unit( node ):
	pass

def get_lvalue( node ):
	return ""

def get_rvalue( node ):
	return ""

def translate_unary_exp( node ):
	tmp = [ "pop(eax)" ];
	if ( node.value=='-' )
		tmp.push("neg(eax)");
	tmp.push( "push(eax)" );
	return tmp 
	
def translate_function_definition( node ):

	return tmp ;

def translate_const( node ):
	# test if is
	pass

def translate_decl( node ):
	#global

def p_iteration_stat( node ):
	tmp = [] ;
	if ( node.children[0]=='WHILE' ):
		rand_tag = get_random_tag();
		tmp.push( node.children[2].codegen() ); #condition
		tmp.push( "je "+rand_tag );
		tmp.push( node.children[4].codegen() );#to write
		tmp.push( rand_tag+" :" );
		#WHILE  LPAREN  exp  RPAREN  stat
	elif ( node.children[0] == 'DO' ):
		rand_tag = get_random_tag();
		tmp.push( rand_tag+" :" );
		tmp.push( node.children[4].codegen() );#to write
		tmp.push( node.children[2].codegen() ); #condition
		tmp.push( "jne "+rand_tag );
		#DO  stat  WHILE  LPAREN  exp  RPAREN  SEMI
		pass
	elif ( node.children[0] == 'FOR' ):
		#FOR  LPAREN  exp SEMI  exp  SEMI exp  RPAREN  stat
		rand_tag = get_random_tag();
		tmp.push( node.children[2].codegen() );#to do
		tmp.push( node.children[4].codegen() ); #test condition
		tmp.push( "je "+rand_tag );
		tmp.push( node.children[8].codegen() );#compound stat
		tmp.push( node.children[6].codegen() );#to update var
		tmp.push( rand_tag+" :" );
		pass
	elif ( node.children[0] == 'FOREACH' ):
		#FOREACH  LPAREN ident IN  exp  RPAREN  stat
		pass
	return tmp ;

def translate_compound( node ):
	pass
	
def translate_binary_exp( node ):
	#tmp = [ "movl "+node.children[0].rvalue()+", %eax" , \
	#	"movl "+node.children[2].rvalue()+", %ebx" ];
	tmp = [ "pop(eax)" , "popl(ebx)" ]; 
	if  node.value == '+':
		tmp.push("add(ebx, eax)");
	elif node.value == '-':
		tmp.push("sub(ebx, eax)");
	elif node.value == '*':
		tmp.push("imul(ebx, eax)");
	elif node.value == '/':
		tmp.push("push(edx)")
		tmp.push("xor (edx,edx)")
		tmp.push("idiv(ebx)")
		tmp.push("pop(edx)")
	elif node.value == '||':
		tmp.push("or(ebx, eax)");
	elif node.value == '&&':
		tmp.push("and (ebx, eax)");
	elif node.value == '<-':
		tmp.push("mov ( ebx, (type int32)[eax] ) ");
	tmp.push("push (eax)");
	return tmp
