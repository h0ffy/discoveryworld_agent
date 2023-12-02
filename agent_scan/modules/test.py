from yapsy.IPlugin import IPlugin


class Test(IPlugin):
    def __init__(self):
        self.print_hello()


    def print_hello(self):
        print "Hello kitty!!"
        
    