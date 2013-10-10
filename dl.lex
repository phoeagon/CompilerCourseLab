%{
	#include "dlang.hpp"
	#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
	#define TOKEN(t) (yylval.token = t)
%}

%%				
0				{
					SAVE_TOKEN ;
					return INT_TYPE ;
				}

[1-9][0-9]*		
				{
					SAVE_TOKEN ;
					return INT_TYPE ;
				}

[a-zA-Z_][a-zA-Z0-9_]*
				{
					SAVE_TOKEN ;
					return ID_TYPE ;
				}

">="			
				{
					return TOKEN( TOKEN_GEQ );
				}

"<="			
				{
					return TOKEN( TOKEN_LEQ );
				}

"!="			
				{
					return TOKEN( TOKEN_NEQ );
				}

"struct"			
				{
					return TOKEN( TOKEN_STRUCT );
				}
%%
"=="			
				{
					return TOKEN( TOKEN_EQ );
				}


"while"			
				{
					return TOKEN( TOKEN_WHILE );
				}

"if"			
				{
					return TOKEN( TOKEN_IF );
				}

"else"			
				{
					return TOKEN( TOKEN_ELSE );
				}

"for"			
				{
					return TOKEN( TOKEN_FOR );
				}

"foreach"		
				{
					return TOKEN( TOKEN_EACH );
				}

"do"			
				{ //don't support
					yyterminate();
				}

[ \t]			
				{
				}
%%				
int yywrap(void){
	return 1;
}
