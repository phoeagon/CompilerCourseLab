import sys
import dllex
import ply.yacc as yacc
import copy 

import dlparse 

Node=dlparse.Node

builtin_type = { 'int':'int' , 'float':'float' , 'char':'char' };

context = copy.copy( builtin_type );
    
def walk( node , context ):
    if ( not isinstance( node , Node ) ):
        return ; # '1', 'a' like literal nodes
    node.val_type = 'void'
    #
    if ( node.type=='compound_stat' or node.type=='function_definition'\
        or node.type=='struct_spec' ):
        context_backup = copy.copy( context );
        #some node must prevent local variables propogate to parent nodes
        # therefore we make a copy of the original mapping just in case.
    else:
        #
        #recurse
        for i in node.children:
            walk( i , context );
        #
        # Most nodes have this:
        if ( len( node.children )== 1 and isinstance( node.children[0],Node ) ):
                node.val_type = node.children[0].val_type ;
        # Can be corrected below
    #
    # now check type for itself
    if ( node.type=='const' ):
        # type should already be assigned by parser
        return
    elif ( node.type=='id' ):
        node.val = node.children[0] 
        if node.children[0] in context:
            node.val_type = context[ node.children[0] ]
    #elif ( node.type=='empty' ):    return
    elif ( node.type=='declarator'): 
        if ( node.children[0]=='*' ):
            node.val_type = 'pointer' ;
        else:
            node.val_type = node.children[0].val_type ; #pass from below
    elif ( node.type=='decl' ): #TODO
        node.val_type = 'void';
        context[ node.children[1].val ] = node.children[0].val ;
    #elif ( node.type=='translation_unit' ): return ;
    #elif ( node.type=='external_decl' ): return ;
    elif ( node.type=='function_definition' ): #TODO
        sub_context = copy.copy( context );
        # typespec
        walk( node.children[0] , sub_context );
        node.val_type = node.children[0].val ;
        # declarator
        walk( node.children[1] , sub_context );
        node.val = node.children[1].val ;
        context[ node.val ] = node.val_type ;
        # compound
        walk( node.children[2] , sub_context );
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
    elif ( node.type=='struct_spec' ): #TODO
            # struct id
        walk( node.children[1] , context );
        if ( len(node.children) == 2 ):
            node.val = '@struct_'+node.children[1].val;
        else:
            # struct id{ int field }
            node.val = '@struct_'+node.children[1].val;
            walk ( node.children[3] , context );
            context_backup[ node.val ] = context ;            
            context = context_backup ; # prevent propogation
        #
    elif ( node.type=='struct_decl' ): #TODO
        node.val_type = 'void';
        context[ node.children[1].val ] = node.children[0].val ;
    #elif ( node.type=='declarator_list' ): 
    elif ( node.type=='declarator' ):
        if ( node.children[0]=='*' ):
            node.val_type = 'pointer';
            node.val = node.children[1].val;
        else: # pass on
            node.val_type = node.children[0].val_type ;
            node.val = node.children[0].val;
    elif ( node.type=='direct_declarator' ): #TODO
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
        elif ( node.children[0].type == 'direct_declarator' ):
            # arr 
            node.val_type = node.children[0].val_type ;
            node.val = node.children[0].val ;
        return ;
    elif ( node.type=='param_list' ): #TODO
        context[ '!params' ] = {};
        context[ '!params-cnt' ] = 0;
        return ;
    elif ( node.type=='param_decl' ): #TODO
        node.val_type = 'void';
        if ( '!params' not in context or '!params-cnt' not in context):            
            context[ '!params' ] = {};
            context[ '!params-cnt' ] = 0;
        context[ node.children[1].val ] = node.children[0].val ;
        context[ '!params' ] [ context[ '!params-cnt' ] ] = node.children[0].val;
        context[ '!params-cnt' ] += 1
        #TODO!!!!!!!!!!!!! 
    elif ( node.type=='stat' ):
        node.val_type = 'void';
        return ;
    elif ( node.type=='exp_stat' ):
        if ( not isinstance( node.children[0],Node ) ):
            node.val_type = 'void';
    elif ( node.type=='iteration_stat' or node.type=='jump_stat' or\
            node.type=='selection_stat' or node.type=='stat_list' or\
            node.type=='compound_stat' ):
        if ( node.type == 'compound_stat' ):
            for i in node.children:
                walk( i , context );
        node.val_type = 'void';
        if ( node.type == 'compound_stat' ):
            context = context_backup; # prevent identifier context propogate
    #elif ( node.type=='p_exp'): #DUMMY STUB
    elif ( node.type=='assignment_exp'):
        if ( len ( node.children ) > 1 ):
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
                    raise Exception('Operator '+node.children[1]+ \
                        ' not applicable to type '+i)
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
                    raise NameException('Operator '+node.children[1]+ \
                        ' not applicable to type'+i)
            if ( 'float' in pool ):            
                node.val_type = 'float'
            elif ( 'int' in pool ):
                node.val_type = 'int'
            else:
                node.val_type = 'char'
    elif ( node.type=='cast_exp' ): 
        if ( len ( node.children ) > 1 ):
            #LPAREN type_spec RPAREN cast_exp
            node.val_type = node.children[3].val_type ;
    elif ( node.type=='unary_exp' ): 
        if ( len ( node.children ) > 1 ):
            #unary_operator cast_exp
            node.val_type = node.children[1].val_type ;
    elif ( node.type=='unary_operator' ):
        if ( node.children[0] == '*' ):
            assert False;#force abort dereferencing pointer
    elif ( node.type=='postfix_exp' ):
        if ( node.children[1] == '->' ): #TODO!!!!!!!!!!!!!!!
            return ;
        elif ( node.children[0]=='$'): #TODO: Check argument type
            tmp = node.children[2].val
            node.val_type = context[ tmp ] ;
        elif ( node.children[1]== '[' ): #CHECk TYPE
            node.val_type = node.children[0].val_type;
    elif ( node.type=='primary_exp' ):
        if ( length( node.children ) > 1 ):
            node.val_type = node.children[1].val_type ;
    #elif ( node.type=='argument_exp_list' )
    #elif ( node.type=='argument_exp_list' )
    #elif ( node.type=='argument_exp_list' )
    #elif ( node.type=='argument_exp_list' )
    #elif ( node.type=='argument_exp_list' )
    #elif ( node.type=='argument_exp_list' )
    #elif ( node.type=='argument_exp_list' )
    
if __name__ == "__main__":
    from dlang import *
    import dlang
    walk( obj , context )
    print  vars(obj) 
    print vars(context)
