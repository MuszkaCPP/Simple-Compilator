
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
    
    def get_value_by_adress(self, reg, address, print="False"):
        self.generated_code += "RESET " + str(reg) +"\n"
        address_val = 0

        while(address_val != address):
            if(address_val > 0 and address_val*2 <= address):
                address_val *= 2
                self.generated_code += "SHL " + str(reg) +"\n"
            else:
                address_val += 1
                self.generated_code += "INC " + str(reg) +"\n"
        
        if(print):
            self.generated_code += "PUT " + str(reg) +"\n"

    def generate_offset(self):
        self.generated_code += "RESET f\n"
        current_val = 0

        offset = self.get_data_offset()

        while(current_val != offset):
            current_val +=1
            self.generated_code += "INC f\n"

    def store_variable(self, var_a, reg):
        self.generated_code += "RESET " + str(reg) + "\n"
        current_val = 0

        while(current_val != var_a):
            if(current_val > 0 and current_val*2 <= var_a):
                current_val *= 2
                self.generated_code += "SHL" + str(reg) + "\n"
            else:
                current_val += 1
                self.generated_code += "INC " + str(reg) + "\n"
        
        self.generate_offset()
        self.generated_code += "STORE " + str(reg) + " f\n"
        self.last_stored_var_addr = self.current_data_offset

    def get_generated_code(self):
        self.generated_code+="HALT"
        return self.generated_code

    def store_value_at_address(self, var_a, address, reg):
        self.generated_code += "RESET a\n"
        current_val = 0

        while(current_val != var_a):
            if(current_val > 0 and current_val*2 <= var_a):
                current_val *= 2
                self.generated_code += "SHL " + str(reg) + "\n"
            else:
                current_val += 1
                self.generated_code += "INC " + str(reg) + "\n"

        self.generated_code += "RESET f\n"
        address_val = 0

        while(address_val != address):
            if(address_val > 0 and address_val*2 <= address):
                address_val *= 2
                self.generated_code += "SHL f\n"
            else:
                address_val += 1
                self.generated_code += "INC f\n"

        self.generated_code += "STORE " + str(reg) + " f\n"

    def store_tab(self,):
        pass

    def get_tab_elem_by_index(self,tab, index):
        #Check if index is closer to start address
        if( tab.start_address + index < tab.end_address - index):
            pass

        