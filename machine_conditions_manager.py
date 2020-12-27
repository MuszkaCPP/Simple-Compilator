
class MachineConditionsManager():
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def carry_out_condition(self, 
                            condition = "",
                            val_a=-1,
                            address_a=-1,
                            val_b=-1,
                            address_b=-1,
                            ):
        if(condition=="="):
            if(address_a != -1 and address_b != -1):
                self.code_generator.equals(address_a=address_a, address_b=address_b)
            elif(address_a != -1 and val_b != -1):
                self.code_generator.equals(address_a=address_a, val_b=val_b)
            elif(val_a != -1 and address_b != -1):
                self.code_generator.equals(val_a=val_a, address_b=address_b)

        elif(condition=="!="):
            if(address_a != -1 and address_b != -1):
                pass
            elif(address_a != -1 and val_b != -1):
                pass
            elif(val_a != -1 and address_b != -1):
                pass
        elif(condition=="<"):
            if(address_a != -1 and address_b != -1):
                pass
            elif(address_a != -1 and val_b != -1):
                pass
            elif(val_a != -1 and address_b != -1):
                pass
        elif(condition==">"):
            if(address_a != -1 and address_b != -1):
                pass
            elif(address_a != -1 and val_b != -1):
                pass
            elif(val_a != -1 and address_b != -1):
                pass
        elif(condition=="<="):
            if(address_a != -1 and address_b != -1):
                pass
            elif(address_a != -1 and val_b != -1):
                pass
            elif(val_a != -1 and address_b != -1):
                pass
        elif(condition==">="):
            if(address_a != -1 and address_b != -1):
                pass
            elif(address_a != -1 and val_b != -1):
                pass
            elif(val_a != -1 and address_b != -1):
                pass