
class MachineConditionsManager():
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def carry_out_condition(self, 
                            condition = "",
                            val_a=-1,
                            address_a=-1,
                            left_index_address = -1,
                            val_b=-1,
                            address_b=-1,
                            right_index_address = -1
                            ):
        if(condition=="="):
            #tab(a) ?[=] tab(b) DONE
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.equals(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    address_b=address_b,
                    right_index_address=right_index_address
                )
            #tab(a) ?[=] variable DONE
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.equals(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    address_b=address_b
                )
            #variable ?[=] tab(a) DONE
            elif(address_a != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.equals(
                    address_b=address_a,
                    address_a=address_b,
                    left_index_address=right_index_address

                )
            #tab(a) ?[=] value DONE
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.equals(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    val_b=val_b
                )
            #value ?[=] tab(a) DONE
            elif(val_a != -1
                and address_b != -1 
                and right_index_address != -1
                ):
                
                self.code_generator.equals(
                    val_b=val_a,
                    address_a=address_b,
                    left_index_address=right_index_address
                )
            #variable ?[=] variable DONE
            elif(address_a != -1 and address_b != -1):
                self.code_generator.equals(address_a=address_a, address_b=address_b)
            #variable ?[=] value DONE
            elif(address_a != -1 and val_b != -1):
                self.code_generator.equals(address_a=address_a, val_b=val_b)
            #value ?[=] variable DONE
            elif(val_a != -1 and address_b != -1):
                self.code_generator.equals(address_a=address_b, val_b=val_a)

        elif(condition=="!="):
            #tab(a) ?[!=] tab(b) DONE
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.not_equals(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    address_b=address_b,
                    right_index_address=right_index_address
                )
            #tab(a) ?[!=] variable DONE
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.not_equals(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    address_b=address_b
                )
            #variable ?[!=] tab(a) DONE
            elif(address_a != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.not_equals(
                    address_b=address_a,
                    address_a=address_b,
                    left_index_address=right_index_address

                )
            #tab(a) ?[!=] value DONE
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.not_equals(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    val_b=val_b
                )
            #value ?[!=] tab(a) DONE
            elif(val_a != -1
                and address_b != -1 
                and right_index_address != -1
                ):
                
                self.code_generator.not_equals(
                    val_b=val_a,
                    address_a=address_b,
                    left_index_address=right_index_address
                )
            #variable ?[!=] variable DONE
            elif(address_a != -1 and address_b != -1):
                self.code_generator.not_equals(address_a=address_a, address_b=address_b)
            #variable ?[!=] value DONE
            elif(address_a != -1 and val_b != -1):
                self.code_generator.not_equals(address_a=address_a, val_b=val_b)
            #value ?[!=] variable DONE
            elif(val_a != -1 and address_b != -1):
                self.code_generator.not_equals(address_a=address_b, val_b=val_a)

        elif(condition=="<"):
                        #tab(a) - tab(b)
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.sub(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    address_b=address_b,
                    right_index_address=right_index_address
                )
            #tab(a) - variable
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.sub(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    address_b=address_b
                )
            #variable - tab(a)
            elif(address_a != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.sub(
                    address_a=address_a,
                    address_b=address_b,
                    right_index_address=right_index_address

                )
            #tab(a) - value
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.sub(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    val_b=val_b
                )
            #value - tab(a)
            elif(val_a != -1
                and address_b != -1 
                and right_index_address != -1
                ):
                
                self.code_generator.sub(
                    val_a=val_a,
                    address_b=address_b,
                    right_index_address=right_index_address
                )
            #variable - variable
            elif(address_a != -1 and address_b != -1):
                self.code_generator.sub(address_a=address_a, address_b=address_b)
            #variable - value
            elif(address_a != -1 and val_b != -1):
                self.code_generator.sub(address_a=address_a, val_b=val_b)
            #value - variable
            elif(val_a != -1 and address_b != -1):
                self.code_generator.sub(val_a=val_a, address_b=address_b)
                
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