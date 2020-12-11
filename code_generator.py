
class CodeGenerator():
    def __init__(self):
        self.registers = ['a', 'b', 'c', 'd', 'e', 'f']
        self.current_data_offset = 0
        self.generated_code = ""

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
    
    def get_value_by_adress(self):
        pass

    def generate_offset(self):
        self.generated_code += "RESET f\n"
        current_val = 0

        offset = self.get_data_offset()

        while(current_val != offset):
            current_val +=1
            self.generated_code += "INC f\n"

    def store_variable(self, var_a, reg):
        self.generated_code += "RESET a\n"
        current_val = 0

        while(current_val != var_a):
            current_val +=1
            self.generated_code += "INC a\n"
        
        self.generate_offset()
        self.generated_code += "STORE " + str(reg) + " f\n"

    def get_generated_code(self):
        self.generated_code+="HALT"
        return self.generated_code

