import ply.lex as lex
import ply.yacc as yacc
import sys


tokens = (
    "READ",
    "WRITE",
    "DECLARE",
    "BEGIN",
    "END",
    'NUM',
    "pidentifier",
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    "ASSIGNMENT",
    "COMMA",
    "COLON",
    "SEMICOLON",
    "LEFT_BRACKET",
    "RIGHT_BRACKET",
    "IF",
    "THEN",
    "ENDIF",
    "ELSE",
    "WHILE",
    "DO",
    "ENDWHILE",
    "REPEAT",
    "UNTIL",
    "FOR",
    "FROM",
    "TO",
    "ENDFOR",
    "DOWNTO",
    "NOT_EQUALS",
    "EQUALS",
    "LOWER",
    "GREATER",
    "LEQ",
    "GEQ",
)

precedence = (
    ( 'left', 'ADD', 'SUB' ),
    ( 'left', 'MUL', 'DIV', 'MOD' ),
)

# Marks
t_ASSIGNMENT = r'\:='
t_COLON = r'[:]'
t_SEMICOLON = r'[;]'
t_LEFT_BRACKET = r'[(]'
t_RIGHT_BRACKET = r'[)]'
t_COMMA = r'[,]'

# Math operators
t_ADD   = r'\+'
t_SUB   = r'-'
t_MUL   = r'\*'
t_DIV   = r'/'
t_MOD   = r'\%'

# Comparisons
t_NOT_EQUALS = r'!='
t_EQUALS = r'='
t_LOWER = r'<'
t_GREATER = r'>'
t_LEQ = r'<='
t_GEQ = r'>='

#ignore
t_ignore_RUBBISH = r'[ \n]+'
t_ignore_COMMENT = r'\[.*\]'

#Number, pidentifier
def t_NUM(t):
    r'[0-9]+'
    t.value = int( t.value )
    return t

def t_pidentifier(t):
    r'[_a-z]+'
    t.value = str( t.value )
    return t

#IF, ELSE, THEN, ENDIF
t_IF = r'IF'
t_THEN = r'THEN'
t_ENDIF = r'ENDIF'
t_ELSE = r'ELSE'

#WHILE, DO, ENDWHILE
t_WHILE = r'WHILE'
t_DO = r'DO'
t_ENDWHILE = r'ENDWHILE'

#REPEAT, UNTIL
t_REPEAT = r'REPEAT'
t_UNTIL = r'UNTIL'

#FOR, FROM, TO, DOWNTO, ENDFOR
t_FOR = r'FOR'
t_FROM = r'FROM'
t_TO = r'TO'
t_ENDFOR = r'ENDFOR'
t_DOWNTO = r'DOWNTO'

#DECLARE, BEGIN, END, READ, WRITE
t_DECLARE = r'DECLARE'
t_BEGIN = r'BEGIN'
t_END = r'END'
t_READ = r'READ'
t_WRITE = r'WRITE'

def t_error(t):
    print("Invalid Token:",t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

start = 'program'

def p_program(p):
    '''program : DECLARE declarations BEGIN commands END
               | BEGIN commands END'''

def p_declarations(p):
    '''declarations : declarations COMMA pidentifier
                    | declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET
                    | pidentifier
                    | pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET'''

def p_commands(p):
    '''commands : commands command
                | command'''
def p_command(p):
    '''command : identifier ASSIGNMENT expression SEMICOLON
               | IF condition THEN commands ELSE commands ENDIF
               | IF  condition  THEN  commands  ENDIF
               | WHILE  condition  DO  commands  ENDWHILE
               | REPEAT  commands  UNTIL  condition SEMICOLON
               | FOR  pidentifier  FROM  value TO  value DO  commands  ENDFOR
               | FOR  pidentifier  FROM  value  DOWNTO  value DO  commands  ENDFOR
               | READ  identifier SEMICOLON
               | WRITE  value SEMICOLON'''
    # if(p[1]=="WRITE"):
    #     println(p[2])

def p_expression(p):
    '''expression : value
                  | value ADD value
                  | value SUB value
                  | value MUL value
                  | value DIV value
                  | value MOD value'''
    if p[1] == "+":
        print(p[0]+p[2])

def p_condition(p):
    '''condition : value EQUALS value
                 | value NOT_EQUALS value
                 | value LOWER value
                 | value GREATER value
                 | value LEQ value
                 | value GEQ value'''
                    
def p_value(p):
    '''value : NUM
             | identifier'''
            
def p_identifier(p):
    '''identifier : pidentifier
                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET
                  | pidentifier LEFT_BRACKET NUM RIGHT_BRACKET'''


def p_error(p):
    print("[Błąd składni]")

parser = yacc.yacc()

lines = ""

inp = "DECLARE [ XDDDD ]\
    a\
BEGIN\
    a:=2;\
    WRITE a;\
END"

lexer.input(inp)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

res = parser.parse(inp)
