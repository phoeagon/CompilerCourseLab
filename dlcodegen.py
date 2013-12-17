import string
import random

def get_random_tag(prefix="tag",size=6):
	chars=string.ascii_uppercase + string.digits
	return prefix.join(random.choice(chars) for x in range(size))

def get_lvalue( node ):
	return ""

def get_rvalue( node ):
	return ""

def translate_unary_exp( node ):
	tmp = [ "pop %eax" ];
	if ( node.value=='-' )
		tmp.push("neg %eax");
	tmp.push( "push %eax" );
	return tmp 
	
def translate_function_definition( node ):
	tmp = [ "push %ebp" , "mov %esp, %ebp"];

	return tmp ;

def translate_const( node ):
	# test if is
	pass

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

def translate_binary_exp( node ):
	#tmp = [ "movl "+node.children[0].rvalue()+", %eax" , \
	#	"movl "+node.children[2].rvalue()+", %ebx" ];
	tmp = [ "pop %eax" , "popl %ebx" ]; 
	if  node.value == '+':
		tmp.push("add %ebx, %eax");
	elif node.value == '-':
		tmp.push("sub %ebx, %eax");
	elif node.value == '*':
		tmp.push("imul %ebx, %eax");
	elif node.value == '/':
		tmp.push("push %edx")
		tmp.push("xor %edx,%edx")
		tmp.push("idiv %ebx")
		tmp.push("pop %edx")
	elif node.value == '||':
		tmp.push("or %ebx, %eax");
	elif node.value == '&&':
		tmp.push("and %ebx, %eax");
	tmp.push("push %eax");
	return tmp

def translate( node ):
	if node.type == "mult_exp":
		return translate_binary_exp( node );
	elif node.type == "additive_exp":
		return translate_binary_exp( node );
	return ""
