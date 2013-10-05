%{
#include <stdlib.h>
}%

%%

0

[1-9][0-9]*

">="

"<="

"!="

%%"=="

"while"

"if"

"else"

"for"

"foreach"

"do"

[ \t]

%%

int yywrap(void){
	return 1;
}
