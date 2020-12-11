
class Symbol():
    def __init__(self, pidentifier):
        self.pidentifier = pidentifier
        self.address = ""
        self.offset = 0

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def get_pidentifier(self):
        return self.pidentifier 
