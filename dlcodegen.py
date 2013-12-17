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
