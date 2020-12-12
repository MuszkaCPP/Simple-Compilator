
class Symbol():
    def __init__(self, pidentifier, address = 0, is_tab = False, start_index = 0, end_index = 0):
        self.pidentifier = pidentifier
        self.address = address
        self.is_tab = is_tab
        
        if(is_tab):
            self.is_tab = True
            self.start_address = self.address
            self.end_address = self.start_address + (end_index - start_index)
            self.length = self.end_address - self.start_address + 1
            self.tab_offset = start_index

            print("Start:" + str(self.start_address) + " " + str(self.end_address)+ " "+ str(self.length) + "\n")

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def get_pidentifier(self):
        return self.pidentifier

    def get_tab_offset(self):
        return self.tab_offset
    
    def get_tab_length(self):
        return self.length


            
