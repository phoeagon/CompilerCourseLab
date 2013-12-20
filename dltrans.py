codegen=1
import sys


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
	print "Procedure: ",result
	return result

def get_var_list( node , context , context_backup ):
	result=""
	func_name = node.val
	cnt = 0
	for ( ele in context )
		if ( type(context[ele])=='str' ):
			if ( (ele not in context_backup ) or ( context[ele]!=context_backup[ele]) ):
				# now a hit
				if cnt==0 :
					result = "var \n"
				cnt=cnt+1;
				result = result + "" +":" + "\n";
	
	
