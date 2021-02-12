import sys
from symbol import Symbol

import ply.lex as lex
import ply.yacc as yacc

from assignment_manager import AssignmentManager
from code_generator import CodeGenerator
from machine_conditions_manager import MachineConditionsManager
from machine_controller import MachineController
from machine_math_manager import MachineMathManager

tokens = (
    "READ",
    "WRITE",
    "DECLARE",
    "BEGIN",
    "END",
    "NUM",
    "pidentifier",
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "MOD",
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

precedence = (("left", "ADD", "SUB"), ("left", "MUL", "DIV", "MOD"))

states = (("comment", "exclusive"),)

# Marks
t_ASSIGNMENT = r"\:="
t_COLON = r"[:]"
t_SEMICOLON = r"[;]"
t_LEFT_BRACKET = r"[(]"
t_RIGHT_BRACKET = r"[)]"
t_COMMA = r"[,]"

# Math operators
t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_MOD = r"\%"

# Comparisons
t_NOT_EQUALS = r"!="
t_EQUALS = r"="
t_LOWER = r"<"
t_GREATER = r">"
t_LEQ = r"<="
t_GEQ = r">="

# ignore
t_ignore_RUBBISH = r"[ \t\n]+"


def t_unknown_symbol(t):
    r"[a-z|A-Z]+[0-9]+ | [0-9]+[a-z|A-Z]+"
    throw_unknown_symbol_error(t)


# Comment
def t_comment(t):
    r"\["
    t.lexer.begin("comment")


def t_comment_error(t):
    t.lexer.skip(1)


def t_comment_end(t):
    r"\]"
    t.lexer.begin("INITIAL")


# Number, pidentifier
def t_NUM(t):
    r"[0-9]+"
    t.value = int(t.value)
    return t


def t_pidentifier(t):
    r"[_a-z]+"
    t.value = str(t.value)
    return t


# IF, ELSE, THEN, ENDIF
t_IF = r"IF"
t_THEN = r"THEN"
t_ENDIF = r"ENDIF"
t_ELSE = r"ELSE"

# WHILE, DO, ENDWHILE
t_WHILE = r"WHILE"
t_DO = r"DO"
t_ENDWHILE = r"ENDWHILE"

# REPEAT, UNTIL
t_REPEAT = r"REPEAT"
t_UNTIL = r"UNTIL"

# FOR, FROM, TO, DOWNTO, ENDFOR
t_FOR = r"FOR"
t_FROM = r"FROM"
t_TO = r"TO"
t_ENDFOR = r"ENDFOR"
t_DOWNTO = r"DOWNTO"

# DECLARE, BEGIN, END, READ, WRITE
t_DECLARE = r"DECLARE"
t_BEGIN = r"BEGIN"
t_END = r"END"
t_READ = r"READ"
t_WRITE = r"WRITE"


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


def p_program(p):
    """program : DECLARE declarations BEGIN commands END
               | BEGIN commands END"""


def p_declarations_muliple(p):
    """declarations : declarations COMMA pidentifier
                    | declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET"""

    if symbol_exists(p[3]):
        throw_redeclare_error(p[3])
    if len(p) == 4:
        symbol = Symbol(p[3], code_generator.get_data_offset())
    else:
        if p[5] > p[7]:
            throw_wrong_tab_bounds(p[5], p[7])

        symbol = Symbol(
            p[3], code_generator.get_data_offset(), True, p[5], p[7])
        code_generator.increase_data_offset(symbol.get_tab_length() - 1)
    symbols.append(symbol)


def p_declarations_single_var(p):
    "declarations : pidentifier"

    if symbol_exists(p[1]):
        throw_redeclare_error(p[1])
    p[0] = p[1]

    symbol = Symbol(p[1], code_generator.get_data_offset())
    symbols.append(symbol)


def p_declarations_single_tab(p):
    "declarations : pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET"
    if symbol_exists(p[1]):
        throw_redeclare_error(p[1])
    if p[3] > p[5]:
        throw_wrong_tab_bounds(p[3], p[5])

    p[0] = p[1]
    symbol = Symbol(p[1], code_generator.get_data_offset(), True, p[3], p[5])
    symbols.append(symbol)
    code_generator.increase_data_offset(symbol.get_tab_length() - 1)


def p_commands(p):
    """commands : commands command
                | command"""


def p_command_read(p):
    "command : READ identifier SEMICOLON"

    global tab_indexes, last_read_symbols, if_passes

    if len(if_passes) > 1 and not if_passes[-2]:
        return

    if in_if_statement and not if_passes[-1]:
        return

    symbol = get_symbol_by_name(p[2])
    if symbol.is_tab:
        index = tab_indexes.pop()
        if index == -1:
            # READ tab(a)
            code_generator.store_unknown_value_from_adress_to_address(
                index_address=get_symbol_address(last_read_symbols.pop()),
                tab_start_address=symbol.get_address(),
                tab_offset=symbol.get_tab_offset(),
            )
        else:
            code_generator.read_from_reg(
                get_symbol_by_name(p[2]).get_real_tab_index_address(index), "f"
            )
            symbol.set_tab_symbol_value_at_index(-1, index)
    else:
        code_generator.read_from_reg(get_symbol_address(p[2]), "f")
        symbol.set_value(-1)


def p_command_assignment(p):
    "command : identifier ASSIGNMENT expression SEMICOLON"

    global tab_indexes, left_is_var, right_is_var, machine_math_manager, machine_values, machine_math, last_read_symbols, if_passes

    if (
        symbol_exists(p[3])
        and get_symbol_by_name(p[3]).is_defined is not True
        and not get_symbol_by_name(p[3]).is_tab
    ):
        throw_using_undefined_error(p[3])

    if (
        symbol_exists(p[1])
        and get_symbol_by_name(p[1]).is_tab
        and len(tab_indexes) == 0
    ):
        throw_wrong_symbol_usage_error(p[1])

    if symbol_exists(p[1]) and get_symbol_by_name(p[1]).is_iterator is True:
        throw_iterator_modifying_error(p[1])

    if len(if_passes) > 1 and not if_passes[-2]:
        return

    if in_if_statement and not if_passes[-1]:
        return

    # Machine math
    if p[3] == "+" or p[3] == "-" or p[3] == "*" or p[3] == "/" or p[3] == "%":

        left_symbol_address_flag, left_value_flag = -1, -1
        right_symbol_address_flag, right_value_flag = -1, -1
        operation = p[3]

        if left_is_var:
            left_symbol_address_flag = 0
            if right_is_var:
                right_symbol_address_flag = 0
            else:
                right_value_flag = 0
        else:
            left_value_flag = 0
            if right_is_var:
                right_symbol_address_flag = 0
            else:
                right_value_flag = 0

        pass_stacks_to_machine_controller()

        machine_controller.prepare_values_for_machine_task(
            task="math_operation",
            task_value=operation,
            left_symbol_address=left_symbol_address_flag,
            left_value=left_value_flag,
            right_symbol_address=right_symbol_address_flag,
            right_value=right_value_flag,
        )

        update_stack_values()

        left_side_symbol = get_symbol_by_name(p[1])

        if left_side_symbol.is_tab:
            index = tab_indexes[0]
            tab_indexes = tab_indexes[1:]
            if index == -1:
                index_address = get_symbol_by_name(
                    last_read_symbols[0]).get_address()
                last_read_symbols = last_read_symbols[1:]

                code_generator.store_from_reg_to_unknown_index(
                    reg="e",
                    tab_address=left_side_symbol.get_address(),
                    index_address=index_address,
                    tab_offset=left_side_symbol.get_tab_offset(),
                )
            else:
                left_side_symbol.set_tab_symbol_value_at_index(-1, index)
                code_generator.store_value_from_reg_at_address(
                    address=left_side_symbol.get_real_tab_index_address(index), reg="e"
                )
        else:
            left_side_symbol.set_value(-1)
            code_generator.store_value_from_reg_at_address(
                address=left_side_symbol.get_address(), reg="e"
            )

        left_is_var = False
        right_is_var = False
        machine_math = False
        return

    if p[2] == ":=":
        left_is_var = False
        right_is_var = False

        if get_symbol_by_name(p[1]) is not None:
            left_is_var = True
        if get_symbol_by_name(p[3]) is not None:
            right_is_var = True

        machine_values.append(p[1])
        machine_values.append(p[3])

        left_symbol_address_flag, left_value_flag = -1, -1
        right_symbol_address_flag, right_value_flag = -1, -1

        if left_is_var:
            left_symbol_address_flag = 0
            if right_is_var:
                right_symbol_address_flag = 0
            else:
                right_value_flag = 0
        else:
            left_value_flag = 0
            if right_is_var:
                right_symbol_address_flag = 0
            else:
                right_value_flag = 0

        pass_stacks_to_machine_controller()

        machine_controller.prepare_values_for_machine_task(
            task="assignment",
            left_symbol_address=left_symbol_address_flag,
            left_value=left_value_flag,
            right_symbol_address=right_symbol_address_flag,
            right_value=right_value_flag,
        )

        update_stack_values()


def p_command_for_down_to(p):
    "command : FOR  for_occured  pidentifier  get_pidentifier FROM  value first_value DOWNTO  value second_value DO do_occured commands  ENDFOR"
    global machine_conditions, symbols

    code_generator.replace_jump_for_condition(pop=True, _for=True)

    for symbol in reversed(symbols):
        if symbol.is_iterator:
            symbols.remove(symbol)
            break

    in_for_loop.pop()


def p_command_for_from_to(p):
    "command : FOR  for_occured  pidentifier  get_pidentifier FROM  value first_value TO  value second_value DO do_occured commands  ENDFOR"

    global machine_conditions, symbols

    code_generator.replace_jump_for_condition(pop=True, _for=True)

    for symbol in reversed(symbols):
        if symbol.is_iterator:
            symbols.remove(symbol)
            break

    in_for_loop.pop()


def p_command_first_value(p):
    "first_value :"

    global for_loop_borders

    value = p.stack[-1].value

    if symbol_exists(value):
        if get_symbol_by_name(value).is_defined is not True:
            throw_using_undefined_error(value)
        if get_symbol_by_name(value).is_iterator is True and len(in_for_loop) == 2:
            throw_wrong_symbol_usage_error(value)

    for_loop_borders.append(value)


def p_command_second_value(p):
    "second_value :"

    global for_loop_borders

    value = p.stack[-1].value

    if symbol_exists(value):
        if get_symbol_by_name(value).is_defined is not True:
            throw_using_undefined_error(value)
        if get_symbol_by_name(value).is_iterator is True and len(in_for_loop) == 2:
            throw_wrong_symbol_usage_error(value)

    for_loop_borders.append(value)


def p_command_get_pidentifier(p):
    "get_pidentifier :"

    global symbols

    pidentifier = p.stack[-1].value

    iterator = Symbol(
        pidentifier, code_generator.get_data_offset(), is_iterator=True)
    iterator.set_value(-1)
    symbols.append(iterator)


def p_command_do_occured(p):
    "do_occured :"

    global last_read_symbols, tab_indexes, symbols, for_loop_borders, machine_values
    left_is_var, right_is_var = False, False
    left_symbol, right_symbol = None, None

    iterator = symbols[-1]
    iterator_address = iterator.get_address()

    loop_type = ""

    if p.stack[-4].value == "TO":
        loop_type = "for_from_to"
    else:
        loop_type = "for_from_downto"

    if symbol_exists(for_loop_borders[1]):
        right_is_var = True
        right_symbol = get_symbol_by_name(for_loop_borders[1])
    if symbol_exists(for_loop_borders[0]):
        left_is_var = True
        left_symbol = get_symbol_by_name(for_loop_borders[0])

    machine_values = for_loop_borders
    left_symbol_address_flag, left_value_flag = -1, -1
    right_symbol_address_flag, right_value_flag = -1, -1

    if left_is_var:
        left_symbol_address_flag = 0
        if right_is_var:
            right_symbol_address_flag = 0
        else:
            right_value_flag = 0
    else:
        left_value_flag = 0
        if right_is_var:
            right_symbol_address_flag = 0
        else:
            right_value_flag = 0

    pass_stacks_to_machine_controller()

    machine_controller.prepare_values_for_machine_task(
        task="for_loop",
        loop_type=loop_type,
        iterator_address=iterator_address,
        left_symbol_address=left_symbol_address_flag,
        left_value=left_value_flag,
        right_symbol_address=right_symbol_address_flag,
        right_value=right_value_flag,
    )

    update_stack_values()

    for_loop_borders = for_loop_borders[2:]


def p_command_for_occured(p):
    "for_occured :"

    global in_for_loop

    in_for_loop.append(True)


def p_command_repeat_until(p):
    "command : REPEAT repeat_occured  commands  UNTIL  condition SEMICOLON"

    global in_repeat_loop

    if machine_conditions.pop():
        code_generator.replace_jump_for_condition(_repeat=True)

    in_repeat_loop.pop()


def p_command_repeat_occured(p):
    "repeat_occured :"

    global in_repeat_loop

    in_repeat_loop.append(True)

    code_generator.save_current_code_length()


def p_command_while(p):
    "command : WHILE while_occured condition  DO  commands  ENDWHILE"

    global in_while_loop

    if machine_conditions.pop():
        code_generator.replace_jump_for_condition(_while=True)

    in_while_loop.pop()


def p_command_while_occured(p):
    "while_occured :"

    global in_while_loop

    in_while_loop.append(True)

    code_generator.save_current_code_length()


def p_command_if_else(p):
    "command : IF if_occured condition THEN commands ELSE else_occured commands ENDIF"

    global in_if_statement, machine_conditions, else_occured

    if machine_conditions.pop():
        code_generator.replace_jump_for_condition()
        return

    if_passes.pop()

    if len(if_passes) == 0:
        in_if_statement = False


def p_command_else_occured(p):
    "else_occured :"
    global if_passes, else_occured

    if machine_conditions[-1]:
        code_generator.replace_jump_for_condition(pop=False)
        return

    if if_passes.pop() is True:
        if_passes.append(False)
    else:
        if_passes.append(True)


def p_command_if_endif(p):
    "command : IF if_occured condition  THEN  commands  ENDIF"

    global in_if_statement, machine_conditions

    if machine_conditions.pop():
        code_generator.replace_jump_for_condition()
        return

    if_passes.pop()

    if len(if_passes) == 0:
        in_if_statement = False


def p_if_occured(p):
    "if_occured :"

    global in_if_statement
    in_if_statement = True


def p_command_write(p):
    "command : WRITE value SEMICOLON"

    if (
        symbol_exists(p[2])
        and not get_symbol_by_name(p[2]).is_tab
        and get_symbol_by_name(p[2]).is_defined is not True
    ):
        throw_using_undefined_error(p[2])

    global tab_indexes, last_read_symbols, in_if_statement, if_passes

    if len(if_passes) > 1 and not if_passes[-2]:
        return

    elif in_if_statement and not if_passes[-1]:
        return

    if symbol_exists(p[2]):
        symbol = get_symbol_by_name(p[2])
        if symbol.is_tab:
            index = tab_indexes.pop()
            if index == -1:
                code_generator.print_value_by_unknown_index(
                    left_symbol_address=get_symbol_address(
                        last_read_symbols.pop()),
                    tab_start=symbol.get_address(),
                    tab_offset=symbol.get_tab_offset(),
                )
            else:
                code_generator.generate_value_from_adress_at_register(
                    "f", symbol.get_real_tab_index_address(index), True
                )
        else:
            code_generator.generate_value_from_adress_at_register(
                "f", get_symbol_address(p[2]), True
            )
    else:
        code_generator.store_number(p[2], "a")
        code_generator.generate_value_from_adress_at_register(
            "f", code_generator.current_data_offset, True
        )


def p_expression_val(p):
    "expression : value"
    p[0] = p[1]


def p_expression_math(p):
    """expression : value ADD value
                  | value SUB value
                  | value MUL value
                  | value DIV value
                  | value MOD value"""

    global tab_indexes, left_is_var, right_is_var, machine_math_manager, machine_values, in_while_loop, in_repeat_loop
    machine_math = False
    left_is_var = False
    right_is_var = False
    left_index = 0
    right_index = 0

    # Machine maths
    if symbol_exists(p[3]):
        right_symbol = get_symbol_by_name(p[3])
        right_is_var = True
        value = 0

        if right_symbol.is_tab:
            right_index = tab_indexes.pop()
            if (
                right_index != -1
                and right_symbol.get_tab_symbol_value(right_index) == -1
            ):
                machine_math = True
        else:
            value = right_symbol.get_symbol_value()

        if (
            value == -1
            or right_index == -1
            or in_while_loop[-1]
            or in_repeat_loop[-1]
            or in_for_loop[-1]
        ):
            machine_math = True

    if symbol_exists(p[1]):
        left_is_var = True
        left_symbol = get_symbol_by_name(p[1])
        value = 0

        if left_symbol.is_tab:
            left_index = tab_indexes.pop()
            if left_index != -1 and left_symbol.get_tab_symbol_value(left_index) == -1:
                machine_math = True
        else:
            value = left_symbol.get_symbol_value()

        if (
            value == -1
            or left_index == -1
            or in_while_loop[-1]
            or in_repeat_loop[-1]
            or in_for_loop[-1]
        ):
            machine_math = True

    if is_tab(p[1]):
        tab_indexes.append(left_index)
    if is_tab(p[3]):
        tab_indexes.append(right_index)

    # Compiler maths
    if not machine_math and (symbol_exists(p[1]) or symbol_exists(p[3])):
        if is_tab(p[3]):
            p[3] = get_symbol_by_name(
                p[3]).get_tab_symbol_value(tab_indexes.pop())
        elif symbol_exists(p[3]):
            p[3] = get_symbol_by_name(p[3]).get_symbol_value()

        if is_tab(p[1]):
            p[1] = get_symbol_by_name(
                p[1]).get_tab_symbol_value(tab_indexes.pop())
        elif symbol_exists(p[1]):
            p[1] = get_symbol_by_name(p[1]).get_symbol_value()

    if machine_math:
        machine_values.append(p[1])
        machine_values.append(p[3])

    if p[2] == "+":
        if machine_math:
            p[0] = "+"
        else:
            p[0] = p[1] + p[3]
    elif p[2] == "-":
        if machine_math:
            p[0] = "-"
        else:
            p[0] = p[1] - p[3]
    elif p[2] == "*":
        if machine_math:
            p[0] = "*"
        else:
            p[0] = p[1] * p[3]
    elif p[2] == "/":
        if machine_math:
            p[0] = "/"
        else:
            if p[3] == 0:
                p[0] = 0
            else:
                p[0] = p[1] // p[3]
    elif p[2] == "%":
        if machine_math:
            p[0] = "%"
        else:
            if p[3] == 0:
                p[0] = 0
            else:
                p[0] = p[1] % p[3]


def p_condition(p):
    """condition : value EQUALS value
                 | value NOT_EQUALS value
                 | value LOWER value
                 | value GREATER value
                 | value LEQ value
                 | value GEQ value"""

    global in_if_statement, if_passes, machine_conditions_manager, tab_indexes, machine_conditions, in_while_loop, machine_controller, machine_values
    left_is_var = False
    right_is_var = False
    machine_condition = False
    condition = ""
    left_index = 0
    right_index = 0

    # Machine conditions
    if symbol_exists(p[3]):
        right_is_var = True
        value = 0
        if is_tab(p[3]):
            right_index = tab_indexes.pop()
            if (
                right_index != -1
                and get_symbol_by_name(p[3]).get_tab_symbol_value(right_index) == -1
            ):
                machine_condition = True
        else:
            value = get_symbol_by_name(p[3]).get_symbol_value()

        if (
            value == -1
            or right_index == -1
            or in_while_loop[-1]
            or in_repeat_loop[-1]
            or in_for_loop[-1]
        ):
            machine_condition = True

    if symbol_exists(p[1]):
        left_is_var = True
        value = 0
        if is_tab(p[1]):
            left_index = tab_indexes.pop()
            if (
                left_index != -1
                and get_symbol_by_name(p[1]).get_tab_symbol_value(left_index) == -1
            ):
                machine_condition = True
        else:
            value = get_symbol_by_name(p[1]).get_symbol_value()

        if (
            value == -1
            or left_index == -1
            or in_while_loop[-1]
            or in_repeat_loop[-1]
            or in_for_loop[-1]
        ):
            machine_condition = True

    if is_tab(p[1]):
        tab_indexes.append(left_index)
    if is_tab(p[3]):
        tab_indexes.append(right_index)

    if not machine_condition and (symbol_exists(p[1]) or symbol_exists(p[3])):
        if in_while_loop[-1] or in_repeat_loop[-1] or in_for_loop[-1]:
            if is_tab(p[3]):
                p[3] = get_symbol_by_name(
                    p[3]).get_tab_index_address(tab_indexes.pop())
            elif symbol_exists(p[3]):
                p[3] = get_symbol_by_name(p[3]).get_address()

            if is_tab(p[1]):
                p[1] = get_symbol_by_name(
                    p[1]).get_tab_index_address(tab_indexes.pop())
            elif symbol_exists(p[1]):
                p[1] = get_symbol_by_name(p[1]).get_address()

        else:
            if is_tab(p[3]):
                p[3] = get_symbol_by_name(
                    p[3]).get_tab_symbol_value(tab_indexes.pop())
            elif symbol_exists(p[3]):
                p[3] = get_symbol_by_name(p[3]).get_symbol_value()

            if is_tab(p[1]):
                p[1] = get_symbol_by_name(
                    p[1]).get_tab_symbol_value(tab_indexes.pop())
            elif symbol_exists(p[1]):
                p[1] = get_symbol_by_name(p[1]).get_symbol_value()

    if machine_condition:
        machine_conditions.append(True)
        machine_values.append(p[1])
        machine_values.append(p[3])
    else:
        machine_conditions.append(False)

    if p[2] == "=":
        condition = "="
        if not machine_condition and not in_while_loop[-1] and not in_repeat_loop[-1]:
            if p[1] == p[3]:
                p[0] = True
            else:
                p[0] = False
    elif p[2] == "!=":
        condition = "!="
        if not machine_condition and not in_while_loop[-1] and not in_repeat_loop[-1]:
            if p[1] != p[3]:
                p[0] = True
            else:
                p[0] = False
    elif p[2] == "<":
        condition = "<"
        if not machine_condition and not in_while_loop[-1] and not in_repeat_loop[-1]:
            if p[1] < p[3]:
                p[0] = True
            else:
                p[0] = False
    elif p[2] == ">":
        condition = ">"
        if not machine_condition and not in_while_loop[-1] and not in_repeat_loop[-1]:
            if p[1] > p[3]:
                p[0] = True
            else:
                p[0] = False
    elif p[2] == "<=":
        condition = "<="
        if not machine_condition and not in_while_loop[-1] and not in_repeat_loop[-1]:
            if p[1] <= p[3]:
                p[0] = True
            else:
                p[0] = False
    elif p[2] == ">=":
        condition = ">="
        if not machine_condition and not in_while_loop[-1] and not in_repeat_loop[-1]:
            if p[1] >= p[3]:
                p[0] = True
            else:
                p[0] = False

    if in_if_statement and machine_condition:
        if_passes.append(True)
    elif in_if_statement and not machine_condition:
        if p[0] == False:
            if_passes.append(False)
        elif p[0] == True:
            if len(if_passes) > 0 and if_passes[-1] == False:
                if_passes.append(False)
            else:
                if_passes.append(True)
        return

    if not machine_condition and (
        in_while_loop[-1] or in_repeat_loop[-1] or in_for_loop[-1]
    ):
        if left_is_var:
            if right_is_var:
                machine_conditions_manager.carry_out_condition(
                    condition=condition,
                    left_symbol_address=p[1],
                    right_symbol_address=p[3],
                )
            else:
                machine_conditions_manager.carry_out_condition(
                    condition=condition, left_symbol_address=p[1], right_value=p[3]
                )
        else:
            if right_is_var:
                machine_conditions_manager.carry_out_condition(
                    condition=condition, left_value=p[1], right_symbol_address=p[3]
                )
            else:
                machine_conditions_manager.carry_out_condition(
                    condition=condition, left_value=p[1], right_value=p[3]
                )
        machine_conditions[-1] = True

    elif machine_condition:
        left_symbol_address_flag, left_value_flag = -1, -1
        right_symbol_address_flag, right_value_flag = -1, -1

        if left_is_var:
            left_symbol_address_flag = 0
            if right_is_var:
                right_symbol_address_flag = 0
            else:
                right_value_flag = 0
        else:
            left_value_flag = 0
            if right_is_var:
                right_symbol_address_flag = 0
            else:
                right_value_flag = 0

        pass_stacks_to_machine_controller()

        machine_controller.prepare_values_for_machine_task(
            task="condition",
            task_value=condition,
            left_symbol_address=left_symbol_address_flag,
            left_value=left_value_flag,
            right_symbol_address=right_symbol_address_flag,
            right_value=right_value_flag,
        )

        update_stack_values()

    left_is_var = False
    right_is_var = False


def p_value_num(p):
    "value : NUM"
    p[0] = p[1]


def p_value_identifier(p):
    "value : identifier"

    if not symbol_exists(p[1]):
        throw_undeclared_error(p[1])

    p[0] = p[1]


def p_identifier(p):
    """identifier : pidentifier
                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET"""
    global tab_indexes, last_read_symbols, for_loop_borders, in_for_loop

    if not symbol_exists(p[1]):
        throw_undeclared_error(p[1])

    if len(p) > 2 and type(p[3]) == str:
        if not symbol_exists(p[3]):
            throw_undeclared_error(p[3])
        if get_symbol_by_name(p[3]).is_defined is not True:
            throw_using_undefined_error(p[3])
        if not get_symbol_by_name(p[1]).is_tab:
            throw_wrong_symbol_usage_error(p[1])

        if get_symbol_by_name(p[3]).get_symbol_value() == -1:
            last_read_symbols.append(p[3])
        index = get_symbol_by_name(p[3]).get_symbol_value()
        tab_indexes.append(index)

    p[0] = p[1]


def p_identifier_tab(p):
    "identifier : pidentifier LEFT_BRACKET NUM RIGHT_BRACKET"
    global tab_indexes

    if not symbol_exists(p[1]):
        throw_undeclared_error(p[1])
    if symbol_exists(p[1]) and not get_symbol_by_name(p[1]).is_tab:
        throw_wrong_symbol_usage_error(p[1])

    p[0] = p[1]
    tab_indexes.append(p[3])


# Errors
def throw_undeclared_error(value):
    print("[Error] Symbol undeclared! [" + str(value) + "]")
    exit(-1)


def throw_redeclare_error(value):
    print("[Error] Symbol redeclared! [" + str(value) + "]")
    exit(-1)


def throw_using_undefined_error(value):
    print("[Error] Using undefined symbol! [" + str(value) + "]")
    exit(-1)


def throw_unknown_symbol_error(t):
    print("[Error] Wrong symbol name! [" + str(t.value) + "]")
    exit(-1)


def throw_wrong_symbol_usage_error(sign):
    print("[Error] Wrong symbol usage! [" + str(sign) + "]")
    exit(-1)


def throw_wrong_sign_error(t):
    print("[Error] Wrong sign! [" + str(t) + "]")
    exit(-1)


def throw_wrong_tab_bounds(left_bound, right_bound):
    print(
        "[Error] Wrong tab bounds! [" +
        str(left_bound) + " : " + str(right_bound) + "]"
    )
    exit(-1)


def throw_iterator_modifying_error(value):
    print("[Error] Iterator is being modified! [" + str(value) + "]")
    exit(-1)


def p_error(p):
    print("[Syntax Error] " + str(p.value))
    exit(-1)


lexer = lex.lex()
parser = yacc.yacc(start="program")
code_generator = CodeGenerator()

symbols = []
tab_indexes = []
left_is_var = False
right_is_var = False
machine_math = False
last_read_symbols = []
machine_values = []

in_if_statement = False
if_passes = []
else_occured = False
machine_conditions = []

in_while_loop = [False]
in_repeat_loop = [False]
in_for_loop = [False]

for_loop_borders = []

machine_math_manager = MachineMathManager(code_generator)
machine_conditions_manager = MachineConditionsManager(code_generator)
assignment_manager = AssignmentManager(code_generator)
machine_controller = MachineController(
    machine_math_manager=machine_math_manager,
    machine_conditions_manager=machine_conditions_manager,
    assignment_manager=assignment_manager,
    code_generator=code_generator,
)


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
        print(
            str(symbol.pidentifier)
            + "  "
            + str(symbol.get_address())
            + "  "
            + str(symbol.get_symbol_value())
        )


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
    symbol = get_symbol_by_name(pidentifier)
    if symbol.is_tab:
        return symbol.get_address() + offset
    else:
        return symbol.get_address()


def pass_stacks_to_machine_controller():
    global tab_indexes, last_read_symbols, machine_values, machine_controller

    machine_controller.update_stack_values(
        tab_indexes=tab_indexes,
        last_read_symbols=last_read_symbols,
        machine_values=machine_values,
        symbols=symbols,
    )


def update_stack_values():
    global tab_indexes, last_read_symbols, machine_values, machine_controller

    tab_indexes, last_read_symbols, machine_values = machine_controller.get_stacks()
