import tokeniser

class Call:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
class Variable:
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self):
        self.tokens = []
        self.tree = []
        self.index = 0
    
    def parse_expr(self):
        start = self.advance()
        if type(start) == tokeniser.T_Ident:
            return Variable(start.value)
        else:
            return start.value
    
    def peek(self, amount = 1):
        try:
            return self.tokens[self.index + amount]
        except:
            return tokeniser.T_End("END")
    
    def consume(self):
        return self.tokens[self.index]
    
    def advance(self):
        self.index += 1
        return self.tokens[self.index - 1]
    
    def at_end(self):
        return type(self.consume()) == tokeniser.T_End
    
    def parse_call(self):
        name = Variable(self.peek(-1).value)
        self.advance()
        arguments = [self.parse_expr()]
        if not (type(self.consume()) == tokeniser.T_RightParen):
            print("Expected ')'")
            exit(1)
        self.advance()
        return Call(name, arguments)
    
    def parse_assign(self):
        name = self.peek(-1).value
        self.advance()
        expr = self.parse_expr()
        return Assign(name, expr)

    def parse_stmt(self):
        beginning = self.advance()
        if type(beginning) == tokeniser.T_Ident and type(self.consume()) == tokeniser.T_LeftParen:
            return self.parse_call()
        elif type(beginning) == tokeniser.T_Ident and type(self.consume()) == tokeniser.T_SingleEquals:
            return self.parse_assign()

    def parse(self, __tokens):
        self.tokens = __tokens
        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        return self.tree