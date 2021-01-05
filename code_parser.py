import ply.lex as lex
import ply.yacc as yacc
import sys
from symbol import Symbol
from code_generator import CodeGenerator
from machine_math_manager import MachineMathManager
from machine_conditions_manager import MachineConditionsManager

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

    global tab_indexes, last_read_symbols, if_passes

    if(len(if_passes)>1 and not if_passes[-2]):
        return

    if(in_if_statement and not if_passes[-1]):
        return

    symbol = get_symbol_by_name(p[2])

    if(is_tab(p[2])):
        index = tab_indexes.pop()
        if(index==-1):
            #READ tab(a)
            code_generator.store_unknown_value_from_adress_to_address(
                get_symbol_address(last_read_symbols.pop()),
                get_symbol_address(p[2])
            )
        else:
            code_generator.read_from_reg(get_symbol_by_name(p[2]).get_tab_index_address(index),'f')
            symbol.set_tab_symbol_value_at_index(-1, index)
    else:
        code_generator.read_from_reg(get_symbol_address(p[2]),'f')
        symbol.set_value(-1)

def p_command_assignment(p):
    'command : identifier ASSIGNMENT expression SEMICOLON'

    global tab_indexes, left_is_var, right_is_var, machine_math_manager, machine_math_values, machine_math, last_read_symbols,if_passes

    if(len(if_passes)>1 and not if_passes[-2]):
        return

    if(in_if_statement and not if_passes[-1]):
        return

    #Machine math
    if( p[3] == '+' 
        or p[3] == '-'
        or p[3] == '*'
        or p[3] == '/'
        or p[3] == '%'
        ):

        if(left_is_var):
            left_symbol = get_symbol_by_name(machine_math_values[0])
            left_symbol_address = left_symbol.get_address()

            if(left_symbol.is_tab):
                if(right_is_var):
                    right_symbol = get_symbol_by_name(machine_math_values[1])
                    right_symbol_address = right_symbol.get_address()
                    #tab(a) [+] tab(b)
                    if(right_symbol.is_tab):
                        right_index = tab_indexes.pop()
                        left_index = tab_indexes.pop()

                        if(right_index == -1):
                            right_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            right_index_address = 0
                            right_symbol_address += right_index

                        if(left_index == -1):
                            left_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            left_index_address = 0
                            left_symbol_address += left_index

                        machine_math_manager.carry_out_operation(
                            operation = p[3],
                            address_a=left_symbol_address,
                            left_index_address=left_index_address,
                            address_b=right_symbol_address,
                            right_index_address= right_index_address
                        )
                    #tab(a) + variable
                    else:
                        left_index = tab_indexes.pop()
                        if(left_index == -1):
                            left_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            left_index_address = 0
                            left_symbol_address += left_index

                        machine_math_manager.carry_out_operation(
                            operation=p[3],
                            address_a=left_symbol_address,
                            left_index_address=left_index_address,
                            address_b=right_symbol_address
                        )

                #tab(a) + value
                else:
                    left_index = tab_indexes.pop()
                    if(left_index == -1):
                        left_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                    else:
                        left_index_address = 0
                        left_symbol_address += left_index

                    right_value = machine_math_values[1]

                    machine_math_manager.carry_out_operation(
                        operation=p[3],
                        address_a=left_symbol_address,
                        left_index_address=left_index_address,
                        val_b=right_value
                    )
            else:
                if(right_is_var):
                    right_symbol = get_symbol_by_name(machine_math_values[1])
                    right_symbol_address = right_symbol.get_address()

                    #variable + tab(i)
                    if(right_symbol.is_tab):
                        right_index = tab_indexes.pop()
                        
                        if(right_index == -1):
                            right_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            right_index_address = 0
                            right_symbol_address += right_index

                        machine_math_manager.carry_out_operation(
                            operation=p[3],
                            address_a=left_symbol_address,
                            address_b=right_symbol_address,
                            right_index_address=right_index_address
                        )
                    #variable + variable
                    else:
                        machine_math_manager.carry_out_operation(
                            operation=p[3],
                            address_a=get_symbol_address(machine_math_values[0]),
                            address_b=get_symbol_address(machine_math_values[1])
                        )
                #variable + number
                else:
                    machine_math_manager.carry_out_operation(
                        operation=p[3],
                        address_a=get_symbol_address(machine_math_values[0]),
                        val_b = machine_math_values[1]
                    )
        else:
            
            if(right_is_var):
                right_symbol = get_symbol_by_name(machine_math_values[1])
                right_symbol_address = right_symbol.get_address()
                left_value = machine_math_values[0]

                #number + tab(i)
                if(right_symbol.is_tab):
                    right_index = tab_indexes.pop()
                        
                    if(right_index == -1):
                        right_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                    else:
                        right_index_address = 0
                        right_symbol_address += right_index

                    machine_math_manager.carry_out_operation(
                        operation=p[3],
                        val_a=left_value,
                        address_b=right_symbol_address,
                        right_index_address=right_index_address,
                    )
                #number + variable
                else:
                    machine_math_manager.carry_out_operation(
                        operation=p[3],
                        val_a = machine_math_values[0],
                        address_b=right_symbol_address
                    )

        left_side_symbol = get_symbol_by_name(p[1])

        if(left_side_symbol.is_tab):
            index = tab_indexes[0]
            tab_indexes = tab_indexes[1:]
            if(index == -1):
                index_address = get_symbol_by_name(last_read_symbols[0]).get_address()
                last_read_symbols = last_read_symbols[1:]

                code_generator.store_from_reg_to_unknown_index(
                    reg='e',
                    tab_address=left_side_symbol.get_address(),
                    index_address=index_address
                )
            else:
                left_side_symbol.set_tab_symbol_value_at_index(-1, index)
                code_generator.store_value_from_reg_at_address(
                    address=left_side_symbol.get_tab_index_address(index),
                    reg='e'
                )
        else:
            left_side_symbol.set_value(-1)
            code_generator.store_value_from_reg_at_address(
                address=left_side_symbol.get_address(),
                reg='e'
            )

        machine_math_values = machine_math_values[2:]
        left_is_var = False
        right_is_var = False
        machine_math = False
        return


    if p[2] == ":=":

        symbol = get_symbol_by_name(p[1])

        # tab(i) := []
        if(is_tab(p[1])):
            if(symbol_exists(p[3])):
                symbol_asgn = get_symbol_by_name(p[3])

                # tab(i) := tab_2(i)
                if(is_tab(p[3])):
                    right_index = tab_indexes.pop()
                    left_index = tab_indexes.pop()
                    value = symbol_asgn.get_tab_symbol_value(right_index)

                    #tab(a) dla READ a
                    if(left_index == -1 and right_index == -1):
                        right_index_address = get_symbol_address(last_read_symbols.pop())
                        left_index_address = get_symbol_address(last_read_symbols.pop())

                        code_generator.store_unknown_tab_with_unknown_indexes(
                                        symbol_asgn.get_address(),
                                        right_index_address,
                                        symbol.get_address(),
                                        left_index_address
                        )
                    elif(value == -1):
                        code_generator.store_from_address_to_address(
                                    symbol_asgn.get_tab_index_address(right_index),
                                    symbol.get_tab_index_address(left_index)
                        )
                        symbol.set_tab_symbol_value_at_index(-1, left_index)

                    else:
                        code_generator.store_value_at_address(
                                        value,
                                        get_symbol_address(p[1], left_index),
                                        'a'
                        )
                        symbol.set_tab_symbol_value_at_index(value, left_index)
                # tab(i) := variable
                else:
                    index = tab_indexes.pop()
                    value = symbol_asgn.get_symbol_value()
                    if(value == -1):
                        if(index == -1):
                            index_address = get_symbol_address(last_read_symbols.pop())

                            code_generator.store_unknown_value_by_unknown_index(
                                            symbol_asgn.get_address(),
                                            symbol.get_address(),
                                            index_address
                            )
                            #symbol.set_tab_symbol_value_at_index(-1, index_address) -> prawdopodobnie useless
                        else:
                            code_generator.store_from_address_to_address(
                                            symbol_asgn.get_address(),
                                            symbol.get_tab_index_address(index)
                            )
                            symbol.set_tab_symbol_value_at_index(-1, index)
                    else:
                        code_generator.store_value_at_address(
                                        value,
                                        get_symbol_address(p[1], index),
                                        'a'
                        )
                        symbol.set_tab_symbol_value_at_index(value, index)
            # tab(i) := number
            else:
                index = tab_indexes.pop()
                value = p[3]
                if(index == -1):
                    index_address = get_symbol_address(last_read_symbols.pop())
                    code_generator.store_value_at_unknown_index(
                                    value,
                                    symbol.get_address(),
                                    index_address
                    )
                    #symbol.set_tab_symbol_value_at_index(value, index_address)
                else:
                    code_generator.store_value_at_address(
                                    value,
                                    get_symbol_address(p[1], index),
                                    'a'
                    )

                    symbol.set_tab_symbol_value_at_index(value, index)
        else:
            if(symbol_exists(p[3])):
                symbol_asgn = get_symbol_by_name(p[3])

                # variable = tab(i)
                if(is_tab(p[3])):
                    index = tab_indexes.pop()
                    value = symbol_asgn.get_tab_symbol_value(index)
                    if(value == -1):
                        code_generator.store_from_address_to_address(
                            symbol_asgn.get_tab_index_address(index),
                            symbol.get_address()
                        )
                    else:
                        code_generator.store_value_at_address(
                                        value,
                                        symbol.get_address(),
                                        'a'
                        )
                        
                    symbol.set_value(value)

                # variable = variable
                else:
                    value = symbol_asgn.get_symbol_value()

                    if(value == -1):
                        code_generator.store_from_address_to_address(
                            symbol_asgn.get_address(),
                            symbol.get_address()
                        )

                    else:
                        code_generator.store_value_at_address(
                            value,
                            symbol.get_address(),
                            'a'
                        )

                    symbol.set_value(value)
            # variable = number        
            else:
                value = p[3]
                
                code_generator.store_value_at_address(
                    value,
                    symbol.get_address(),
                    'a'
                )

                symbol.set_value(value)

        if(not get_symbol_by_name(p[1]).is_defined):
            symbol.is_defined = True
        

def p_command_all(p):
    '''command : REPEAT  commands  UNTIL  condition SEMICOLON
               | FOR  pidentifier  FROM  value TO  value DO  commands  ENDFOR
               | FOR  pidentifier  FROM  value  DOWNTO  value DO  commands  ENDFOR'''

def p_command_while(p):
    'command : WHILE while_occured condition  DO  commands  ENDWHILE'

    global in_while_loop

    if(machine_conditions.pop()):
        code_generator.replace_jump_for_condition(_while=True)
    
    in_while_loop.pop()

def p_command_while_occured(p):
    'while_occured :'

    global in_while_loop

    in_while_loop.append(True)

    code_generator.save_current_code_length()

def p_command_if_else(p):
    'command : IF if_occured condition THEN commands ELSE else_occured commands ENDIF'

    global in_if_statement, machine_conditions, else_occured

    if(machine_conditions.pop()):
        code_generator.replace_jump_for_condition()
        return

    if_passes.pop()

    if(len(if_passes) == 0):
        in_if_statement = False

def p_command_else_occured(p):
    'else_occured :'
    global if_passes, else_occured

    if(machine_conditions[-1]):
        code_generator.replace_jump_for_condition(pop=False)
        return
    
    if(if_passes.pop() is True):
        if_passes.append(False)
    else:
        if_passes.append(True)

def p_command_if_endif(p):
    'command : IF if_occured condition  THEN  commands  ENDIF'

    global in_if_statement, machine_conditions

    if(machine_conditions.pop()):
        code_generator.replace_jump_for_condition()
        return

    if_passes.pop()

    if(len(if_passes) == 0):
        in_if_statement = False

def p_if_occured(p):
    "if_occured :"
    
    global in_if_statement
    in_if_statement = True

def p_command_write(p):
    'command : WRITE value SEMICOLON'

    global tab_indexes, last_read_symbols, in_if_statement, if_passes

    if(len(if_passes)>1 and not if_passes[-2]):
        return

    elif(in_if_statement and not if_passes[-1]):
        return

        
    if(symbol_exists(p[2])):
        if is_tab(p[2]):
            index = tab_indexes.pop()

            if(index == -1):
                code_generator.print_value_by_unknown_index(
                        get_symbol_address(last_read_symbols.pop()),
                        get_symbol_address(p[2])
                )
            else:
                code_generator.generate_value_from_adress_at_register(
                                'f',
                                get_symbol_address(p[2], index),
                                True
                )
        else:
            code_generator.generate_value_from_adress_at_register('f', get_symbol_address(p[2]), True)
    else:
        code_generator.store_number(p[2], 'a')
        code_generator.generate_value_from_adress_at_register(
                        'f',
                        code_generator.current_data_offset,
                        True
        )

def p_expression_val(p):
    'expression : value'
    p[0] = p[1]

def p_expression_math(p):
    '''expression : value ADD value
                  | value SUB value
                  | value MUL value
                  | value DIV value
                  | value MOD value'''
                  
    global tab_indexes, left_is_var, right_is_var, machine_math_manager, machine_math_values, in_while_loop
    machine_math = False
    left_is_var = False
    right_is_var = False
    left_index = 0
    right_index = 0

    #Machine maths
    if(symbol_exists(p[3])):
        right_is_var = True
        value = 0
        if(is_tab(p[3])):
            right_index = tab_indexes.pop()
            if(get_symbol_by_name(p[3]).get_tab_symbol_value(right_index)==-1):
                machine_math = True
        else:
            value = get_symbol_by_name(p[3]).get_symbol_value()
        
        if(value == -1 or right_index == -1 or in_while_loop[-1]):
            machine_math = True

    if(symbol_exists(p[1])):
        left_is_var = True
        value = 0
        if(is_tab(p[1])):
            left_index = tab_indexes.pop()
            if(get_symbol_by_name(p[3]).get_tab_symbol_value(left_index)==-1):
                machine_math = True
        else:
            value = get_symbol_by_name(p[1]).get_symbol_value()
        
        if(value == -1 or left_index == -1 or in_while_loop[-1]):
            machine_math = True

    if(is_tab(p[1])):
        tab_indexes.append(left_index)
    if(is_tab(p[3])):
        tab_indexes.append(right_index) 
                
    #Compiler maths
    if(not machine_math and (symbol_exists(p[1]) or symbol_exists(p[3]))):
        if(is_tab(p[3])):
            p[3] = get_symbol_by_name(p[3]).get_tab_symbol_value(tab_indexes.pop())
        elif(symbol_exists(p[3])):
            p[3] = get_symbol_by_name(p[3]).get_symbol_value()

        if(is_tab(p[1])):
            p[1] = get_symbol_by_name(p[1]).get_tab_symbol_value(tab_indexes.pop())
        elif(symbol_exists(p[1])):
            p[1] = get_symbol_by_name(p[1]).get_symbol_value()
        

    if(machine_math):
        machine_math_values.append(p[1])
        machine_math_values.append(p[3])

    if p[2] == '+':
        if(machine_math):
            p[0] = '+'
        else:
            p[0] = p[1] + p[3]
    elif p[2] == '-':
        if(machine_math):
            p[0] = '-'
        else:
            p[0] = p[1] - p[3]
    elif p[2] == '*':
        if(machine_math):
            p[0] = '*'
        else:
            p[0] = p[1] * p[3]
    elif p[2] == '/':
        if(machine_math):
            p[0] = '/'
        else:
            p[0] = p[1] // p[3]
    elif p[2] == '%':
        if(machine_math):
            p[0] = '%'
        else:
            p[0] = p[1] % p[3]

def p_condition(p):
    '''condition : value EQUALS value
                 | value NOT_EQUALS value
                 | value LOWER value
                 | value GREATER value
                 | value LEQ value
                 | value GEQ value'''

    global in_if_statement, if_passes, machine_conditions_manager, tab_indexes, machine_conditions, in_while_loop
    left_is_var = False
    right_is_var = False
    machine_condition = False
    condition = ""
    left_index = 0
    right_index = 0
    machine_condition_values = []

    #Machine conditions
    if(symbol_exists(p[3])):
        right_is_var = True
        value = 0
        if(is_tab(p[3])):
            right_index = tab_indexes.pop()
            if(get_symbol_by_name(p[3]).get_tab_symbol_value(right_index)==-1):
                machine_condition = True
        else:
            value = get_symbol_by_name(p[3]).get_symbol_value()
        
        if(value == -1 or right_index == -1 or in_while_loop[-1]):
            machine_condition = True

    if(symbol_exists(p[1])):
        left_is_var = True
        value = 0
        if(is_tab(p[1])):
            left_index = tab_indexes.pop()
            if(get_symbol_by_name(p[1]).get_tab_symbol_value(left_index)==-1):
                machine_condition = True
        else:
            value = get_symbol_by_name(p[1]).get_symbol_value()
        
        if(value == -1 or left_index == -1 or in_while_loop[-1]):
            machine_condition = True

    if(is_tab(p[1])):
        tab_indexes.append(left_index)
    if(is_tab(p[3])):
        tab_indexes.append(right_index)  

    if(not machine_condition and (symbol_exists(p[1]) or symbol_exists(p[3]))):
        if(in_while_loop[-1]):
            if(is_tab(p[3])):
                p[3] = get_symbol_by_name(p[3]).get_tab_index_address(tab_indexes.pop())
            elif(symbol_exists(p[3])):
                p[3] = get_symbol_by_name(p[3]).get_address()

            if(is_tab(p[1])):
                p[1] = get_symbol_by_name(p[1]).get_tab_index_address(tab_indexes.pop())
            elif(symbol_exists(p[1])):
                p[1] = get_symbol_by_name(p[1]).get_address()

        else:
            if(is_tab(p[3])):
                p[3] = get_symbol_by_name(p[3]).get_tab_symbol_value(tab_indexes.pop())
            elif(symbol_exists(p[3])):
                p[3] = get_symbol_by_name(p[3]).get_symbol_value()

            if(is_tab(p[1])):
                p[1] = get_symbol_by_name(p[1]).get_tab_symbol_value(tab_indexes.pop())
            elif(symbol_exists(p[1])):
                p[1] = get_symbol_by_name(p[1]).get_symbol_value()

    if(machine_condition):
        machine_conditions.append(True)
        machine_condition_values.append(p[1])
        machine_condition_values.append(p[3])
    else:
        machine_conditions.append(False)

    if p[2] == '=':
        condition = "="
        if(not machine_condition and not in_while_loop[-1]):
            if(p[1] == p[3]):
                p[0] = True
            else:
                p[0] = False
    elif p[2] == '!=':
        condition = "!="
        if(not machine_condition and not in_while_loop[-1]):
            if(p[1] != p[3]):
                p[0] = True
            else:
                p[0] = False
    elif p[2] == '<':
        condition = "<"
        if(not machine_condition and not in_while_loop[-1]):
            if(p[1] < p[3]):
                p[0] = True
            else:
                p[0] = False
    elif p[2] == '>':
        condition = ">"
        if(not machine_condition and not in_while_loop[-1]):
            if(p[1] > p[3]):
                p[0] = True
            else:
                p[0] = False
    elif p[2] == '<=':
        condition = "<="
        if(not machine_condition and not in_while_loop[-1]):
            if(p[1] <= p[3]):
                p[0] = True
            else:
                p[0] = False
    elif p[2] == '>=':
        condition = ">="
        if(not machine_condition and not in_while_loop[-1]):
            if(p[1] >= p[3]):
                p[0] = True
            else:
                p[0] = False

    if(in_if_statement and machine_condition):
        if_passes.append(True)
    elif(in_if_statement and not machine_condition):
        if(p[0] == False):
            if_passes.append(False)
        elif(p[0] == True):
            if(len(if_passes) > 0 and if_passes[-1] == False):
                if_passes.append(False)
            else:
                if_passes.append(True)
        return

    if(not machine_condition and in_while_loop[-1]):
        if(left_is_var):
            if(right_is_var):
                machine_conditions_manager.carry_out_condition(
                    condition=condition,
                    address_a=p[1],
                    address_b=p[3]
                )
            else:
                machine_conditions_manager.carry_out_condition(
                    condition=condition,
                    address_a=p[1],
                    val_b=p[3]
                )
        else:
            if(right_is_var):
                machine_conditions_manager.carry_out_condition(
                    condition=condition,
                    val_a=p[1],
                    address_b=p[3]
                )
            else:
                machine_conditions_manager.carry_out_condition(
                    condition=condition,
                    val_a=p[1],
                    val_b=p[3]
                )
        machine_conditions[-1]=True
        
    elif(machine_condition):
        if(left_is_var):
            left_symbol = get_symbol_by_name(machine_condition_values[0])
            left_symbol_address = left_symbol.get_address()

            if(left_symbol.is_tab):
                if(right_is_var):
                    right_symbol = get_symbol_by_name(machine_condition_values[1])
                    right_symbol_address = right_symbol.get_address()
                    #tab(a) [?] tab(b)
                    if(right_symbol.is_tab):
                        right_index = tab_indexes.pop()
                        left_index = tab_indexes.pop()

                        if(right_index == -1):
                            right_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            right_index_address = 0
                            right_symbol_address += right_index

                        if(left_index == -1):
                            left_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            left_index_address = 0
                            left_symbol_address += left_index

                        machine_conditions_manager.carry_out_condition(
                            condition=condition,
                            address_a=left_symbol_address,
                            left_index_address=left_index_address,
                            address_b=right_symbol_address,
                            right_index_address= right_index_address
                        )
                    #tab(a) [?] variable
                    else:
                        left_index = tab_indexes.pop()
                        if(left_index == -1):
                            left_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            left_index_address = 0
                            left_symbol_address += left_index

                        machine_conditions_manager.carry_out_condition(
                            condition=condition,
                            address_a=left_symbol_address,
                            left_index_address=left_index_address,
                            address_b=right_symbol_address
                        )

                #tab(a) [?] value
                else:
                    left_index = tab_indexes.pop()
                    if(left_index == -1):
                        left_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                    else:
                        left_index_address = 0
                        left_symbol_address += left_index

                    right_value = machine_condition_values[1]

                    machine_conditions_manager.carry_out_condition(
                        condition=condition,
                        address_a=left_symbol_address,
                        left_index_address=left_index_address,
                        val_b=right_value
                    )
            else:
                if(right_is_var):
                    right_symbol = get_symbol_by_name(machine_condition_values[1])
                    right_symbol_address = right_symbol.get_address()

                    #variable [?] tab(i)
                    if(right_symbol.is_tab):
                        right_index = tab_indexes.pop()
                        
                        if(right_index == -1):
                            right_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                        else:
                            right_index_address = 0
                            right_symbol_address += right_index

                        machine_conditions_manager.carry_out_condition(
                            condition=condition,
                            address_a=left_symbol_address,
                            address_b=right_symbol_address,
                            right_index_address=right_index_address
                        )
                    #variable [?] variable
                    else:
                        machine_conditions_manager.carry_out_condition(
                            condition=condition,
                            address_a=get_symbol_address(machine_condition_values[0]),
                            address_b=get_symbol_address(machine_condition_values[1])
                        )
                #variable [?] number
                else:
                    machine_conditions_manager.carry_out_condition(
                        condition=condition,
                        address_a=get_symbol_address(machine_condition_values[0]),
                        val_b = machine_condition_values[1]
                    )
        else:
            
            if(right_is_var):
                right_symbol = get_symbol_by_name(machine_condition_values[1])
                right_symbol_address = right_symbol.get_address()
                left_value = machine_condition_values[0]

                #number [?] tab(i)
                if(right_symbol.is_tab):
                    right_index = tab_indexes.pop()
                        
                    if(right_index == -1):
                        right_index_address = get_symbol_by_name(last_read_symbols.pop()).get_address()
                    else:
                        right_index_address = 0
                        right_symbol_address += right_index

                    machine_conditions_manager.carry_out_condition(
                        condition=condition,
                        val_a=left_value,
                        address_b=right_symbol_address,
                        right_index_address=right_index_address,
                    )
                #number [?] variable
                else:
                    machine_conditions_manager.carry_out_condition(
                        condition=condition,
                        val_a = machine_condition_values[0],
                        address_b=right_symbol_address
                    )

    left_is_var = False
    right_is_var = False

def p_value_num(p):
    'value : NUM'
    p[0] = p[1]

def p_value_identifier(p):
    'value : identifier'
    p[0] = p[1]
    
def p_identifier(p):
    '''identifier : pidentifier
                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET'''
    global tab_indexes, last_read_symbols
    
    if(len(p)>2 and type(p[3])==str):
        if(get_symbol_by_name(p[3]).get_symbol_value() == -1):
            last_read_symbols.append(p[3])
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
machine_conditions_manager = MachineConditionsManager(code_generator)

symbols = []
tab_indexes = []
left_is_var = False
right_is_var = False
machine_math = False
last_read_symbols = []
machine_math_values = []

in_if_statement = False
if_passes = []
else_occured = False
machine_conditions = []

in_while_loop = []

def symbol_exists(pidentifier):
    for symbol in symbols:
        if pidentifier == symbol.get_pidentifier():
            return True
    return False

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