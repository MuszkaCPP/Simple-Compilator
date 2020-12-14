import ply.lex as lex
import ply.yacc as yacc
import sys
from symbol import Symbol
from code_generator import CodeGenerator
from machine_math_manager import MachineMathManager

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

def p_command_read(p):
    'command : READ identifier SEMICOLON'

    code_generator.read_from_reg(get_symbol_address(p[2]),'f')
    symbol = get_symbol_by_name(p[2])
    symbol.set_value(-1)

def p_command_assignment(p):
    'command : identifier ASSIGNMENT expression SEMICOLON'

    global tab_index, left_is_var, right_is_var, machine_math_manager
    if p[2] == ":=":
        if(p[3]==-1 or p[3]==-2 or p[3]==-3 or p[3]==-4 or p[3]==-5):
            if(is_tab(p[1])):
                code_generator.set_address_for_machine(get_symbol_address(p[1], tab_indexes.pop()))
            else:
                code_generator.set_address_for_machine(get_symbol_address(p[1]))

            if(left_is_var):
                if(right_is_var):
                    machine_math_manager.carry_out_operation(
                                            operation=p[3],
                                            address_a=get_symbol_address(machine_math_values[0]),
                                            address_b=get_symbol_address(machine_math_values[1])
                                            )
                else:
                    machine_math_manager.carry_out_operation(
                                            operation=p[3],
                                            address_a=get_symbol_address(machine_math_values[0]),
                                            var_b = machine_math_values[1]
                                            )
            else:
                if(right_is_var):
                    machine_math_manager.carry_out_operation(
                                            operation=p[3],
                                            var_a = machine_math_values[0],
                                            address_b=get_symbol_address(machine_math_values[1])
                                            )
            return

        symbol = get_symbol_by_name(p[1])

        # LOVELY SPAGHETTI B)
        # tab(i) == number
        if(is_tab(p[1]) and not symbol_exists(p[3])):
            index = tab_indexes[-1]
            symbol.get_tab_symbol_value_at_index(p[3], index)

            code_generator.store_value_at_address(
                    p[3], get_symbol_address(p[1], tab_indexes.pop()), 'a'
                )

        # tab(i) == tab2(i)/variable
        elif(is_tab(p[1]) and symbol_exists(p[3])):
            symbol_asgn = get_symbol_by_name(p[3])
            value = 0

            # tab(i) == tab2(i)
            if(is_tab(p[3])):
                index = tab_indexes[-1]
                value = symbol_asgn.get_tab_symbol_values()[index]
                code_generator.print_value_from_adress(
                        'b', get_symbol_address(p[3], tab_indexes.pop())
                    )

            # tab(i) == variable    
            else:
                value = symbol_asgn.get_symbol_value()
                code_generator.print_value_from_adress('b', get_symbol_address(p[3]))
            
            index = tab_indexes[-1]
            address = get_symbol_address(p[1], tab_indexes.pop())
            code_generator.store_value_from_reg_at_address(address, 'b')

            symbol.get_tab_symbol_value_at_index(value, index)

        else:
            # variable = tab(i)
            if(is_tab(p[3])):
                index = tab_indexes[-1]
                value = get_symbol_by_name(p[3]).get_tab_symbol_values()[index]
                code_generator.store_value_at_address(
                        value, get_symbol_address(p[1], tab_indexes.pop()), 'a'
                    )
            # variable = number
            else:
                if(symbol_exists(p[3])):
                    symbol.set_value(get_symbol_by_name(p[3]).get_symbol_value())
                    value = get_symbol_by_name(p[3]).get_symbol_value()
                    code_generator.store_value_at_address(value, get_symbol_address(p[1]), 'a')
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

    global tab_indexes, last_read_symbol
    if(symbol_exists(p[2])):
        if is_tab(p[2]):
            index = tab_indexes.pop()
            if(index == -1):
                code_generator.store_from_address_to_address(
                                    get_symbol_address(last_read_symbol),
                                    get_symbol_address(p[2]),
                                    True
                                )
            else:
                code_generator.print_value_from_adress(
                        'f', get_symbol_address(p[2], index), True
                    )
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
    global tab_indexes, left_is_var, right_is_var
    machine_math = False

    #Machine maths
    if(symbol_exists(p[1]) or symbol_exists(p[3])):
        if(symbol_exists(p[1]) and not is_tab(p[1])):
            value = get_symbol_by_name(p[1]).value
            left_is_var = True
            if(value == -1):
                machine_math = True
        if(symbol_exists(p[3])and not is_tab(p[3])):
            value = get_symbol_by_name(p[3]).value
            right_is_var = True
            if(value == -1):
                machine_math = True
                
    #Compiler maths
    if(not machine_math and (symbol_exists(p[1]) or symbol_exists(p[3]))):
        if(is_tab(p[3])):
            p[3] = get_symbol_by_name(p[3]).get_tab_symbol_values()[tab_indexes.pop()]
        elif(symbol_exists(p[3])):
            p[3] = get_symbol_by_name(p[3]).get_symbol_value()

        if(is_tab(p[1])):
            p[1] = get_symbol_by_name(p[1]).get_tab_symbol_values()[tab_indexes.pop()]
        elif(symbol_exists(p[1])):
            p[1] = get_symbol_by_name(p[1]).get_symbol_value()

    if(machine_math):
            machine_math_values.append(p[1])
            machine_math_values.append(p[3])

    if p[2] == '+':
        if(machine_math):
            p[0] = -1
        else:
            p[0] = p[1] + p[3]
    elif p[2] == '-':
        if(machine_math):
            p[0] = -2
        else:
            p[0] = p[1] - p[3]
    elif p[2] == '*':
        if(machine_math):
            p[0] = -3
        else:
            p[0] = p[1] * p[3]
    elif p[2] == '/':
        if(machine_math):
            p[0] = -4
        else:
            p[0] = p[1] // p[3]
    elif p[2] == '%':
        if(machine_math):
            p[0] = -5
        else:
            p[0] = p[1] % p[3]

def p_condition(p):
    '''condition : value EQUALS value
                 | value NOT_EQUALS value
                 | value LOWER value
                 | value GREATER value
                 | value LEQ value
                 | value GEQ value'''
                    
def p_value_num(p):
    'value : NUM'
    p[0] = p[1]

def p_value_identifier(p):
    'value : identifier'
    p[0] = p[1]
    
def p_identifier(p):
    '''identifier : pidentifier
                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET'''
    global tab_indexes, last_read_symbol
    
    if(len(p)>2 and type(p[3])==str):
        last_read_symbol = p[3]
        index = get_symbol_by_name(p[3]).get_symbol_value()
        tab_indexes.append(index)

    p[0] = p[1]

def p_identifier_tab(p):
    'identifier : pidentifier LEFT_BRACKET NUM RIGHT_BRACKET'
    global tab_indexes
    p[0] = p[1]
    tab_indexes.append(p[3])

def p_error(p):
    print("[Błąd składni]")

lexer = lex.lex()
parser = yacc.yacc(start='program')
code_generator = CodeGenerator()
machine_math_manager = MachineMathManager(code_generator)

symbols = []
tab_indexes = []
left_is_var = False
right_is_var = False
machine_math_values = []
last_read_symbol = ''

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
        print(str(symbol.pidentifier) + "  " + str(symbol.get_address()) +"  " + str(symbol.get_symbol_value()))

def get_lexer():
    return lexer

def get_parser():
    return parser

def get_code_generator():
    return code_generator