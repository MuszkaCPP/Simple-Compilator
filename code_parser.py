import ply.lex as lex
import ply.yacc as yacc
import sys
from symbol import Symbol
from code_generator import CodeGenerator

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
t_ignore_RUBBISH = r'[ \t\n]+'
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

def p_program(p):
    '''program : DECLARE declarations BEGIN commands END
               | BEGIN commands END'''

def p_declarations_muliple(p):
    '''declarations : declarations COMMA pidentifier
                    | declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET'''

    if symbol_exists(p[3]):
        throw_redeclare_error(p,3)
    if len(p) == 4:
        symbol = Symbol(p[3], code_generator.get_data_offset())
    else:
        symbol = Symbol(p[3], code_generator.get_data_offset(), True, p[5], p[7])
        code_generator.increase_data_offset(symbol.get_tab_length()-1)
    symbols.append(symbol)

def p_declarations_single_var(p):
    'declarations : pidentifier'

    if symbol_exists(p[1]):
        throw_redeclare_error(p,1)
    p[0] = p[1]

    symbol = Symbol(p[1], code_generator.get_data_offset())
    symbol.set_address(code_generator.get_data_offset())
    symbols.append(symbol)

def p_declarations_single_tab(p):
    'declarations : pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET'
    if symbol_exists(p[1]):
        throw_redeclare_error(p,1)
    p[0] = p[1]

    symbol = Symbol(p[1], code_generator.get_data_offset(), True, p[3], p[5])
    symbols.append(symbol)
    code_generator.increase_data_offset(symbol.get_tab_length()-1)

def throw_redeclare_error(p, index):
    print("[Error] Line: [" + str(p.lineno(1)) + "] | Symbol redeclared! [" + str(p[index]) + "]")
    exit(-1)

def p_commands(p):
    '''commands : commands command
                | command'''
                
def p_command_assignment(p):
    '''command : identifier ASSIGNMENT expression SEMICOLON
               | READ  identifier SEMICOLON'''

    global tab_index
    if p[2] == ":=":
        symbol =  get_symbol_by_name(p[1])

        # tab(i) == number
        if(is_tab(p[1]) and not symbol_exists(p[3])):
            index = tab_indexes[-1]
            symbol.tab_symbol_value_at_index(p[3], index)
            code_generator.store_value_at_address(p[3], get_symbol_address(p[1], tab_indexes.pop()), 'a')

        # tab(i) == tab2(i)/variable
        elif(is_tab(p[1]) and symbol_exists(p[3])):
            symbol_asgn = get_symbol_by_name(p[3])
            value = 0

             # tab(i) == tab2(i)
            if(is_tab(p[3])):
                index = tab_indexes[-1]
                value = symbol_asgn.get_tab_symbol_values()[index]
                code_generator.print_value_from_adress('b', get_symbol_address(p[3], tab_indexes.pop()), False)

            # tab(i) == variable    
            else:
                value = symbol_asgn.get_symbol_value()
                code_generator.print_value_from_adress('b', get_symbol_address(p[3]), False)
            
            index = tab_indexes[-1]
            address = get_symbol_address(p[1], tab_indexes.pop())
            code_generator.store_value_from_reg_at_address(address, 'b')

            symbol.tab_symbol_value_at_index(value, index)

        else:
            # variable = tab(i)
            if(is_tab(p[3])):
                index = tab_indexes[-1]
                value = get_symbol_by_name(p[3]).get_tab_symbol_values()[index]
                code_generator.store_value_at_address(value, get_symbol_address(p[1], tab_indexes.pop()), 'a')
            # variable = number
            else:
                symbol.set_value(p[3])    
                code_generator.store_value_at_address(p[3], get_symbol_address(p[1]), 'a')

        if(not get_symbol_by_name(p[1]).is_defined):
            symbol.is_defined = True

def p_command_all(p):
    '''command : IF condition THEN commands ELSE commands ENDIF
               | IF  condition  THEN  commands  ENDIF
               | WHILE  condition  DO  commands  ENDWHILE
               | REPEAT  commands  UNTIL  condition SEMICOLON
               | FOR  pidentifier  FROM  value TO  value DO  commands  ENDFOR
               | FOR  pidentifier  FROM  value  DOWNTO  value DO  commands  ENDFOR'''

def p_command_write(p):
    'command : WRITE value SEMICOLON'

    global tab_indexes
    if(symbol_exists(p[2])):
        if is_tab(p[2]):
            code_generator.print_value_from_adress('f', get_symbol_address(p[2], tab_indexes.pop()), True)
        else:
            code_generator.print_value_from_adress('f', get_symbol_address(p[2]), True)
    else:
        code_generator.store_variable(p[2], 'a')
        code_generator.print_value_from_adress('f', code_generator.current_data_offset)

def p_expression_val(p):
    'expression : value'
    p[0] = p[1]

def p_expression_math(p):
    '''expression : value ADD value
                  | value SUB value
                  | value MUL value
                  | value DIV value
                  | value MOD value'''
    global tab_indexes
    if(symbol_exists(p[1]) or symbol_exists(p[3])):
        if(is_tab(p[3])):
            p[3] = get_symbol_by_name(p[3]).get_tab_symbol_values()[tab_indexes.pop()]
        elif(symbol_exists(p[3])):
            p[3] = get_symbol_by_name(p[3]).get_symbol_value()

        if(is_tab(p[1])):
            p[1] = get_symbol_by_name(p[1]).get_tab_symbol_values()[tab_indexes.pop()]
        elif(symbol_exists(p[1])):
            print("lel2")
            p[1] = get_symbol_by_name(p[1]).get_symbol_value()
    
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        print(p[1])
        print(p[3])
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] // p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]

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
    p[0] = p[1]

def p_identifier(p):
    '''identifier : pidentifier
                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET'''
    p[0] = p[1]

def p_identifier_tab(p):
    'identifier : pidentifier LEFT_BRACKET NUM RIGHT_BRACKET'
    global tab_index
    p[0] = p[1]
    tab_indexes.append(p[3])

def p_error(p):
    print("[Błąd składni]")

lexer = lex.lex()
parser = yacc.yacc(start='program')
code_generator = CodeGenerator()
symbols = []
constants = {}
tab_indexes = []

def symbol_exists(pidentifier):
    for symbol in symbols:
        if pidentifier == symbol.get_pidentifier():
            return True
    return False

def get_symbol_by_name(pidentifier):
    for symbol in symbols:
        if pidentifier == symbol.get_pidentifier():
            return symbol

def get_symbol_address(pidentifier, offset=0):
    for symbol in symbols:
        if pidentifier == symbol.get_pidentifier():
            if(symbol.is_tab):
                return symbol.get_address() + offset
            else:
                return symbol.get_address()

def is_tab(pidentifier):
    for symbol in symbols:
        if pidentifier == symbol.get_pidentifier() and symbol.is_tab:
            return True

    return False    

def print_all_symbols():
    for symbol in symbols:
        print(str(symbol.pidentifier) + "  " + str(symbol.get_address()) +"\n")

def get_lexer():
    return lexer

def get_parser():
    return parser

def get_code_generator():
    return code_generator