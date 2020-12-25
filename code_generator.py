from symbol import Symbol


class CodeGenerator():
    def __init__(self):
        self.registers = ['a', 'b', 'c', 'd', 'e', 'f']
        self.current_data_offset = 0
        self.generated_code = []
        self.address_for_machine_math = 0
        self.condition_end_index = 0

    # Math
    def add(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        if(val_a != -1):
            # number + variable
            if(address_b != -1):
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code.append("LOAD c b\n")
                self.generated_code.append("ADD a c\n")
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code.append("STORE a b\n")

        elif(address_a != -1):
            #variable + variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code.append("LOAD c b\n")
                self.generated_code.append("LOAD d a\n")
                self.generated_code.append("ADD d c\n")
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code.append("STORE d b\n")
            #variable + number
            else:
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(val_b, 'b')
                self.generated_code.append("LOAD c a\n")
                self.generated_code.append("ADD a c\n")
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code.append("STORE a b\n")

    def sub(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        if(val_a != -1):
            # number - variable
            if(address_b != -1):
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code.append("LOAD c b\n")
                self.generated_code.append("SUB a c\n")
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code.append("STORE a b\n")

        elif(address_a != -1):
            #variable - variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code.append("LOAD c b\n")
                self.generated_code.append("LOAD d a\n")
                self.generated_code.append("SUB d c\n")
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code.append("STORE d b\n")
            #variable - number
            else:
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(val_b, 'b')
                self.generated_code.append("LOAD c a\n")
                self.generated_code.append("SUB a c\n")
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code.append("STORE a b\n")

    def mul(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        #result in register c
        if(val_a != -1):
            # number * variable
            if(address_b != -1):
                self.generated_code.append("RESET c\n")
                self.generate_number_at_reg(val_a, 'a')
                self.generated_code.append("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.generated_code.append("LOAD b f\n")

        elif(address_a != -1):
            #variable * variable
            if(address_b != -1):
                self.generated_code.append("RESET c\n")
                self.generate_number_at_reg(address_a, 'f')
                self.generated_code.append("LOAD a f\n")
                self.generated_code.append("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.generated_code.append("LOAD b f\n")
            #variable * number
            else:
                self.generated_code.append("RESET c\n")
                self.generate_number_at_reg(address_a, 'f')
                self.generated_code.append("LOAD a f\n")
                self.generated_code.append("RESET f\n")
                self.generate_number_at_reg(val_b, 'b')

        self.carry_out_multiplication_algorithm('a','b','c')

    def carry_out_multiplication_algorithm(self, reg_1, reg_2, reg_result):
        self.generated_code.append("JODD " + reg_2 + " 2\n")
        self.generated_code.append("JUMP 2\n")
        self.generated_code.append("ADD " + reg_result + " " + reg_1 + "\n")
        self.generated_code.append("SHL " + reg_1 + "\n")
        self.generated_code.append("SHR " + reg_2 + "\n")
        self.generated_code.append("JZERO " + reg_2 + " 2\n")
        self.generated_code.append("JUMP -6\n")
        self.generate_number_at_reg(self.address_for_machine_math, 'd')
        self.generated_code.append("STORE " + reg_result + " d\n")
                
    def div(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generated_code.append("RESET d\n")
        self.generated_code.append("RESET e\n")
        if(val_a != -1):

            # number / variable
            if(address_b != -1):
                if(val_a == 0):
                    self.generated_code.append("RESET a\n")
                    self.generate_number_at_reg(self.address_for_machine_math, 'f')
                    self.generated_code.append("STORE a f\n")
                else:
                    self.generate_number_at_reg(val_a, 'a')
                    self.generated_code.append("RESET f\n")
                    self.generate_number_at_reg(address_b, 'f')
                    self.generated_code.append("LOAD b f\n")
                    self.carry_out_division_algorithm('a','b','c','d','e')

        elif(address_a != -1):
            #variable / variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.generated_code.append("LOAD a f\n")
                self.generated_code.append("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.generated_code.append("LOAD b f\n")
                self.carry_out_division_algorithm('a','b','c','d','e')
            #variable / number
            else:
                if(val_b == 0):
                    self.generated_code.append("RESET a\n")
                    self.generate_number_at_reg(self.address_for_machine_math, 'f')
                    self.generated_code.append("STORE a f\n") 
                else:
                    self.generate_number_at_reg(address_a, 'f')
                    self.generated_code.append("LOAD a f\n")
                    self.generate_number_at_reg(val_b, 'b')
                    self.carry_out_division_algorithm('a','b','c','d','e')
    
    def carry_out_division_algorithm(self, reg_1, reg_2, quotient, counter, reg_tmp):
        self.generated_code.append("JZERO " + str(reg_1) + " 26\n")
        self.generated_code.append("JZERO " + str(reg_2) + " 25\n")

        self.generated_code.append("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")
        self.generated_code.append("INC " + str(reg_1)+ "\n")
        self.generated_code.append("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("JZERO " + str(reg_1)+ " 5\n")
        self.generated_code.append("ADD " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("INC " + str(counter)+ "\n")
        self.generated_code.append("SHL " + str(reg_2)+ "\n")
        self.generated_code.append("JUMP -5\n")

        self.generated_code.append("ADD " + str(reg_1)+ " " + str(reg_tmp)+ "\n")
        self.generated_code.append("SHR " + str(reg_2)+ "\n")
        
        self.generated_code.append("RESET " + str(reg_tmp)+ "\n")
        self.generated_code.append("ADD " + str(reg_tmp)+ " " + str(reg_1)+ "\n")

        self.generated_code.append("INC " + str(reg_tmp)+ "\n")
        self.generated_code.append("SUB " + str(reg_tmp)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("JZERO " + str(reg_tmp)+ " 5\n")
        self.generated_code.append("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("SHL " + str(quotient)+ "\n")
        self.generated_code.append("INC " + str(quotient)+ "\n")
        self.generated_code.append("JUMP 2\n")
        self.generated_code.append("SHL " + str(quotient)+ "\n")

        self.generated_code.append("SHR " + str(reg_2)+ "\n")

        self.generated_code.append("DEC " + str(counter)+ "\n")
        self.generated_code.append("JZERO " + str(counter)+ " 2\n")
        self.generated_code.append("JUMP -13\n")
        self.generate_number_at_reg(self.address_for_machine_math, 'f')
        self.generated_code.append("STORE " + str(quotient)+ " f\n")
                
    
    def mod(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generated_code.append("RESET d\n")
        self.generated_code.append("RESET e\n")

        if(val_a != -1):

            # number % variable
            if(address_b != -1):
                if(val_a == 0):
                    self.generated_code.append("RESET a\n")
                    self.generate_number_at_reg(self.address_for_machine_math, 'f')
                    self.generated_code.append("STORE a f\n")
                else:
                    self.generate_number_at_reg(val_a, 'a')
                    self.generated_code.append("RESET f\n")
                    self.generate_number_at_reg(address_b, 'f')
                    self.generated_code.append("LOAD b f\n")
                    self.carry_out_modulo_algorithm('a','b','c','d','e')

        elif(address_a != -1):
            #variable % variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.generated_code.append("LOAD a f\n")
                self.generated_code.append("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.generated_code.append("LOAD b f\n")
                self.carry_out_modulo_algorithm('a','b','c','d','e')
            #variable % number
            else:
                if(val_b == 0):
                    self.generated_code.append("RESET a\n")
                    self.generate_number_at_reg(self.address_for_machine_math, 'f')
                    self.generated_code.append("STORE a f\n")
                else:
                    self.generate_number_at_reg(address_a, 'f')
                    self.generated_code.append("LOAD a f\n")
                    self.generate_number_at_reg(val_b, 'b')
                    self.carry_out_modulo_algorithm('a','b','c','d','e')

    def carry_out_modulo_algorithm(self, reg_1, reg_2, quotient, counter, reg_tmp):
        self.generate_number_at_reg(self.address_for_machine_math, 'f')

        self.generated_code.append("JZERO " + str(reg_1) + " 31\n")
        self.generated_code.append("JZERO " + str(reg_2) + " 30\n")

        self.generated_code.append("DEC " + str(reg_1) + "\n")
        self.generated_code.append("JZERO " + str(reg_1) + " 30\n")

        self.generated_code.append("INC " + str(reg_1) + "\n")

        self.generated_code.append("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")
        self.generated_code.append("INC " + str(reg_1)+ "\n")
        self.generated_code.append("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("JZERO " + str(reg_1)+ " 5\n")
        self.generated_code.append("ADD " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("INC " + str(counter)+ "\n")
        self.generated_code.append("SHL " + str(reg_2)+ "\n")
        self.generated_code.append("JUMP -5\n")

        self.generated_code.append("ADD " + str(reg_1)+ " " + str(reg_tmp)+ "\n")
        self.generated_code.append("SHR " + str(reg_2)+ "\n")
        
        self.generated_code.append("JZERO " + str(counter) + "19\n")

        self.generated_code.append("RESET " + str(reg_tmp)+ "\n")
        self.generated_code.append("ADD " + str(reg_tmp)+ " " + str(reg_1)+ "\n")

        self.generated_code.append("INC " + str(reg_tmp)+ "\n")
        self.generated_code.append("SUB " + str(reg_tmp)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("JZERO " + str(reg_tmp)+ " 5\n")
        self.generated_code.append("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.generated_code.append("SHL " + str(quotient)+ "\n")
        self.generated_code.append("INC " + str(quotient)+ "\n")
        self.generated_code.append("JUMP 2\n")
        self.generated_code.append("SHL " + str(quotient)+ "\n")

        self.generated_code.append("SHR " + str(reg_2)+ "\n")

        self.generated_code.append("DEC " + str(counter)+ "\n")
        self.generated_code.append("JZERO " + str(counter)+ " 2\n")
        self.generated_code.append("JUMP -13\n")
        self.generated_code.append("JUMP 4\n")
        self.generated_code.append("RESET " + str(reg_1) + "\n")
        self.generated_code.append("JUMP 2\n")
        self.generated_code.append("INC " + str(reg_1) + "\n")
        self.generated_code.append("STORE " + str(reg_1) + " f\n")

    def set_address_for_machine(self, address):
        self.address_for_machine_math = address

    def get_address_for_machine(self):
        return self.address_for_machine_math

    def get_data_offset(self):
        self.current_data_offset += 1 
        return self.current_data_offset

    def increase_data_offset(self, offset):
        self.current_data_offset += offset

    def generate_number_at_reg(self, val_a, reg):
        self.generated_code.append("RESET " + str(reg) + "\n")
        bin_var = bin(val_a)[2:]
        first_digit = bin_var[0]
        bin_var = bin(val_a)[3:]

        if first_digit == '1':
            self.generated_code.append("INC " + str(reg) + "\n")
        else:
            return
        
        if len(bin_var)==0:
            return

        for digit in bin_var:
            if digit == '1':
                self.generated_code.append("SHL " + str(reg) + "\n")
                self.generated_code.append("INC " + str(reg) + "\n")
            else:
                self.generated_code.append("SHL " + str(reg) + "\n")

    def generate_offset(self, reg):
        self.generated_code.append("RESET " + str(reg) + "\n")

        offset = self.get_data_offset()
        self.generate_number_at_reg(offset, reg)

    def store_number(self, val_a, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_offset('f')
        self.generated_code.append("STORE " + str(reg) + " f\n")

    def store_value_at_address(self, val_a, address, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_number_at_reg(address, 'f')
        self.generated_code.append("STORE " + str(reg) + " f\n")

    def store_value_from_reg_at_address(self, address, reg):
        self.generate_number_at_reg(address, 'a')
        self.generated_code.append("LOAD c " + str(reg) + "\n")
        self.generated_code.append("STORE c a\n")
    
    def store_from_address_to_address(self, address_a, address_b, _print=False):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(address_b, 'b')
        self.generated_code.append("LOAD c a\n")
        self.generated_code.append("STORE c b\n")
         
        if(_print):
            self.generated_code.append("PUT b\n")

    def store_unknown_value_from_adress_to_address(self, address_a, tab_start_address):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_start_address, 'b')
        self.generated_code.append("LOAD c a\n")
        self.generated_code.append("ADD b c\n")
        self.generated_code.append("GET b\n")

    def print_value_by_unknown_index(self, address_a, tab_start):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_start, 'b')
        self.generated_code.append("LOAD c a\n")
        self.generated_code.append("ADD b c\n")
        self.generated_code.append("PUT b\n")

    def store_unknown_value_by_unknown_index(self, address_a, tab_address, index_address):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generated_code.append("RESET d\n")
        self.generated_code.append("RESET f\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_address, 'b')
        self.generate_number_at_reg(index_address, 'c')
        self.generated_code.append("LOAD f c\n")
        self.generated_code.append("ADD b f\n")
        self.generated_code.append("LOAD d a\n")
        self.generated_code.append("STORE d b\n")

    def store_value_at_unknown_index(self, val_a, tab_address, index_address):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generated_code.append("RESET d\n")
        self.generated_code.append("RESET f\n")
        self.generate_number_at_reg(val_a, 'a')
        self.generate_number_at_reg(tab_address, 'b')
        self.generate_number_at_reg(index_address, 'c')
        self.generated_code.append("LOAD f c\n")
        self.generated_code.append("ADD b f\n")
        self.generated_code.append("STORE a b\n")

    def store_unknown_tab_with_unknown_indexes(self, tab_a_address, index_a, tab_b_address, index_b):
        self.generated_code.append("RESET a\n")
        self.generated_code.append("RESET b\n")
        self.generated_code.append("RESET c\n")
        self.generated_code.append("RESET d\n")
        self.generated_code.append("RESET e\n")
        self.generated_code.append("RESET f\n")
        self.generate_number_at_reg(tab_a_address, 'a')
        self.generate_number_at_reg(index_a, 'b')
        self.generated_code.append("LOAD f b\n")
        self.generated_code.append("ADD a f\n")
        self.generated_code.append("LOAD e a\n")
        self.generate_number_at_reg(tab_b_address, 'c')
        self.generate_number_at_reg(index_b, 'd')
        self.generated_code.append("LOAD f d\n")
        self.generated_code.append("ADD c f\n")
        self.generated_code.append("STORE e c\n")

    def get_generated_code(self):
        self.generated_code+="HALT"
        return self.generated_code

    def generate_value_from_adress_at_register(self, reg, address, _print=False):
        self.generate_number_at_reg(address, reg)

        if(_print):
            self.generated_code.append("PUT " + str(reg) +"\n")

    def print_value_from_register(self, val_a, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_offset('f')

    def read_from_reg(self, address, reg):
        self.generate_number_at_reg(address, reg)
        self.generated_code.append("GET " + str(reg) + "\n")

