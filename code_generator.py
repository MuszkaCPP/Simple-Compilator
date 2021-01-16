from symbol import Symbol
from register_manager import RegisterManager


class CodeGenerator:
    def __init__(self):
        self.current_data_offset = 0
        self.generated_code = []
        self.address_for_machine_math = 0
        self.length_before_jump = []
        self.register_manager = RegisterManager()

    # Math
    def process_math_operation(
        self,
        operation="",
        left_value=-1,
        left_symbol_address=-1,
        left_index_address=-1,
        left_offset=-1,
        right_value=-1,
        right_symbol_address=-1,
        right_index_address=-1,
        right_offset=-1,
    ):

        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if left_index_address != -1:
            self.generate_number_at_reg(left_symbol_address, "f")
            self.generate_number_at_reg(left_index_address, "b")
            self.generate_number_at_reg(left_offset, "d")

            self.append_code("LOAD c b\n")
            self.append_code("ADD f c\n")
            self.append_code("SUB f d\n")
            self.append_code("LOAD a f\n")

            self.append_code("RESET b\n")
            self.append_code("RESET c\n")
            self.append_code("RESET d\n")
            self.append_code("RESET f\n")

            # tab(a) ? tab(b)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # tab(a) ? variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")

            # tab(a) ? value
            elif right_value != -1:
                self.generate_number_at_reg(right_value, "b")

        elif left_value != -1:
            self.generate_number_at_reg(left_value, "a")
            # number ? tab(a)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # number ? variable
            else:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")

        elif left_symbol_address != -1:
            self.generate_number_at_reg(left_symbol_address, "f")
            self.append_code("LOAD a f\n")
            self.append_code("RESET f\n")

            # variable ? tab(a)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # variable ? variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")
            # variable ? value
            else:
                if right_value == 0:
                    self.append_code("RESET e\n")
                else:
                    self.generate_number_at_reg(right_value, "b")

        if operation == "+":
            self.carry_out_addition("a", "b")
        elif operation == "-":
            self.carry_out_substraction("a", "b")
        elif operation == "*":
            self.carry_out_multiplication_algorithm("a", "b", "e")
        elif operation == "/":
            self.carry_out_division_algorithm("a", "b", "c", "d", "e")
        elif operation == "%":
            self.carry_out_modulo_algorithm("a", "b", "c", "d", "e")

    def carry_out_addition(self, reg_1, reg_2):
        self.append_code("RESET e\n")
        self.append_code("ADD e a\n")
        self.append_code("ADD e b\n")

    def carry_out_substraction(self, reg_1, reg_2):
        self.append_code("RESET e\n")
        self.append_code("ADD e a\n")
        self.append_code("SUB e b\n")

    def carry_out_multiplication_algorithm(self, reg_1, reg_2, reg_result):
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")
        self.append_code("ADD e " + str(reg_1) + "\n")
        self.append_code("ADD f " + str(reg_2) + "\n")
        self.append_code("INC e\n")
        self.append_code("SUB e f\n")
        self.append_code("JZERO e 2\n")
        self.append_code("JUMP 9\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")
        self.append_code("ADD e " + str(reg_1) + "\n")
        self.append_code("ADD f " + str(reg_2) + "\n")
        self.append_code("RESET " + str(reg_1) + "\n")
        self.append_code("RESET " + str(reg_2) + "\n")
        self.append_code("ADD " + str(reg_1) + " f\n")
        self.append_code("ADD " + str(reg_2) + " e\n")

        self.append_code("RESET " + str(reg_result) + "\n")
        self.append_code("JODD " + reg_2 + " 2\n")
        self.append_code("JUMP 2\n")
        self.append_code("ADD " + reg_result + " " + reg_1 + "\n")
        self.append_code("SHL " + reg_1 + "\n")
        self.append_code("SHR " + reg_2 + "\n")
        self.append_code("JZERO " + reg_2 + " 2\n")
        self.append_code("JUMP -6\n")

    def carry_out_division_algorithm(self, reg_1, reg_2, quotient, counter, reg_tmp):
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")
        self.append_code("ADD e " + str(reg_1) + "\n")
        self.append_code("ADD f " + str(reg_2) + "\n")
        self.append_code("INC e\n")
        self.append_code("SUB e f\n")
        self.append_code("JZERO e 32\n")  # --> if b>a JUMP

        self.append_code("RESET " + str(quotient) + "\n")
        self.append_code("RESET " + str(counter) + "\n")
        self.append_code("RESET " + str(reg_tmp) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 26\n")
        self.append_code("JZERO " + str(reg_2) + " 25\n")

        self.append_code("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 5\n")
        self.append_code("ADD " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("INC " + str(counter) + "\n")
        self.append_code("SHL " + str(reg_2) + "\n")
        self.append_code("JUMP -5\n")

        self.append_code("ADD " + str(reg_1) + " " + str(reg_tmp) + "\n")
        self.append_code("SHR " + str(reg_2) + "\n")

        self.append_code("RESET " + str(reg_tmp) + "\n")
        self.append_code("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")

        self.append_code("INC " + str(reg_tmp) + "\n")
        self.append_code("SUB " + str(reg_tmp) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_tmp) + " 5\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("SHL " + str(quotient) + "\n")
        self.append_code("INC " + str(quotient) + "\n")
        self.append_code("JUMP 2\n")
        self.append_code("SHL " + str(quotient) + "\n")

        self.append_code("SHR " + str(reg_2) + "\n")

        self.append_code("DEC " + str(counter) + "\n")
        self.append_code("JZERO " + str(counter) + " 2\n")
        self.append_code("JUMP -13\n")

        self.append_code("RESET e\n")
        self.append_code("ADD e " + str(quotient) + "\n")

    def carry_out_modulo_algorithm(self, reg_1, reg_2, quotient, counter, reg_tmp):
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        self.append_code("ADD e " + str(reg_1) + "\n")
        self.append_code("ADD f " + str(reg_2) + "\n")
        self.append_code("INC e\n")
        self.append_code("SUB e f\n")
        self.append_code("JZERO e 3\n")  # --> if b>a JUMP

        self.append_code("DEC e\n")

        self.append_code("JZERO e 40\n")  # --> JUMP if True

        self.append_code("RESET " + str(quotient) + "\n")
        self.append_code("RESET " + str(counter) + "\n")
        self.append_code("RESET " + str(reg_tmp) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 31\n")
        self.append_code("JZERO " + str(reg_2) + " 30\n")

        self.append_code("DEC " + str(reg_1) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 30\n")

        self.append_code("INC " + str(reg_1) + "\n")

        self.append_code("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 5\n")
        self.append_code("ADD " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("INC " + str(counter) + "\n")
        self.append_code("SHL " + str(reg_2) + "\n")
        self.append_code("JUMP -5\n")

        self.append_code("ADD " + str(reg_1) + " " + str(reg_tmp) + "\n")
        self.append_code("SHR " + str(reg_2) + "\n")

        self.append_code("JZERO " + str(counter) + " 19\n")

        self.append_code("RESET " + str(reg_tmp) + "\n")
        self.append_code("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")

        self.append_code("INC " + str(reg_tmp) + "\n")
        self.append_code("SUB " + str(reg_tmp) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_tmp) + " 5\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("SHL " + str(quotient) + "\n")
        self.append_code("INC " + str(quotient) + "\n")
        self.append_code("JUMP 2\n")
        self.append_code("SHL " + str(quotient) + "\n")

        self.append_code("SHR " + str(reg_2) + "\n")

        self.append_code("DEC " + str(counter) + "\n")
        self.append_code("JZERO " + str(counter) + " 2\n")
        self.append_code("JUMP -13\n")
        self.append_code("JUMP 4\n")
        self.append_code("RESET " + str(reg_1) + "\n")
        self.append_code("JUMP 2\n")
        self.append_code("INC " + str(reg_1) + "\n")

        self.append_code("RESET e \n")
        self.append_code("ADD e " + str(reg_1) + "\n")

    # Conditions ------------------------------------------------------------
    def check_condition(
        self,
        condition="",
        left_value=-1,
        left_symbol_address=-1,
        left_index_address=-1,
        left_offset=-1,
        right_value=-1,
        right_symbol_address=-1,
        right_index_address=-1,
        right_offset=-1,
    ):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if left_index_address != -1:
            self.generate_number_at_reg(left_symbol_address, "f")
            self.generate_number_at_reg(left_index_address, "b")
            self.generate_number_at_reg(left_offset, "d")

            self.append_code("LOAD c b\n")
            self.append_code("ADD f c\n")
            self.append_code("SUB f d\n")
            self.append_code("LOAD a f\n")

            self.append_code("RESET b\n")
            self.append_code("RESET c\n")
            self.append_code("RESET d\n")
            self.append_code("RESET f\n")

            # tab(a) ? tab(b)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # tab(a) ? variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")

            # tab(a) ? value
            elif right_value != -1:
                self.generate_number_at_reg(right_value, "b")

        elif left_value != -1:
            self.generate_number_at_reg(left_value, "a")
            # number ? tab(a)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # number ? variable
            else:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")
        elif left_symbol_address != -1:
            self.generate_number_at_reg(left_symbol_address, "f")
            self.append_code("LOAD a f\n")
            self.append_code("RESET f\n")
            # variable ? tab(a)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")
            # variable ? variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")
            # variable ? number
            else:
                self.generate_number_at_reg(right_value, "b")

        if left_value != -1 and right_value != -1:
            self.generate_number_at_reg(left_value, "a")
            self.generate_number_at_reg(right_value, "b")

        if condition == "=":
            self.check_registers_equality("a", "b")
        elif condition == "!=":
            self.check_registers_inequality("a", "b")
        elif condition == "<":
            self.check_registers_lower_than("a", "b")
        elif condition == ">":
            self.check_registers_lower_than("b", "a")
        elif condition == "<=":
            self.check_registers_lower_equals("a", "b")
        elif condition == ">=":
            self.check_registers_lower_equals("b", "a")

    def replace_jump_for_condition(
        self, pop=True, _while=False, _repeat=False, _for=False
    ):
        length_before_jump = 0
        current_code_length = len(self.generated_code)

        if pop:
            length_before_jump = self.length_before_jump.pop()
        else:
            length_before_jump = self.length_before_jump[-1]
            self.length_before_jump[-1] += current_code_length - length_before_jump + 1

        code_length_increase = current_code_length - length_before_jump

        jump_value = code_length_increase + 1

        if not pop or _while or _for:
            jump_value += 1

        if _while or _for:
            backwards_jump = current_code_length - self.length_before_jump.pop()
            self.generated_code.append("JUMP -" + str(backwards_jump) + "\n")
        elif _repeat:
            backwards_jump = current_code_length - self.length_before_jump.pop() - 1
            self.generated_code[length_before_jump - 1] = (
                "JUMP -" + str(backwards_jump) + "\n"
            )

        if not _repeat:
            self.generated_code[length_before_jump - 1] = (
                "JUMP " + str(jump_value) + "\n"
            )

    def manage_for_loop(
        self,
        iterator_address,
        loop_type="",
        left_value=-1,
        left_symbol_address=-1,
        left_index_address=-1,
        left_offset=-1,
        right_value=-1,
        right_symbol_address=-1,
        right_index_address=-1,
        right_offset=-1,
    ):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if left_index_address != -1:
            self.generate_number_at_reg(left_symbol_address, "f")
            self.generate_number_at_reg(left_index_address, "b")
            self.generate_number_at_reg(left_offset, "d")
            self.append_code("LOAD c b\n")
            self.append_code("ADD f c\n")
            self.append_code("SUB f d\n")
            self.append_code("LOAD a f\n")

            self.append_code("RESET b\n")
            self.append_code("RESET c\n")
            self.append_code("RESET d\n")
            self.append_code("RESET f\n")

            # tab(a) ? tab(b)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # tab(a) ? variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")

            # tab(a) ? value
            elif right_value != -1:
                self.generate_number_at_reg(right_value, "b")

        elif left_value != -1:
            self.generate_number_at_reg(left_value, "a")
            # number ? tab(a)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # number ? variable
            else:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")

        elif left_symbol_address != -1:
            self.generate_number_at_reg(left_symbol_address, "f")
            self.append_code("LOAD a f\n")
            self.append_code("RESET f\n")
            # variable ? tab(a)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")
            # variable ? variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")
            # variable ? value
            else:
                self.generate_number_at_reg(right_value, "b")

        if left_value != -1 and right_value != -1:
            self.generate_number_at_reg(left_value, "a")
            self.generate_number_at_reg(right_value, "b")

        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET f\n")

        if loop_type == "for_from_to":
            self.append_code("INC a\n")
            self.append_code("INC b\n")
            self.append_code("INC b\n")
            self.generate_offset("f")
            right_value_address = self.current_data_offset

            self.append_code("STORE b f\n")
            self.generate_number_at_reg(iterator_address, "c")
            self.append_code("STORE a c\n")
            self.generate_offset("f")
            self.append_code("INC a\n")
            tmp_iterator_address = self.current_data_offset
            self.append_code("STORE a f\n")

            self.save_current_code_length()

            self.generate_number_at_reg(iterator_address, "c")
            self.append_code("RESET a\n")
            self.append_code("LOAD a c\n")
            self.generate_number_at_reg(right_value_address, "f")
            self.append_code("RESET b\n")
            self.append_code("LOAD b f\n")
            self.append_code("RESET f\n")
            self.generate_number_at_reg(tmp_iterator_address, "f")
            self.append_code("RESET e\n")
            self.append_code("LOAD e f\n")

        elif loop_type == "for_from_downto":
            self.append_code("INC a\n")
            self.append_code("INC b\n")
            self.append_code("INC b\n")
            self.generate_offset("f")
            right_value_address = self.current_data_offset

            self.append_code("STORE b f\n")
            self.generate_number_at_reg(iterator_address, "c")
            self.append_code("STORE a c\n")
            self.generate_offset("f")
            self.append_code("INC a\n")
            tmp_iterator_address = self.current_data_offset
            self.append_code("STORE a f\n")

            self.save_current_code_length()

            self.generate_number_at_reg(iterator_address, "c")
            self.append_code("RESET a\n")
            self.append_code("LOAD a c\n")
            self.generate_number_at_reg(right_value_address, "f")
            self.append_code("RESET b\n")
            self.append_code("LOAD b f\n")
            self.append_code("RESET f\n")
            self.generate_number_at_reg(tmp_iterator_address, "f")
            self.append_code("RESET e\n")
            self.append_code("LOAD e f\n")

        if loop_type == "for_from_to":
            self.append_code("RESET a\n")
            self.append_code("ADD a e\n")
            self.append_code("DEC a\n")
            self.append_code("DEC a\n")
            self.append_code("STORE a c\n")
            self.append_code("RESET d\n")
            self.append_code("ADD d e\n")
            self.append_code("INC e\n")
            self.append_code("STORE e f\n")
            self.check_registers_lower_equals("d", "b")
        elif loop_type == "for_from_downto":
            self.append_code("RESET a\n")
            self.append_code("ADD a e\n")
            self.append_code("DEC a\n")
            self.append_code("DEC a\n")
            self.append_code("STORE a c\n")
            self.append_code("RESET d\n")
            self.append_code("ADD d e\n")
            self.append_code("DEC e\n")
            self.append_code("STORE e f\n")
            self.check_registers_lower_than("b", "d", _for_loop=True)

    def save_current_code_length(self):
        self.length_before_jump.append(len(self.generated_code))

    def check_registers_equality(self, reg_1, reg_2):
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 3\n")  # --> if b>a JUMP

        self.append_code("DEC " + str(reg_1) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 2\n")  # --> JUMP if True

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    def check_registers_inequality(self, reg_1, reg_2):
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 3\n")  # --> if b>a JUMP

        self.append_code("DEC " + str(reg_1) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 2\n")
        self.append_code("JUMP 2\n")  # --> JUMP if True

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    def check_registers_lower_than(self, reg_1, reg_2, _for_loop=False):
        if _for_loop:
            self.append_code("DEC " + str(reg_2) + "\n")
            self.append_code("JZERO " + str(reg_2) + " 3\n")
            self.append_code("INC " + str(reg_2) + "\n")
            self.append_code("JUMP 8\n")
            self.append_code("INC " + str(reg_2) + "\n")
            self.append_code("SUB " + str(reg_2) + " " + str(reg_1) + "\n")
            self.append_code("JZERO " + str(reg_2) + " 3\n")  # --> if b>a JUMP

            self.append_code("DEC " + str(reg_2) + "\n")

            self.append_code("JZERO " + str(reg_2) + " 2\n")  # --> JUMP if True
            self.append_code("JUMP 4\n")

        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 2\n")  # --> if b>a JUMP

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    def check_registers_lower_equals(self, reg_1, reg_2):
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 4\n")  # --> if b>a JUMP d>=b

        self.append_code("DEC " + str(reg_1) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 2\n")  # --> JUMP if True

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    # -----------------------------------------------------------------------

    def append_code(self, code):
        self.generated_code.append(code)

    def set_address_for_machine(self, address):
        self.address_for_machine_math = address

    def get_address_for_machine(self):
        return self.address_for_machine_math

    def get_data_offset(self):
        self.current_data_offset += 1
        return self.current_data_offset

    def increase_data_offset(self, offset):
        self.current_data_offset += offset

    def generate_number_at_reg(self, left_value, reg):
        self.append_code("RESET " + str(reg) + "\n")
        bin_var = bin(left_value)[2:]
        first_digit = bin_var[0]
        bin_var = bin(left_value)[3:]

        if first_digit == "1":
            self.append_code("INC " + str(reg) + "\n")
        else:
            return

        if len(bin_var) == 0:
            return

        for digit in bin_var:
            if digit == "1":
                self.append_code("SHL " + str(reg) + "\n")
                self.append_code("INC " + str(reg) + "\n")
            else:
                self.append_code("SHL " + str(reg) + "\n")

    def generate_offset(self, reg):
        self.append_code("RESET " + str(reg) + "\n")

        offset = self.get_data_offset()
        self.generate_number_at_reg(offset, reg)

    # Store
    def store_symbol(
        self,
        left_value=-1,
        left_symbol_address=-1,
        left_index_address=-1,
        left_offset=-1,
        right_value=-1,
        right_symbol_address=-1,
        right_index_address=-1,
        right_offset=-1,
    ):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if left_index_address != -1:
            self.generate_number_at_reg(left_symbol_address, "a")
            self.generate_number_at_reg(left_index_address, "b")
            self.generate_number_at_reg(left_offset, "d")

            self.append_code("LOAD c b\n")
            self.append_code("ADD a c\n")
            self.append_code("SUB a d\n")

            self.append_code("RESET b\n")
            self.append_code("RESET c\n")
            self.append_code("RESET d\n")

            # tab(a) := tab(b)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")

            # tab(a) := variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")

            # tab(a) := value
            elif right_value != -1:
                self.generate_number_at_reg(right_value, "b")

        elif left_symbol_address != -1:
            self.generate_number_at_reg(left_symbol_address, "a")
            # variable := tab(a)
            if right_index_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.generate_number_at_reg(right_index_address, "c")
                self.generate_number_at_reg(right_offset, "e")

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("SUB f e\n")
                self.append_code("LOAD b f\n")
            # variable := variable
            elif right_symbol_address != -1:
                self.generate_number_at_reg(right_symbol_address, "f")
                self.append_code("LOAD b f\n")
            # variable := value
            else:
                self.generate_number_at_reg(right_value, "b")

        self.append_code("STORE b a\n")

    def store_number(self, left_value, reg):
        self.append_code("RESET " + reg + "\n")
        self.generate_number_at_reg(left_value, reg)
        self.generate_offset("f")
        self.append_code("STORE " + str(reg) + " f\n")

    def store_value_at_address(self, left_value, address, reg):
        self.generate_number_at_reg(left_value, reg)
        self.generate_number_at_reg(address, "f")
        self.append_code("STORE " + str(reg) + " f\n")

    def store_value_from_reg_at_address(self, address, reg):
        self.generate_number_at_reg(address, "a")
        self.append_code("STORE " + str(reg) + " a\n")

    def store_unknown_value_from_adress_to_address(
        self, index_address, tab_start_address, tab_offset
    ):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.generate_number_at_reg(index_address, "a")
        self.generate_number_at_reg(tab_start_address, "b")
        self.generate_number_at_reg(tab_offset, "d")
        self.append_code("LOAD c a\n")
        self.append_code("ADD b c\n")
        self.append_code("SUB b d\n")
        self.append_code("GET b\n")

    def print_value_by_unknown_index(self, left_symbol_address, tab_start, tab_offset):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.generate_number_at_reg(left_symbol_address, "a")
        self.generate_number_at_reg(tab_start, "b")
        self.generate_number_at_reg(tab_offset, "d")
        self.append_code("LOAD c a\n")
        self.append_code("ADD b c\n")
        self.append_code("SUB b d\n")
        self.append_code("PUT b\n")

    def store_from_reg_to_unknown_index(
        self, reg, tab_address, index_address, tab_offset
    ):
        # Value in reg e!
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")

        self.generate_number_at_reg(tab_address, "a")
        self.generate_number_at_reg(index_address, "b")
        self.generate_number_at_reg(tab_offset, "d")

        self.append_code("LOAD c b\n")
        self.append_code("ADD a c\n")
        self.append_code("SUB a d\n")

        self.append_code("STORE " + str(reg) + " a\n")

    def get_generated_code(self):
        self.generated_code.append("HALT")
        return self.generated_code

    def generate_value_from_adress_at_register(self, reg, address, _print=False):
        self.append_code("RESET " + str(reg) + "\n")
        self.generate_number_at_reg(address, reg)

        if _print:
            self.append_code("PUT " + str(reg) + "\n")

    def print_value_from_register(self, left_value, reg):
        self.append_code("RESET f\n")
        self.generate_number_at_reg(left_value, reg)
        self.generate_offset("f")

    def read_from_reg(self, address, reg):
        self.generate_number_at_reg(address, reg)
        self.append_code("GET " + str(reg) + "\n")
