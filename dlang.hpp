#include <cstdlib>
#include <cstdio>
#include <string>
#include <iostream>

//using namespace std;

#define NON_TYPE  				(0)
#define INT_TYPE  (1)



class node {
	public:
		int type ;
		union {
			int intValue ; 
			char charValue ;
			std::string strValue ;
		} value ;
};

extern int sym[100];

#define TOKEN_IF  				(0)
#define TOKEN_ELSE  			(1)
#define TOKEN_WHILE  			(2)
#define TOKEN_FOR  				(3)
#define TOKEN_EACH  			(4)
#define TOKEN_NUM  				(5)
#define TOKEN_ID  				(6)
#define TOKEN_GE  				(7)
#define TOKEN_LE  				(8)
#define TOKEN_LE  				(9)
#define TOKEN_ASSIGN  			(10)
#define TOKEN_LESS  			(11)
#define TOKEN_GREAT  			(12)
#define TOKEN_AND  				(13)
#define TOKEN_OR  				(14)
#define TOKEN_NOT  				(15)
#define TOKEN_STRUCT  			(16)
#define TOKEN_INT  				(17)
#define TOKEN_FLOAT  			(18)
#define TOKEN_CHAR  			(19)
#define TOKEN_BRACKET  			(20)
//#define TOKEN_IF  				(0)
//#define TOKEN_IF  				(0)
