import sys
import dllex
import ply.yacc as yacc

import dlparse.Node as Node

symbol = {};

def walk( node , context ):
    if ( not isinstance( node , Node ) ):
        return ; # '1', 'a' like literal nodes
    #    
    if ( node.type=='compound_stat' ):
        context_backup = copy( context );
        #some node must prevent local variables propogate to parent nodes
        # therefore we make a copy of the original mapping just in case.
    #
    #recurse
    for i in node.children:
        walk( i , context );
    #
    # Most nodes have this:
    if ( len( children )== 1 and isinstance( node.children[0],Node ) ):
            node.val_type = node.children[0].val_type ;
    # Can be corrected below
    # now check type for itself
    if ( node.type=='const' ):
        # type should already be assigned by parser
        return
    elif ( node.type=='id' ):
        if node.children[0] not in context:
            raise NameException('Undefined identifier '+node.children[0])
        else:
            node.val_type = context[ node.children[0] ]
        return
    elif ( node.type=='empty' ):
        return
    elif ( node.type=='declarator'): #TODO
        if ( node.children[0]=='*' ):
            node.val_type = 'pointer' ;
            #assert  (node.children[1] not in context ) or \
            #        ( context[ node.children[1] ] == node.val_typ )
            # DISABLE THIS TO ALLOW LOCAL VARIABLE OVERRIDE
            context[ node.children[1] ] = node.val_type ;
    elif ( node.type=='decl' ): #TODO
        return ;
    #elif ( node.type=='translation_unit' ): 
    elif ( node.type=='function_definition' ): #TODO
        return ;
    elif ( node.type=='external_decl' ): #TODO
        return ;
    elif ( node.type=='function_definition' ): #TODO
        return ;
    elif ( node.type=='decl' ): #TODO
        return ;
    #elif ( node.type=='decl_list' ): 
    elif ( node.type=='type_spec' ): #TODO
        return ;
    elif ( node.type=='struct_spec' ): #TODO
        return ;
    #elif ( node.type=='struct_decl_list' ): 
    elif ( node.type=='struct_decl' ): #TODO
        return ;
    #elif ( node.type=='declarator_list' ): 
    elif ( node.type=='declarator' ): #TODO
        return ;
    elif ( node.type=='direct_declarator' ): #TODO
        return ;
    elif ( node.type=='param_list' ): #TODO
        return ;
    elif ( node.type=='param_decl' ): #TODO
        return ;
    elif ( node.type=='stat' ):
        node.val_type = 'void';
        return ;
    elif ( node.type=='exp_stat' ):
        if ( !isinstance( node.children[0],Node ) )
            node.val_type = 'void';
    elif ( node.type=='iteration_stat' or node.type=='jump_stat' \
            node.type=='selection_stat' or node.type=='stat_list' \
            node.type='compound_stat' ):
        node.val_type = 'void';
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
                    raise NameException('Operator '+node.children[1]+ \
                        ' not applicable to type'+i)
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
        return # TODO
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
    

