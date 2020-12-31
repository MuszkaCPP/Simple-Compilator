from symbol import Symbol


class CodeGenerator():
    def __init__(self):
        self.registers = ['a', 'b', 'c', 'd', 'e', 'f']
        self.current_data_offset = 0
        self.generated_code = []
        self.address_for_machine_math = 0
        self.length_before_jump = []

    # Math
    def add(self,
            val_a=-1, address_a=-1, left_index_address=-1,
            val_b=-1, address_b=-1, right_index_address=-1
            ):

        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if(left_index_address != -1):
            self.generate_number_at_reg(address_a, 'a')
            self.generate_number_at_reg(left_index_address, 'b')

            self.append_code("LOAD c b\n")
            self.append_code("ADD a c\n")
            self.append_code("LOAD e a\n")
            
            self.append_code("RESET c\n")
            self.append_code("RESET b\n")

            #tab(a) + tab(b)
            if(right_index_address != -1):

                self.generate_number_at_reg(address_b, 'b')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD b d\n")

                self.append_code("LOAD f b\n")

                self.append_code("ADD e f\n")

            #tab(b) + variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_b, 'b')

                self.append_code("LOAD c b\n")
                self.append_code("ADD e c\n")

            #tab(a) + value
            elif(val_b != -1):
                self.generate_number_at_reg(val_b, 'b')
                self.append_code("ADD e b\n")

        elif(address_a != -1):
            #variable + variable
            if(address_b != -1):
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.append_code("LOAD c b\n")
                self.append_code("LOAD d a\n")
                self.append_code("ADD d c\n")

                self.append_code("RESET e\n")
                self.append_code("ADD e d\n")

            #variable + number
            else:
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(val_b, 'b')
                self.append_code("LOAD c a\n")
                self.append_code("ADD c b\n")

                self.append_code("RESET e\n")
                self.append_code("ADD e c\n")

    def sub(self,
            val_a=-1, address_a=-1, left_index_address=-1,
            val_b=-1, address_b=-1, right_index_address=-1
            ):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if(left_index_address != -1):
            self.generate_number_at_reg(address_a, 'a')
            self.generate_number_at_reg(left_index_address, 'b')

            self.append_code("LOAD c b\n")
            self.append_code("ADD a c\n")
            self.append_code("LOAD e a\n")
            
            self.append_code("RESET c\n")
            self.append_code("RESET b\n")

            #tab(a) - tab(b)
            if(right_index_address != -1):

                self.generate_number_at_reg(address_b, 'b')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD b d\n")

                self.append_code("LOAD f b\n")

                self.append_code("SUB e f\n")

            #tab(a) - variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_b, 'b')

                self.append_code("LOAD c b\n")
                self.append_code("SUB e c\n")

            #tab(a) - value
            elif(val_b != -1):
                self.generate_number_at_reg(val_b, 'b')
                self.append_code("SUB e b\n")

        elif(val_a != -1):
            # number - tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(val_a, 'a')

                self.generate_number_at_reg(address_b, 'b')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD d b\n")

                self.append_code("RESET c\n")

                self.append_code("ADD e a\n")
                self.append_code("LOAD c d\n")

                self.append_code("SUB e c\n")


            # number - variable
            else:
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.append_code("LOAD c b\n")
                self.append_code("SUB a c\n")
                
                self.append_code("RESET e\n")
                self.append_code("ADD e a\n")

        elif(address_a != -1):
            #variable - tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(address_a, 'a')

                self.generate_number_at_reg(address_b, 'b')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD d b\n")

                self.append_code("RESET c\n")

                self.append_code("LOAD e a\n")
                self.append_code("LOAD c d\n")

                self.append_code("SUB e c\n")


            #variable - variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(address_b, 'b')
                self.append_code("LOAD c b\n")
                self.append_code("LOAD d a\n")
                self.append_code("SUB d c\n")

                self.append_code("RESET e\n")
                self.append_code("ADD e d\n")

            #variable - number
            else:
                self.generate_number_at_reg(address_a, 'a')
                self.generate_number_at_reg(val_b, 'b')
                self.append_code("LOAD c a\n")
                self.append_code("SUB c b\n")
                
                self.append_code("RESET e\n")
                self.append_code("ADD e c\n")


    def mul(self,
            val_a=-1, address_a=-1, left_index_address=-1,
            val_b=-1, address_b=-1, right_index_address=-1
            ):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if(left_index_address != -1):
            self.generate_number_at_reg(address_a, 'a')
            self.generate_number_at_reg(left_index_address, 'b')

            self.append_code("LOAD c b\n")
            self.append_code("ADD a c\n")
            self.append_code("LOAD e a\n")
            self.append_code("RESET a\n")
            self.append_code("ADD a e\n")
            
            self.append_code("RESET c\n")
            self.append_code("RESET b\n")

            #tab(a) * tab(b)
            if(right_index_address != -1):

                self.generate_number_at_reg(address_b, 'b')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD b d\n")

                self.append_code("LOAD f b\n")
                self.append_code("RESET b\n")
                self.append_code("ADD b f\n")


            #tab(b) * variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_b, 'b')

                self.append_code("LOAD c b\n")
                self.append_code("RESET b\n")
                self.append_code("ADD b c\n")

            #tab(a) * value
            elif(val_b != -1):
                self.generate_number_at_reg(val_b, 'b')

        elif(address_a != -1):
            #variable * variable
            if(address_b != -1):
                self.append_code("RESET c\n")
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")
            #variable * number
            else:
                self.append_code("RESET c\n")
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")
                self.generate_number_at_reg(val_b, 'b')

        self.carry_out_multiplication_algorithm('a','b','e')

    def carry_out_multiplication_algorithm(self, reg_1, reg_2, reg_result):
        self.append_code("RESET " + str(reg_result) + "\n")
        self.append_code("JODD " + reg_2 + " 2\n")
        self.append_code("JUMP 2\n")
        self.append_code("ADD " + reg_result + " " + reg_1 + "\n")
        self.append_code("SHL " + reg_1 + "\n")
        self.append_code("SHR " + reg_2 + "\n")
        self.append_code("JZERO " + reg_2 + " 2\n")
        self.append_code("JUMP -6\n")
                
    def div(self,
            val_a=-1, address_a=-1, left_index_address=-1,
            val_b=-1, address_b=-1, right_index_address=-1
            ):

        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if(left_index_address != -1):
            self.generate_number_at_reg(address_a, 'f')
            self.generate_number_at_reg(left_index_address, 'b')

            self.append_code("LOAD c b\n")
            self.append_code("ADD f c\n")
            self.append_code("LOAD a f\n")
            
            self.append_code("RESET c\n")
            self.append_code("RESET b\n")
            self.append_code("RESET f\n")

            #tab(a) / tab(b)
            if(right_index_address != -1):

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            #tab(a) / variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")

            #tab(a) / value
            elif(val_b != -1):
                self.generate_number_at_reg(val_b, 'b')

        elif(val_a != -1):
            # number / tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(val_a, 'a')

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            # number / variable
            else:
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")

        elif(address_a != -1):
            #variable / tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            #variable / variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")
            #variable / number
            else:
                if(val_b == 0):
                    self.append_code("RESET e\n")
                else:
                    self.generate_number_at_reg(address_a, 'f')
                    self.append_code("LOAD a f\n")
                    self.generate_number_at_reg(val_b, 'b')

        self.carry_out_division_algorithm('a','b','c','d','e')             

    
    def carry_out_division_algorithm(self, reg_1, reg_2, quotient, counter, reg_tmp):
        self.append_code("RESET " + str(quotient) + "\n")
        self.append_code("RESET " + str(counter) + "\n")
        self.append_code("RESET " + str(reg_tmp) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 26\n")
        self.append_code("JZERO " + str(reg_2) + " 25\n")

        self.append_code("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")
        self.append_code("INC " + str(reg_1)+ "\n")
        self.append_code("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.append_code("JZERO " + str(reg_1)+ " 5\n")
        self.append_code("ADD " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.append_code("INC " + str(counter)+ "\n")
        self.append_code("SHL " + str(reg_2)+ "\n")
        self.append_code("JUMP -5\n")

        self.append_code("ADD " + str(reg_1)+ " " + str(reg_tmp)+ "\n")
        self.append_code("SHR " + str(reg_2)+ "\n")
        
        self.append_code("RESET " + str(reg_tmp)+ "\n")
        self.append_code("ADD " + str(reg_tmp)+ " " + str(reg_1)+ "\n")

        self.append_code("INC " + str(reg_tmp)+ "\n")
        self.append_code("SUB " + str(reg_tmp)+ " " + str(reg_2)+ "\n")
        self.append_code("JZERO " + str(reg_tmp)+ " 5\n")
        self.append_code("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.append_code("SHL " + str(quotient)+ "\n")
        self.append_code("INC " + str(quotient)+ "\n")
        self.append_code("JUMP 2\n")
        self.append_code("SHL " + str(quotient)+ "\n")

        self.append_code("SHR " + str(reg_2)+ "\n")

        self.append_code("DEC " + str(counter)+ "\n")
        self.append_code("JZERO " + str(counter)+ " 2\n")
        self.append_code("JUMP -13\n")

        self.append_code("RESET e\n")
        self.append_code("ADD e " + str(quotient) + "\n")
                
    
    def mod(self,
            val_a=-1, address_a=-1, left_index_address=-1,
            val_b=-1, address_b=-1, right_index_address=-1
            ):

        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if(left_index_address != -1):
            self.generate_number_at_reg(address_a, 'f')
            self.generate_number_at_reg(left_index_address, 'b')

            self.append_code("LOAD c b\n")
            self.append_code("ADD f c\n")
            self.append_code("LOAD a f\n")
            
            self.append_code("RESET c\n")
            self.append_code("RESET b\n")
            self.append_code("RESET f\n")

            #tab(a) % tab(b)
            if(right_index_address != -1):

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            #tab(a) % variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")

            #tab(a) % value
            elif(val_b != -1):
                self.generate_number_at_reg(val_b, 'b')

        elif(val_a != -1):
            # number % tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(val_a, 'a')

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            # number % variable
            else:
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")

        elif(address_a != -1):
            #variable % tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            #variable % variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")
            #variable % number
            else:
                if(val_b == 0):
                    self.append_code("RESET e\n")
                else:
                    self.generate_number_at_reg(address_a, 'f')
                    self.append_code("LOAD a f\n")
                    self.generate_number_at_reg(val_b, 'b')

        self.carry_out_modulo_algorithm('a','b','c','d','e')    

    def carry_out_modulo_algorithm(self, reg_1, reg_2, quotient, counter, reg_tmp):
        self.append_code("RESET " + str(quotient) + "\n")
        self.append_code("RESET " + str(counter) + "\n")
        self.append_code("RESET " + str(reg_tmp) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 31\n")
        self.append_code("JZERO " + str(reg_2) + " 30\n")

        self.append_code("DEC " + str(reg_1) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 30\n")

        self.append_code("INC " + str(reg_1) + "\n")

        self.append_code("ADD " + str(reg_tmp) + " " + str(reg_1) + "\n")
        self.append_code("INC " + str(reg_1)+ "\n")
        self.append_code("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.append_code("JZERO " + str(reg_1)+ " 5\n")
        self.append_code("ADD " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.append_code("INC " + str(counter)+ "\n")
        self.append_code("SHL " + str(reg_2)+ "\n")
        self.append_code("JUMP -5\n")

        self.append_code("ADD " + str(reg_1)+ " " + str(reg_tmp)+ "\n")
        self.append_code("SHR " + str(reg_2)+ "\n")
        
        self.append_code("JZERO " + str(counter) + "19\n")

        self.append_code("RESET " + str(reg_tmp)+ "\n")
        self.append_code("ADD " + str(reg_tmp)+ " " + str(reg_1)+ "\n")

        self.append_code("INC " + str(reg_tmp)+ "\n")
        self.append_code("SUB " + str(reg_tmp)+ " " + str(reg_2)+ "\n")
        self.append_code("JZERO " + str(reg_tmp)+ " 5\n")
        self.append_code("SUB " + str(reg_1)+ " " + str(reg_2)+ "\n")
        self.append_code("SHL " + str(quotient)+ "\n")
        self.append_code("INC " + str(quotient)+ "\n")
        self.append_code("JUMP 2\n")
        self.append_code("SHL " + str(quotient)+ "\n")

        self.append_code("SHR " + str(reg_2)+ "\n")

        self.append_code("DEC " + str(counter)+ "\n")
        self.append_code("JZERO " + str(counter)+ " 2\n")
        self.append_code("JUMP -13\n")
        self.append_code("JUMP 4\n")
        self.append_code("RESET " + str(reg_1) + "\n")
        self.append_code("JUMP 2\n")
        self.append_code("INC " + str(reg_1) + "\n")

        self.append_code("RESET e \n")
        self.append_code("ADD e " + str(reg_1) + "\n")

    #Conditions ------------------------------------------------------------
    def check_condition(self,
            val_a=-1, address_a=-1, left_index_address=-1,
            val_b=-1, address_b=-1, right_index_address=-1,
            condition=""
            ):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")

        if(left_index_address != -1):
            self.generate_number_at_reg(address_a, 'f')
            self.generate_number_at_reg(left_index_address, 'b')

            self.append_code("LOAD c b\n")
            self.append_code("ADD f c\n")
            self.append_code("LOAD a f\n")
            
            self.append_code("RESET c\n")
            self.append_code("RESET b\n")
            self.append_code("RESET f\n")

            #tab(a) ? tab(b)
            if(right_index_address != -1):

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            #tab(a) ? variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")

            #tab(a) ? value
            elif(val_b != -1):
                self.generate_number_at_reg(val_b, 'b')

        elif(val_a != -1):
            # number ? tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(val_a, 'a')

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")

            # number ? variable
            else:
                self.generate_number_at_reg(val_a, 'a')
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")
        elif(address_a != -1):
            #variable % tab(a)
            if(right_index_address != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")

                self.generate_number_at_reg(address_b, 'f')
                self.generate_number_at_reg(right_index_address, 'c')

                self.append_code("LOAD d c\n")
                self.append_code("ADD f d\n")
                self.append_code("LOAD b f\n")
            #variable ? variable
            elif(address_b != -1):
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.append_code("RESET f\n")
                self.generate_number_at_reg(address_b, 'f')
                self.append_code("LOAD b f\n")
            #variable ? number
            else:
                self.generate_number_at_reg(address_a, 'f')
                self.append_code("LOAD a f\n")
                self.generate_number_at_reg(val_b, 'b')
        
        if(condition=="="):
            self.check_registers_equality('a', 'b')
        elif(condition=="!="):
            self.check_registers_inequality('a', 'b')
        elif(condition=="<"):
            self.check_registers_lower_than('a', 'b')
        elif(condition==">"):
            self.check_registers_lower_than('b', 'a')
        elif(condition=="<="):
            self.check_registers_lower_equals('a', 'b')
        elif(condition==">="):
            self.check_registers_lower_equals('b', 'a')
    
    def replace_jump_for_condition(self):
        current_code_length = len(self.generated_code)
        length_before_jump = self.length_before_jump.pop()
        code_length_increase = current_code_length - length_before_jump
        jump_value = code_length_increase + 1

        self.generated_code[length_before_jump-1] = "JUMP " + str(jump_value) + "\n"

    def check_registers_equality(self, reg_1, reg_2):
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 3\n") #--> if b>a JUMP

        self.append_code("DEC " + str(reg_1) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 2\n") #--> JUMP if True

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    def check_registers_inequality(self, reg_1, reg_2):
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 3\n") #--> if b>a JUMP

        self.append_code("DEC " + str(reg_1) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 2\n") 
        self.append_code("JUMP 2\n") #--> JUMP if True

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    def check_registers_lower_than(self, reg_1, reg_2):
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 2\n") #--> if b>a JUMP

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    def check_registers_lower_equals(self, reg_1, reg_2):
        self.append_code("INC " + str(reg_1) + "\n")
        self.append_code("SUB " + str(reg_1) + " " + str(reg_2) + "\n")
        self.append_code("JZERO " + str(reg_1) + " 4\n") #--> if b>a JUMP

        self.append_code("DEC " + str(reg_1) + "\n")

        self.append_code("JZERO " + str(reg_1) + " 2\n") #--> JUMP if True

        self.append_code(" \n")
        self.length_before_jump.append(len(self.generated_code))

    #-----------------------------------------------------------------------


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

    def generate_number_at_reg(self, val_a, reg):
        self.append_code("RESET " + str(reg) + "\n")
        bin_var = bin(val_a)[2:]
        first_digit = bin_var[0]
        bin_var = bin(val_a)[3:]

        if first_digit == '1':
            self.append_code("INC " + str(reg) + "\n")
        else:
            return
        
        if len(bin_var)==0:
            return

        for digit in bin_var:
            if digit == '1':
                self.append_code("SHL " + str(reg) + "\n")
                self.append_code("INC " + str(reg) + "\n")
            else:
                self.append_code("SHL " + str(reg) + "\n")

    def generate_offset(self, reg):
        self.append_code("RESET " + str(reg) + "\n")

        offset = self.get_data_offset()
        self.generate_number_at_reg(offset, reg)

    def store_number(self, val_a, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_offset('f')
        self.append_code("STORE " + str(reg) + " f\n")

    def store_value_at_address(self, val_a, address, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_number_at_reg(address, 'f')
        self.append_code("STORE " + str(reg) + " f\n")

    def store_value_from_reg_at_address(self, address, reg):
        self.generate_number_at_reg(address, 'a')
        self.append_code("STORE " + str(reg) + " a\n")
    
    def store_from_address_to_address(self, address_a, address_b, _print=False):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(address_b, 'b')
        self.append_code("LOAD c a\n")
        self.append_code("STORE c b\n")
         
        if(_print):
            self.append_code("PUT b\n")

    def store_unknown_value_from_adress_to_address(self, address_a, tab_start_address):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_start_address, 'b')
        self.append_code("LOAD c a\n")
        self.append_code("ADD b c\n")
        self.append_code("GET b\n")

    def print_value_by_unknown_index(self, address_a, tab_start):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_start, 'b')
        self.append_code("LOAD c a\n")
        self.append_code("ADD b c\n")
        self.append_code("PUT b\n")

    def store_unknown_value_by_unknown_index(self, address_a, tab_address, index_address):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET f\n")
        self.generate_number_at_reg(address_a, 'a')
        self.generate_number_at_reg(tab_address, 'b')
        self.generate_number_at_reg(index_address, 'c')
        self.append_code("LOAD f c\n")
        self.append_code("ADD b f\n")
        self.append_code("LOAD d a\n")
        self.append_code("STORE d b\n")

    def store_value_at_unknown_index(self, val_a, tab_address, index_address):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET f\n")
        self.generate_number_at_reg(val_a, 'a')
        self.generate_number_at_reg(tab_address, 'b')
        self.generate_number_at_reg(index_address, 'c')
        self.append_code("LOAD f c\n")
        self.append_code("ADD b f\n")
        self.append_code("STORE a b\n")

    def store_unknown_tab_with_unknown_indexes(self, tab_a_address, index_a, tab_b_address, index_b):
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")
        self.append_code("RESET d\n")
        self.append_code("RESET e\n")
        self.append_code("RESET f\n")
        self.generate_number_at_reg(tab_a_address, 'a')
        self.generate_number_at_reg(index_a, 'b')
        self.append_code("LOAD f b\n")
        self.append_code("ADD a f\n")
        self.append_code("LOAD e a\n")
        self.generate_number_at_reg(tab_b_address, 'c')
        self.generate_number_at_reg(index_b, 'd')
        self.append_code("LOAD f d\n")
        self.append_code("ADD c f\n")
        self.append_code("STORE e c\n")

    def store_from_reg_to_unknown_index(self, reg, tab_address, index_address):
        #Value in reg e!
        self.append_code("RESET a\n")
        self.append_code("RESET b\n")
        self.append_code("RESET c\n")

        self.generate_number_at_reg(tab_address, 'a')
        self.generate_number_at_reg(index_address, 'b')

        self.append_code("LOAD c b\n")

        self.append_code("ADD a c\n")

        self.append_code("STORE e a\n")


    def get_generated_code(self):
        self.generated_code.append("HALT")
        return self.generated_code

    def generate_value_from_adress_at_register(self, reg, address, _print=False):
        self.generate_number_at_reg(address, reg)

        if(_print):
            self.append_code("PUT " + str(reg) +"\n")

    def print_value_from_register(self, val_a, reg):
        self.generate_number_at_reg(val_a, reg)
        self.generate_offset('f')

    def read_from_reg(self, address, reg):
        self.generate_number_at_reg(address, reg)
        self.append_code("GET " + str(reg) + "\n")

