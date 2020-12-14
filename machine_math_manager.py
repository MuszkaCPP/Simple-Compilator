
class MachineMathManager():
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def carry_out_operation(self, 
                            operation = 0,
                            var_a=0,
                            address_a=0,
                            var_b=0,
                            address_b=0,
                            ):
        if(operation==-1):
            if(address_a != 0 and address_b != 0):
                self.code_generator.add(address_a=address_a, address_b=address_b)

            elif(address_a != 0 and var_b != 0):
                self.code_generator.add(address_a=address_a, var_b=var_b)

            elif(var_a != 0 and address_b != 0):
                self.code_generator.add(var_a=var_a , address_b=address_b)

        elif(operation==-2):
            if(address_a != 0 and address_b != 0):
                self.code_generator.sub(address_a=address_a, address_b=address_b)
                
            elif(address_a != 0 and var_b != 0):
                self.code_generator.sub(address_a=address_a, var_b=var_b)

            elif(var_a != 0 and address_b != 0):
                self.code_generator.sub(var_a=var_a , address_b=address_b)
        elif(operation==-3):
            if(address_a != 0 and address_b != 0):
                self.code_generator.mul(address_a=address_a, address_b=address_b)
                
            elif(address_a != 0 and var_b != 0):
                self.code_generator.mul(address_a=address_a, var_b=var_b)

            elif(var_a != 0 and address_b != 0):
                self.code_generator.mul(var_a=var_a , address_b=address_b)
        elif(operation==-4):
            pass
        elif(operation==-5):
            pass