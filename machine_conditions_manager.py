
class MachineConditionsManager():
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def carry_out_condition(self, 
                            condition = "",
                            val_a=0,
                            address_a=0,
                            val_b=0,
                            address_b=0,
                            ):
        if(condition=="="):
            if(address_a != 0 and address_b != 0):
                pass
            elif(address_a != 0 and val_b != 0):
                pass
            elif(val_a != 0 and address_b != 0):
                pass
            
        elif(condition=="!="):
            if(address_a != 0 and address_b != 0):
                pass
            elif(address_a != 0 and val_b != 0):
                pass
            elif(val_a != 0 and address_b != 0):
                pass
        elif(condition=="<"):
            if(address_a != 0 and address_b != 0):
                pass
            elif(address_a != 0 and val_b != 0):
                pass
            elif(val_a != 0 and address_b != 0):
                pass
        elif(condition==">"):
            if(address_a != 0 and address_b != 0):
                pass
            elif(address_a != 0 and val_b != 0):
                pass
            elif(val_a != 0 and address_b != 0):
                pass
        elif(condition=="<="):
            if(address_a != 0 and address_b != 0):
                pass
            elif(address_a != 0 and val_b != 0):
                pass
            elif(val_a != 0 and address_b != 0):
                pass
        elif(condition==">="):
            if(address_a != 0 and address_b != 0):
                pass
            elif(address_a != 0 and val_b != 0):
                pass
            elif(val_a != 0 and address_b != 0):
                pass