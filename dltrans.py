codegen=1
import sys
from dlparse import Node
import string
import random
from dlcheck2 import is_internal

procedure_code = [];
global_code = [];

global_vars = {};

def get_type( typename ):
	typename = typename.replace("int[","int32[");
	if typename =='int':
		return 'int32'
	elif typename == 'arr':
		return 'ArrayType'
	else:
		return typename;


def translate_postfix_exp(node):
	#print "postfix_exp (len="+str(len(node.children))+"): "+str(node)
	if len(node.children)==1:
		return translate(node.children[0]);
	elif len(node.children)==4 and node.children[0]<>'$':
		# a [ id ]
		tmp = [];
		tmp.extend( translate( node.children[0] ) )
		tmp.extend( translate( node.children[2] ) )
		tmp.extend( [ "pop(ebx);", "pop(eax);" ] )
		tmp.extend( ["add(ebx,eax);", "pushd([eax]);"] )
		return tmp
	elif len(node.children)==3:
		#a->id
		return [];
	elif len(node.children)==6:
		#FUNCALL LBRACKET  ident COLON argument_exp_list RBRACKET
		tmp = ["push(ebx);","push(ecx);","push(edx);","push(esi);","push(edi);"];
		if is_internal(node.children[2].val):
			routine = node.children[2].val[4:]
			routine = routine.replace('_','.');
			tmp.extend( translate_argument_exp_list( node.children[4] ) );
			tmp.append( 'call '+routine +';' );
		else:
			tmp.extend( translate_argument_exp_list( node.children[4] ) );
			tmp.extend(["call("+node.children[2].val+");" ]);
			# I still don't know why this is not needed
			#stack_back=str(4*count_argument_exp_list( node.children[4] ));
			#tmp.append("add("+stack_back+",esp);");
		tmp.extend([ "pop(edi);","pop(esi);","pop(edx);","pop(ecx);","pop(ebx);"]);
		tmp.extend([ "push(eax);" ])
		return tmp
	elif len(node.children)==4 and node.children[0]=='$':
		#FUNCALL LBRACKET  ident  RBRACKET
		return [node.children[2].val+"();","push(eax);"];
	return [];

def translate_argument_exp_list(node):
	if type(node)==str: #fix ";"
		return [];
	elif node.type=='argument_exp_list':
		tmp = [];
		for i in range(len(node.children)-1,0,-1):
			tmp=translate_argument_exp_list(node.children[i])+tmp #reverse order
		return tmp;
	else : #if node.type=='assignment_exp':
		return translate( node )

def count_argument_exp_list(node):
	if type(node)==str: #fix ";"
		return 0;
	elif node.type=='argument_exp_list':
		tmp = 0;
		for i in range(len(node.children)-1,0,-1):
			tmp+=count_argument_exp_list(node.children[i])
		return tmp;
	else : #if node.type=='assignment_exp':
		return 1;

def translate_function_definition (node,context):
	#print context
	result=""
	func_name = node.val
	result="procedure "+func_name;
	tmp = '@_func_'+func_name
	if tmp not in context:
		print "fuck!!!!!"
	tmp2 = context[ tmp ];
	#print "translate_func_def:"+str(tmp2)
	if ( '@params-cnt' not in tmp2 or
		'@params' not in tmp2 ): ##no arg needed
		#epilog
		result+= ";@nodisplay;"
		#print "Procedure: ",result
		return result
	param_cnt = tmp2[ '@params-cnt' ]
	for i in range(param_cnt):
		if i==0:
			result=result+"( Var ";
		else:
			result=result+";";
		#print tmp2['@params']
		result += tmp2['@params']["@pt_"+str(i)]+":"+get_type(tmp2['@params'][i]);
	#epilog
	result+= ");@nodisplay;"
	#print "function_definition: "+result
	return result

def get_var_list( node , context , context_backup ):
	#print "get_var_list"
	result=""
	func_name = node.val
	cnt = 0
	exclude = [];
	if '@params' in context:
		for ele in context['@params']:
			exclude.append( context['@params'][ele] )
	#print "exclude:",exclude
	for ele in context:
		if ( type(context[ele])==str ):
			if ele in exclude:
				continue
			if ( (ele not in context_backup ) or ( context[ele]!=context_backup[ele]) ):
				# now a hit
				if cnt==0 :
					result = "var \n"
				cnt=cnt+1;
				result = result + " "+ele +":" + get_type(context[ele])+";\n";
	#print "get_var_list"+result;
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
	return prefix+"".join(random.choice(chars) for x in range(size))

def translate_translation_unit( node ):
	pass


def translate_unary_exp( node ):
	tmp = [ "pop(eax);" ];
	if ( node.value=='-' ):
		tmp.append("neg(eax);");
	elif node.value=='+':
		pass
	tmp.append( "push(eax);" );
	return tmp 
	

def translate_const( node ):
	#print "translate_const"
	# test if is
	tmp=[];
	if ( node.val_type=='int' ):
		tmp.append("pushd("+node.val+");");
	elif ( node.val_type=='float'):
		tmp.append("pushf("+node.val+");");
	return tmp

def translate_decl( node ):
	return [""]

def translate_selection_stat( node ):
	tmp = [] ;
	#IF  LPAREN  exp  RPAREN  stat
	#IF  LPAREN  exp  RPAREN  stat ELSE  stat
	if len(node.children)==5:
		rand_tag = get_random_tag();
		tmp.extend( translate(node.children[2]) ); #condition
		tmp.extend( ["pop(eax);","test(eax,eax);" ]);
		tmp.append( "je "+rand_tag +";" );
		tmp.extend( translate(node.children[4]) );#to write
		tmp.append( rand_tag+" :" );
	elif len(node.children)==7:
		rand_tag = get_random_tag();
		tmp.extend( translate(node.children[2]) ); #condition
		tmp.extend( ["pop(eax);","test(eax,eax);" ]);
		tmp.append( "je "+rand_tag  +";" );
		tmp.extend( translate(node.children[4]) );#to write
		tmp.append( rand_tag+" :" );
		tmp.extend( translate(node.children[6]) );#to write
	return tmp

def translate_iteration_stat( node ):
	tmp = [] ;
	#print "translate_iteration_stat"
	if ( node.children[0]=='while' ):
		rand_tag = get_random_tag();
		rand_tag2 = get_random_tag();
		tmp.append( rand_tag2+" :" );
		tmp.extend( translate(node.children[2]) ); #condition
		tmp.extend( ["pop(eax);","test(eax,eax);" ]);
		tmp.append( "je "+rand_tag  +";" );
		tmp.extend( translate(node.children[4]) );#to write
		tmp.append( "jmp "+rand_tag2  +";" );
		tmp.append( rand_tag+" :" );
		#WHILE  LPAREN  exp  RPAREN  stat
	elif ( node.children[0] == 'do' ):
		rand_tag = get_random_tag();
		tmp.append( rand_tag+" :" );
		tmp.extend( translate(node.children[1]) ); #body
		tmp.extend( translate(node.children[4]) );#to write
		tmp.extend( ["pop(eax);","test(eax,eax);" ]);
		tmp.append( "jne "+rand_tag  +";" );
		#DO  stat  WHILE  LPAREN  exp  RPAREN  SEMI
		pass
	elif ( node.children[0] == 'for' ):
		#FOR  LPAREN  exp SEMI  exp  SEMI exp  RPAREN  stat
		rand_tag = get_random_tag();
		rand_tag2 = get_random_tag();
		tmp.extend( translate(node.children[2]) );#to do
		tmp.append( "pop(eax);" );#to do
		
		tmp.append( rand_tag2+":");
		tmp.extend( translate(node.children[4]) ); #test condition
		tmp.extend( ["pop(eax);","test(eax,eax);" ]);
		tmp.append( "je "+rand_tag  +";" );
		tmp.extend( translate(node.children[8]) );#compound stat
		tmp.extend( translate(node.children[6]) );#to update var
		tmp.append( "pop(eax);" );#to do
		tmp.append( "jmp "+rand_tag2+";" );
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
	#print "translate_compound:"+str(tmp)
	return tmp


def translate_rvalue_id( node ):
	return ["push ("+node.val+");"];
	
def translate_binary_exp( node ):
	if ( len(node.children)!=3 ):
		if ( isinstance( node ,Node ) ):
			return translate(node.children[0])
	#print "binary_exp" + str(node)
	#tmp = [ "movl "+node.children[0].rvalue()+", %eax" , \
	#	"movl "+node.children[2].rvalue()+", %ebx" ];
	tmp = [  ]; 
	tmp.extend( translate(node.children[0]) )
	tmp.extend( translate(node.children[2]) )
	tmp.extend( [ "pop(ebx);" , "pop(eax);"  ] )
	if  node.val == '+':
		tmp.append("add(ebx, eax);");
	elif node.val == '-':
		tmp.append("sub(ebx, eax);");
	elif node.val == '*':
		tmp.append("imul(ebx, eax);");
	elif node.val == '/':
		tmp.append("extend(edx);")
		tmp.append("xor (edx,edx);")
		tmp.append("idiv(ebx);")
		tmp.append("pop(edx);")
	elif node.val == '||':
		tmp.append("or(ebx, eax);");
	elif node.val == '&&':
		tmp.append("and (ebx, eax);");
	elif node.val == '>':
		tmp.append("if( eax>ebx ) then");
		tmp.append("mov(1,eax);");
		tmp.append("else");
		tmp.append( "xor(eax,eax);" );
		tmp.append("endif;");
	elif node.val == '>=':
		tmp.append("if( eax>=ebx ) then");
		tmp.append("mov(1,eax);");
		tmp.append("else");
		tmp.append( "xor(eax,eax);" );
		tmp.append("endif;");	
	elif node.val == '<':
		tmp.append("if( eax<=ebx ) then");
		tmp.append("mov(1,eax);");
		tmp.append("else");
		tmp.append( "xor(eax,eax);" );
		tmp.append("endif;");
		
	elif node.val == '<=':
		tmp.append("if( eax<=ebx ) then");
		tmp.append("mov(1,eax);");
		tmp.append("else");
		tmp.append( "xor(eax,eax);" );
		tmp.append("endif;");		
	elif node.val == '==':
		tmp.append("if( eax==ebx ) then");
		tmp.append("mov(1,eax);");
		tmp.append("else");
		tmp.append( "xor(eax,eax);" );
		tmp.append("endif;");
		
	tmp.append("push (eax);");
	return tmp

def translate_assignment_exp( node ):
	if ( len(node.children)!=3 ):
		if ( isinstance( node ,Node ) ):
			return translate(node.children[0])
	tmp = []; 
	tmp.extend( translate_leftvalue(node.children[0]) )
	tmp.extend( translate(node.children[2]) )
	tmp.extend( [ "pop(ebx);","pop(eax);" ] )
	tmp.append("mov ( ebx, [eax] ); ");
	tmp.append("pushd([eax]);");
	#print "assignment_exp: ",tmp
	return tmp
	
def translate_leftvalue( node ):
	#print"translate_leftvalue: "+node.type
	if node.type=='id':
		return ["lea( eax,"+node.val+");","push(eax);"]
	elif node.type=='postfix_exp'and len(node.children)==4:
		tmp = [];
		# id [ sub ] 
		tmp.extend( translate_leftvalue( node.children[0] ) )
		tmp.extend( translate( node.children[2] ) )
		tmp.extend( [ "pop(ebx);", "pop(eax);" ] )
		tmp.extend( ["add(ebx,eax);", "push(eax);"] )
		return tmp;
	else:
		for i in range(len(node.children)):
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
		tmp.append("pop(eax);"); #clear last result
		return tmp;
	elif node.type=='mult_exp' or node.type=='additive_exp'\
		or node.type=='relational_exp' or node.type=='logical_exp':
		return translate_binary_exp( node );
	elif  node.type=='assignment_exp':
		return translate_assignment_exp( node );
	elif node.type=='compound_stat':
		return translate_compound( node );
	elif node.type=='iteration_stat':
		return translate_iteration_stat( node );
	elif node.type=='selection_stat':
		return translate_selection_stat( node );
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

def output_procedure_body( code ):
	result = [] ;
	#print code;
	for line in code:
		if len(line)==0:
			continue
		#if line[-1]==';':
		result.append( "\t"+line );
		#elif line[-1]!=':' and line!="else" and line[]!="": #fix label
	#		result.append( "\t"+line+';');
	#	else:
	#		result.append( "\t"+line );
	#print result ;
	return result;

def output_procedure( prototype , var , body , procedure_name ):
	tmp = [];
	tmp.append( prototype ) ;
	tmp.append( var );
	tmp.append( "begin "+procedure_name+";" );
	tmp.extend( output_procedure_body(body) );
	tmp.append( "end "+procedure_name+";" );

	#for i in tmp:
	#	print i

	
	global procedure_code
	procedure_code.extend( tmp );
	return tmp ;

def translate_static( context ):
	tmp = [];
	cnt = 0 ;
	for ele in context:
		if ele[0]=='@' or ele in ('int','float','char'):
			continue;
		if ('@_func_'+ele) in context:
			continue;
		if cnt == 0 :
			tmp.append("static");
		cnt = cnt+1;
		tmp.append( "\t"+ele +":"+ get_type(context[ele]) + ";");

	#for i in tmp:
	#	print i
	global global_code
	global_code.extend( tmp );
	return tmp ;

def translate_everything():
	tag=get_random_tag("prog");
	print "program "+tag+";"
	print "#include( \"stdlib.hhf\" );"
	for line in global_code:
		print line
	for line in procedure_code:
		print line
	print "begin "+tag+";"
	print "\t call(main);"
	print "end "+tag+";"
