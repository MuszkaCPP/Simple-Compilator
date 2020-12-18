from symbol import Symbol



class CodeGenerator():
    def __init__(self):
        self.registers = ['a', 'b', 'c', 'd', 'e', 'f']
        self.current_data_offset = 0
        self.generated_code = ""
        self.address_for_machine_math = 0

    # Math
    def add(self, var_a = -1, address_a = -1, var_b = -1, address_b = -1):
        if(var_a != -1):
            # number + variable
            if(address_b != -1):
                self.generate_number_at_reg(var_a, 'a')
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
                self.generate_number_at_reg(var_b, 'b')
                self.generated_code += "LOAD c a\n"
                self.generated_code += "ADD a c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE a b\n"

    def sub(self, var_a = -1, address_a = -1, var_b = -1, address_b = -1):
        if(var_a != -1):
            # number + variable
            if(address_b != -1):
                self.generate_number_at_reg(var_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code += "LOAD c b\n"
                self.generated_code += "SUB a c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE a b\n"

        elif(address_a != -1):
            #variable + variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.generated_code += "LOAD c b\n"
                self.generated_code += "LOAD d a\n"
                self.generated_code += "SUB d c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE d b\n"
            #variable + number
            else:
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(var_b, 'b')
                self.generated_code += "LOAD c a\n"
                self.generated_code += "SUB a c\n"
                self.generate_number_at_reg(self.address_for_machine_math, 'b')
                self.generated_code += "STORE a b\n"

    def mul(self, var_a = -1, address_a = -1, var_b = -1, address_b = -1):
        #result in register c
        if(var_a != -1):
            # number * variable
            if(address_b != -1):
                self.generated_code += "RESET c\n"
                self.generate_number_at_reg(var_a, 'a')
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
                self.generate_number_at_reg(var_b, 'b')

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
                
    def div(self, var_a = -1, address_a = -1, var_b = -1, address_b = -1):
        pass
    def mod(self, var_a = -1, address_a = -1, var_b = -1, address_b = -1):
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

    def generate_number_at_reg(self, var_a, reg):
        self.generated_code += "RESET " + str(reg) + "\n"
        bin_var = bin(var_a)[2:]
        first_digit = bin_var[0]
        bin_var = bin(var_a)[3:]

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

    def store_variable(self, var_a, reg):
        self.generate_number_at_reg(var_a, reg)
        self.generate_offset('f')
        self.generated_code += "STORE " + str(reg) + " f\n"

    def store_value_at_address(self, var_a, address, reg):
        self.generate_number_at_reg(var_a, reg)
        self.generate_number_at_reg(address, 'f')
        self.generated_code += "STORE " + str(reg) + " f\n"

        self.last_stored_var_addr = self.current_data_offset

    def store_value_from_reg_at_address(self, address, reg):
        self.generate_number_at_reg(address, 'a')
        self.generated_code += "LOAD c " + str(reg) + "\n"
        self.generated_code += "STORE c a\n"
    
    def store_from_address_to_address(self, address_a, address_b, _print=False):
        self.generated_code += "RESET a\n"
        self.generated_code += "RESET b\n"
        self.generated_code += "RESET c\n"
        self.generate_number_at_reg(address_a, 'a')
        # self.generated_code += "PUT a\n"
        self.generate_number_at_reg(address_b, 'b')
        self.generated_code += "LOAD c a\n"
        self.generated_code += "STORE c b\n"
        # self.generated_code += "PUT b\n"
         
        if(_print):
            self.generated_code += "PUT b\n"
            pass


    def get_generated_code(self):
        self.generated_code+="HALT"
        return self.generated_code

    def print_value_from_adress(self, reg, address, _print=False):
        self.generate_number_at_reg(address, reg)

        if(_print):
            self.generated_code += "PUT " + str(reg) +"\n"

    def print_value_from_register(self, var_a, reg):
        self.generate_number_at_reg(var_a, reg)
        self.generate_offset('f')

    def read_from_reg(self, address, reg):
        self.generate_number_at_reg(address, reg)
        self.generated_code += "GET " + str(reg) + "\n"
