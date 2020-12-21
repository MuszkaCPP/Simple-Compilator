from symbol import Symbol


class CodeGenerator():
    def __init__(self):
        self.registers = ['a', 'b', 'c', 'd', 'e', 'f']
        self.current_data_offset = 0
        self.generated_code = ""
        self.address_for_machine_math = 0

    # Math
    def add(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        if(val_a != -1):
            # number + variable
            if(address_b != -1):
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code += "LOAD c b\n"
                self.generated_code += "ADD a c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE a b\n"

        elif(address_a != -1):
            #variable + variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code += "LOAD c b\n"
                self.generated_code += "LOAD d a\n"
                self.generated_code += "ADD d c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE d b\n"
            #variable + number
            else:
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(val_b, 'b')
                self.generated_code += "LOAD c a\n"
                self.generated_code += "ADD a c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE a b\n"

    def sub(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        if(val_a != -1):
            # number - variable
            if(address_b != -1):
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code += "LOAD c b\n"
                self.generated_code += "SUB a c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE a b\n"

        elif(address_a != -1):
            #variable - variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code += "LOAD c b\n"
                self.generated_code += "LOAD d a\n"
                self.generated_code += "SUB d c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE d b\n"
            #variable - number
            else:
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(val_b, 'b')
                self.generated_code += "LOAD c a\n"
                self.generated_code += "SUB a c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE a b\n"

    def mul(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        #result in register c
        if(val_a != -1):
            # number * variable
            if(address_b != -1):
                self.generated_code += "RESET c\n"
                self.generate_number_at_reg(val_a, 'a')
                self.generated_code += "RESET f\n"
                self.generate_number_at_reg(address_b, 'f')
                self.generated_code += "LOAD b f\n"

        elif(address_a != -1):
            #variable * variable
            if(address_b != -1):
                self.generated_code += "RESET c\n"
                self.generate_number_at_reg(address_a, 'f')
                self.generated_code += "LOAD a f\n"
                self.generated_code += "RESET f\n"
                self.generate_number_at_reg(address_b, 'f')
                self.generated_code += "LOAD b f\n"
            #variable * number
            else:
                self.generated_code += "RESET c\n"
                self.generate_number_at_reg(address_a, 'f')
                self.generated_code += "LOAD a f\n"
                self.generated_code += "RESET f\n"
                self.generate_number_at_reg(val_b, 'b')

        self.carry_out_multiplication_algorithm('a','b','c')

    def carry_out_multiplication_algorithm(self, reg_1, reg_2, reg_result):
        self.generated_code += "JODD " + reg_2 + " 2\n"
        self.generated_code += "JUMP 2\n"
        self.generated_code += "ADD " + reg_result + " " + reg_1 + "\n"
        self.generated_code += "SHL " + reg_1 + "\n"
        self.generated_code += "SHR " + reg_2 + "\n"
        self.generated_code += "JZERO " + reg_2 + " 2\n"
        self.generated_code += "JUMP -6\n"
        self.generate_number_at_reg(self.address_for_machine_math, 'd')
        self.generated_code += "STORE " + reg_result + " d\n"
                
    def div(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        pass
    
    def mod(self, val_a = -1, address_a = -1, val_b = -1, address_b = -1):
        pass

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
        self.generated_code += "RESET " + str(reg) + "\n"
        bin_var = bin(val_a)[2:]
        first_digit = bin_var[0]
        bin_var = bin(val_a)[3:]

        if first_digit == '1':
            self.generated_code += "INC " + str(reg) + "\n"
        else:
            return
        
        if len(bin_var)==0:
            return

        for digit in bin_var:
            if digit == '1':
                self.generated_code += "SHL " + str(reg) + "\n"
                self.generated_code += "INC " + str(reg) + "\n"
            else:
                self.generated_code += "SHL " + str(reg) + "\n"

    def generate_offset(self, reg):
        self.generated_code += "RESET " + str(reg) + "\n"

        offset = self.get_data_offset()
        self.generate_number_at_reg(offset, reg)

    def store_number(self, val_a, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_offset('f')
        self.generated_code += "STORE " + str(reg) + " f\n"

    def store_value_at_address(self, val_a, address, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_number_at_reg(address, 'f')
        self.generated_code += "STORE " + str(reg) + " f\n"

    def store_value_from_reg_at_address(self, address, reg):
        self.generate_number_at_reg(address, 'a')
        self.generated_code += "LOAD c " + str(reg) + "\n"
        self.generated_code += "STORE c a\n"
    
    def store_from_address_to_address(self, address_a, address_b, _print=False):
        self.generated_code += "RESET a\n"
        self.generated_code += "RESET b\n"
        self.generated_code += "RESET c\n"
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(address_b, 'b')
        self.generated_code += "LOAD c a\n"
        self.generated_code += "STORE c b\n"
         
        if(_print):
            self.generated_code += "PUT b\n"

    def store_unknown_value_from_adress_to_address(self, address_a, tab_start_address):
        self.generated_code += "RESET a\n"
        self.generated_code += "RESET b\n"
        self.generated_code += "RESET c\n"
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_start_address, 'b')
        self.generated_code += "LOAD c a\n"
        self.generated_code += "ADD b c\n"
        self.generated_code += "GET b\n"

    def print_value_by_unknown_index(self, address_a, tab_start):
        self.generated_code += "RESET a\n"
        self.generated_code += "RESET b\n"
        self.generated_code += "RESET c\n"
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_start, 'b')
        self.generated_code += "LOAD c a\n"
        self.generated_code += "ADD b c\n"
        self.generated_code += "PUT b\n"

    def store_unknown_value_by_unknown_index(self, address_a, tab_address, index_address):
        self.generated_code += "RESET a\n"
        self.generated_code += "RESET b\n"
        self.generated_code += "RESET c\n"
        self.generated_code += "RESET d\n"
        self.generated_code += "RESET f\n"
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_address, 'b')
        self.generate_number_at_reg(index_address, 'c')
        self.generated_code += "LOAD f c\n"
        self.generated_code += "ADD b f\n"
        self.generated_code += "LOAD d a\n"
        self.generated_code += "STORE d b\n"

    def store_value_at_unknown_index(self, val_a, tab_address, index_address):
        self.generated_code += "RESET a\n"
        self.generated_code += "RESET b\n"
        self.generated_code += "RESET c\n"
        self.generated_code += "RESET d\n"
        self.generated_code += "RESET f\n"
        self.generate_number_at_reg(val_a, 'a')
        self.generate_number_at_reg(tab_address, 'b')
        self.generate_number_at_reg(index_address, 'c')
        self.generated_code += "LOAD f c\n"
        self.generated_code += "ADD b f\n"
        self.generated_code += "STORE a b\n"

    def store_unknown_tab_with_unknown_indexes(self, tab_a_address, index_a, tab_b_address, index_b):
        self.generated_code += "RESET a\n"
        self.generated_code += "RESET b\n"
        self.generated_code += "RESET c\n"
        self.generated_code += "RESET d\n"
        self.generated_code += "RESET e\n"
        self.generated_code += "RESET f\n"
        self.generate_number_at_reg(tab_a_address, 'a')
        self.generate_number_at_reg(index_a, 'b')
        self.generated_code += "LOAD f b\n"
        self.generated_code += "ADD a f\n"
        self.generated_code += "LOAD e a\n"
        self.generate_number_at_reg(tab_b_address, 'c')
        self.generate_number_at_reg(index_b, 'd')
        self.generated_code += "LOAD f d\n"
        self.generated_code += "ADD c f\n"
        self.generated_code += "STORE e c\n"
        
    def get_length_of_value(self, val_address, reg):
        self.generated_code += "RESET " + str(reg) + "\n"


    def get_generated_code(self):
        self.generated_code+="HALT"
        return self.generated_code

    def generate_value_from_adress_at_register(self, reg, address, _print=False):
        self.generate_number_at_reg(address, reg)

        if(_print):
            self.generated_code += "PUT " + str(reg) +"\n"

    def print_value_from_register(self, val_a, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_offset('f')

    def read_from_reg(self, address, reg):
        self.generate_number_at_reg(address, reg)
        self.generated_code += "GET " + str(reg) + "\n"
