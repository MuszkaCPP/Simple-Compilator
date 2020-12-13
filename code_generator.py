
class CodeGenerator():
    def __init__(self):
        self.registers = ['a', 'b', 'c', 'd', 'e', 'f']
        self.current_data_offset = 0
        self.generated_code = ""
        self.last_stored_var_addr = ""

    # Math
    def add(self, var_a, var_b):
        pass
    def sub(self, var_a, var_b):
        pass
    def mul(self, var_a, var_b):
        pass
    def div(self, var_a, var_b):
        pass
    def mod(self, var_a, var_b):
        pass

    #Input
    def read_input(self):
        pass

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

    def generate_offset(self):
        self.generated_code += "RESET f\n"
        current_val = 0

        offset = self.get_data_offset()

        while(current_val != offset):
            current_val +=1
            self.generated_code += "INC f\n"

    def store_variable(self, var_a, reg):
        self.generate_number_at_reg(var_a, reg)
        self.generate_offset()
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
        self.generate_offset()

    def get_tab_elem_by_index(self,tab, index):
        #Check if index is closer to start address
        if( tab.start_address + index < tab.end_address - index):
            pass

        