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

            
        
    def sub(self, var_a, var_b):
        pass
    def mul(self, var_a, var_b):
        pass
    def div(self, var_a, var_b):
        pass
    def mod(self, var_a, var_b):
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

    def get_generated_code(self):
        self.generated_code+="HALT"
        return self.generated_code

    def print_value_from_adress(self, reg, address, _print="False"):
        self.generate_number_at_reg(address, reg)

        if(_print):
            self.generated_code += "PUT " + str(reg) +"\n"

    def print_value_from_register(self, var_a, reg):
        self.generate_number_at_reg(var_a, reg)
        self.generate_offset('f')

    def read_from_reg(self, address, reg):
        self.generate_number_at_reg(address, reg)
        self.generated_code += "GET " + str(reg) + "\n"

    def get_tab_elem_by_index(self,tab, index):
        #Check if index is closer to start address
        if( tab.start_address + index < tab.end_address - index):
            pass

        