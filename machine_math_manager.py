
class MachineMathManager():
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def carry_out_operation(self, 
                            operation = '',
                            val_a=-1,
                            address_a=-1,
                            left_index_address=-1,
                            left_offset=-1,
                            val_b=-1,
                            address_b=-1,
                            right_index_address=-1,
                            right_offset=-1,
        ):

        if(operation=='+'):
            #tab(a) + tab(b)
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.add(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )
            #tab(a) + variable
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.add(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b
                )
            #variable + tab(a)
            elif(address_a != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.add(
                    address_b=address_a,
                    address_a=address_b,
                    left_index_address=right_index_address,
                    right_offset=right_offset

                )
            #tab(a) + value
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.add(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    val_b=val_b
                )
            #value + tab(a)
            elif(val_a != -1
                and address_b != -1 
                and right_index_address != -1
                ):
                
                self.code_generator.add(
                    val_b=val_a,
                    address_a=address_b,
                    left_index_address=right_index_address,
                    right_offset=right_offset
                )
            #variable + variable
            elif(address_a != -1 and address_b != -1):
                self.code_generator.add(address_a=address_a, address_b=address_b)
            #variable + value
            elif(address_a != -1 and val_b != -1):
                self.code_generator.add(address_a=address_a, val_b=val_b)
            #value + variable
            elif(val_a != -1 and address_b != -1):
                self.code_generator.add(address_a=address_b, val_b=val_a)

        elif(operation=='-'):
            #tab(a) - tab(b)
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.sub(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )
            #tab(a) - variable
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.sub(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
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
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )
            #tab(a) - value
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.sub(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
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
                    right_index_address=right_index_address,
                    right_offset=right_offset
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

        elif(operation=='*'):
            #tab(a) * tab(b)
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.mul(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )
            #tab(a) * variable
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.mul(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b
                )
            #variable * tab(a)
            elif(address_a != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.mul(
                    address_b=address_a,
                    address_a=address_b,
                    left_index_address=right_index_address,
                    right_offset=right_offset
                )
            #tab(a) * value
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.mul(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    val_b=val_b
                )
            #value * tab(a)
            elif(val_a != -1
                and address_b != -1 
                and right_index_address != -1
                ):
                
                self.code_generator.mul(
                    val_b=val_a,
                    address_a=address_b,
                    left_index_address=right_index_address,
                    right_offset=right_offset
                )
            #variable * variable
            elif(address_a != -1 and address_b != -1):
                self.code_generator.mul(address_a=address_a, address_b=address_b)
            #variable * value
            elif(address_a != -1 and val_b != -1):
                self.code_generator.mul(address_a=address_a, val_b=val_b)
            #value * variable
            elif(val_a != -1 and address_b != -1):
                self.code_generator.mul(address_a=address_b, val_b=val_a)

        elif(operation=='/'):
            #tab(a) / tab(b)
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.div(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )
            #tab(a) / variable
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.div(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b
                )
            #variable / tab(a)
            elif(address_a != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.div(
                    address_a=address_a,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )
            #tab(a) / value
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.div(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    val_b=val_b
                )
            #value / tab(a)
            elif(val_a != -1
                and address_b != -1 
                and right_index_address != -1
                ):
                
                self.code_generator.div(
                    val_a=val_a,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )
            #variable / variable
            elif(address_a != -1 and address_b != -1):
                self.code_generator.div(address_a=address_a, address_b=address_b)
            #variable / value
            elif(address_a != -1 and val_b != -1):
                self.code_generator.div(address_a=address_a, val_b=val_b)
            #value / variable
            elif(val_a != -1 and address_b != -1):
                self.code_generator.div(val_a=val_a, address_b=address_b)

        elif(operation=='%'):
            #tab(a) % tab(b)
            if(address_a != -1
                and left_index_address != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.mod(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )

            #tab(a) % variable
            elif(address_a != -1
                and left_index_address != -1
                and address_b != -1
                ):

                self.code_generator.mod(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    address_b=address_b
                )

            #variable % tab(a)
            elif(address_a != -1
                and address_b != -1
                and right_index_address != -1
                ):

                self.code_generator.mod(
                    address_a=address_a,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )

            #tab(a) % value
            elif(address_a != -1 
                and left_index_address != -1
                and val_b != -1
                ):
                
                self.code_generator.mod(
                    address_a=address_a,
                    left_index_address=left_index_address,
                    left_offset=left_offset,
                    val_b=val_b
                )
            #value % tab(a)
            elif(val_a != -1
                and address_b != -1 
                and right_index_address != -1
                ):
                
                self.code_generator.mod(
                    val_a=val_a,
                    address_b=address_b,
                    right_index_address=right_index_address,
                    right_offset=right_offset
                )

            #variable % variable
            elif(address_a != -1 and address_b != -1):
                self.code_generator.mod(address_a=address_a, address_b=address_b)
            #variable % value
            elif(address_a != -1 and val_b != -1):
                self.code_generator.mod(address_a=address_a, val_b=val_b)
            #value % variable
            elif(val_a != -1 and address_b != -1):
                self.code_generator.mod(val_a=val_a, address_b=address_b)