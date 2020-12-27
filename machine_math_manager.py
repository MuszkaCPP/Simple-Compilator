
class MachineMathManager():
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def carry_out_operation(self, 
                            operation = -1,
                            val_a=-1,
                            address_a=-1,
                            left_index_address=-1,
                            val_b=-1,
                            address_b=-1,
                            right_index_address=-1,
                            ):
        if(operation==-2):
            if(address_a != -1 and address_b != -1):
                self.code_generator.add(address_a=address_a, address_b=address_b)

            elif(address_a != -1 and val_b != -1):
                self.code_generator.add(address_a=address_a, val_b=val_b)

            elif(val_a != -1 and address_b != -1):
                self.code_generator.add(val_a=val_a , address_b=address_b)
            
            #tab(a) + value
            #tab(a) + variable
            #tab(a) + tab(b)

        elif(operation==-3):
            if(address_a != -1 and address_b != -1):
                self.code_generator.sub(address_a=address_a, address_b=address_b)
                
            elif(address_a != -1 and val_b != -1):
                self.code_generator.sub(address_a=address_a, val_b=val_b)

            elif(val_a != -1 and address_b != -1):
                self.code_generator.sub(val_a=val_a , address_b=address_b)

        elif(operation==-4):
            if(address_a != -1 and address_b != -1):
                self.code_generator.mul(address_a=address_a, address_b=address_b)
                
            elif(address_a != -1 and val_b != -1):
                self.code_generator.mul(address_a=address_a, val_b=val_b)

            elif(val_a != -1 and address_b != -1):
                self.code_generator.mul(val_a=val_a , address_b=address_b)

        elif(operation==-5):
            if(address_a != -1 and address_b != -1):
                self.code_generator.div(address_a=address_a, address_b=address_b)
                
            elif(address_a != -1 and val_b != -1):
                self.code_generator.div(address_a=address_a, val_b=val_b)

            elif(val_a != -1 and address_b != -1):
                self.code_generator.div(val_a=val_a , address_b=address_b)

        elif(operation==-6):
            if(address_a != -1 and address_b != -1):
                self.code_generator.mod(address_a=address_a, address_b=address_b)
                
            elif(address_a != -1 and val_b != -1):
                self.code_generator.mod(address_a=address_a, val_b=val_b)

            elif(val_a != -1 and address_b != -1):
                self.code_generator.mod(val_a=val_a , address_b=address_b)