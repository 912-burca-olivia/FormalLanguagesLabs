%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1 
%}

%token PROGRAM
%token INT
%token FLOAT
%token LONG
%token UNSIGNED
%token STRING
%token CHAR
%token WHILE
%token IF
%token ELSE
%token READ
%token PRINT

%token ASSIGN
%token PLUS
%token MINUS
%token MUL
%token DIV
%token MOD
%token EQUAL
%token NOT_EQUAL
%token NOT
%token LT
%token GT
%token LET
%token GET

%token OPEN_ROUND_BRACKET
%token CLOSED_ROUND_BRACKET
%token SEMI_COLON
%token COMMA
%token OPEN_CURLY_BRACKET
%token CLOSED_CURLY_BRACKET

%token IDENTIFIER
%token CONSTANT_NUMBER
%token CONSTANT_STRING
%token CONSTANT_CHARACTER

%start program

%%

program : PROGRAM OPEN_CURLY_BRACKET declaration_list statements CLOSED_CURLY_BRACKET
declaration_list : declaration declaration_list | /*Empty*/
declaration : var_type IDENTIFIER SEMI_COLON
var_type : INT | FLOAT | LONG | UNSIGNED | CHAR | STRING
expression : term sign_and_expression
sign_and_expression : sign expression | /*Empty*/
sign : PLUS | MINUS | MUL | DIV | MOD
term : IDENTIFIER | constant
constant : CONSTANT_NUMBER | CONSTANT_STRING | CONSTANT_CHARACTER
statements : statement statements | /*Empty*/
statement : simple_stmt | struct_stmt
simple_stmt : assignment_stmt | input_output_stmt
struct_stmt : if_stmt | while_stmt
assignment_stmt : IDENTIFIER ASSIGN expression SEMI_COLON
input_output_stmt : READ term SEMI_COLON | PRINT term SEMI_COLON
if_stmt : IF OPEN_ROUND_BRACKET condition CLOSED_ROUND_BRACKET OPEN_CURLY_BRACKET statements CLOSED_CURLY_BRACKET else_stmt
else_stmt : ELSE OPEN_CURLY_BRACKET statements CLOSED_CURLY_BRACKET | /*Empty*/
while_stmt : WHILE OPEN_ROUND_BRACKET condition CLOSED_ROUND_BRACKET OPEN_CURLY_BRACKET statements CLOSED_CURLY_BRACKET
condition : expression relation expression
relation : EQUAL | NOT_EQUAL | LT | GT | LET | GET

%%
yyerror(char *s)
{	
	printf("%s\n",s);
}

extern FILE *yyin;

int main(int argc, char **argv)
{
	printf("Argc: %d\n", argc);
     printf("Argv[1]: %s\n", argv[1]);
 yyin = fopen( argv[1], "r" );  
    if (!yyin)
    {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        
    } 
	if(argc>1) yyin :  fopen(argv[1],"r");
	if(argc>2 && !strcmp(argv[2],"-d")) yydebug: 1;
	if(!yyparse()) fprintf(stderr, "\t No errors found \n");
}