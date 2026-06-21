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
class IfCondition:
    def __init__(self, condition, statements, else_statements):
        self.condition = condition
        self.statements = statements
        self.else_statements = else_statements
class Definiton:
    def __init__(self, name, parameters, statements):
        self.name = name
        self.parameters = parameters
        self.statements = statements
    def __repr__(self):
        return f"<function '{self.name}'>"
class Return:
    def __init__(self, value):
        self.value = value
class BinOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Parser:
    def __init__(self):
        self.tokens = []
        self.tree = []
        self.index = 0
    
    def parse_factor(self):
        if type(self.consume()) == tokeniser.T_LeftParen:
            self.advance()
            expr = self.parse_expr()
            self.advance()
            return expr
        else:
            return self.parse_expr(True)
    
    def parse_term(self):
        node = self.parse_factor()
        while type(self.consume()) in [tokeniser.T_Star, tokeniser.T_Slash]:
            op = self.advance().value
            right = self.parse_factor()
            node = BinOp(str(op), node, right)
        return node
    
    def parse_math(self, base=True):
        if base:
            self.index -= 1
        node = self.parse_term()
        while type(self.consume()) in [tokeniser.T_Plus, tokeniser.T_Minus]:
            op = self.advance().value
            right = self.parse_term()
            node = BinOp(str(op), node, right)
        return node
    
    def parse_expr(self, ignore_math=False):
        start = self.advance()
        if type(start) == tokeniser.T_Ident:
            if type(self.consume()) == tokeniser.T_LeftParen:
                old_index = self.index
                call = self.parse_call()
                if type(self.consume()) in [tokeniser.T_Plus, tokeniser.T_Minus, tokeniser.T_Star, tokeniser.T_Slash] and not ignore_math:
                    self.index = old_index
                    return self.parse_math()
                else:
                    return call
            elif type(self.consume()) in [tokeniser.T_Plus, tokeniser.T_Minus, tokeniser.T_Star, tokeniser.T_Slash] and not ignore_math:
                return self.parse_math()
            else:
                return Variable(start.value)
        elif type(self.consume()) in [tokeniser.T_Plus, tokeniser.T_Minus, tokeniser.T_Star, tokeniser.T_Slash] and not ignore_math:
            return self.parse_math()
        else:
            return start.value
    
    def peek(self, amount = 1) -> tokeniser.T_Token:
        try:
            return self.tokens[self.index + amount]
        except:
            return tokeniser.T_End("END")
    
    def consume(self) -> tokeniser.T_Token:
        return self.tokens[self.index]
    
    def advance(self) -> tokeniser.T_Token:
        self.index += 1
        return self.tokens[self.index - 1]
    
    def at_end(self):
        return type(self.consume()) == tokeniser.T_End
    
    def parse_call(self):
        name = Variable(self.peek(-1).value)
        self.advance()
        arguments = []
        if type(self.consume()) != tokeniser.T_RightParen:
            value = self.parse_expr()
            arguments.append(value)
            while type(self.consume()) != tokeniser.T_RightParen:
                if type(self.consume()) != tokeniser.T_Comma:
                    print("ERROR: Expected ','")
                    exit(1)
                self.advance()
                value = self.parse_expr()
                arguments.append(value)
        if type(self.consume()) != tokeniser.T_RightParen:
            print("ERROR: Expected ')'")
            exit(1)
        self.advance()
        return Call(name, arguments)
    
    def parse_assign(self):
        name = self.peek(-1).value
        self.advance()
        expr = self.parse_expr()
        return Assign(name, expr)

    def parse_if(self):
        condition = self.parse_expr()
        if type(self.consume()) != tokeniser.T_LeftBrace:
            print("ERROR: Expected '{'")
            exit(1)
        self.advance()
        statements = []
        while type(self.consume()) != tokeniser.T_RightBrace:
            stmt = self.parse_stmt()
            if not stmt:
                print("ERROR: Expected '}'")
                exit(1)
            statements.append(stmt)
        self.advance()
        else_statements = []
        if type(self.consume()) == tokeniser.T_Else:
            self.advance()
            if type(self.consume()) != tokeniser.T_LeftBrace:
                print("ERROR: Expected '{'")
                exit(1)
            self.advance()
            while type(self.consume()) != tokeniser.T_RightBrace:
                stmt = self.parse_stmt()
                if not stmt:
                    print("ERROR: Expected '{'")
                    exit(1)
                else_statements.append(stmt)
            self.advance()
        return IfCondition(condition, statements, else_statements)
    
    def parse_define(self):
        name = self.advance().value
        if type(self.consume()) != tokeniser.T_LeftParen:
            print("ERROR: Expected '('")
            exit(1)
        self.advance()
        parameters = []
        if type(self.consume()) != tokeniser.T_RightParen:
            param_name = self.advance().value
            parameters.append(param_name)
            while type(self.consume()) != tokeniser.T_RightParen:
                if type(self.consume()) != tokeniser.T_Comma:
                    print("ERROR: Expected ','")
                    exit(1)
                self.advance()
                param_name = self.advance().value
                parameters.append(param_name)
        if type(self.consume()) != tokeniser.T_RightParen:
            print("ERROR: Expected ')'")
            exit(1)
        self.advance()
        if type(self.consume()) != tokeniser.T_LeftBrace:
            print("ERROR: Expected '{'")
            exit(1)
        self.advance()
        statements = []
        while type(self.consume()) != tokeniser.T_RightBrace:
            stmt = self.parse_stmt()
            if not stmt:
                print("ERROR: Expected '}'")
                exit(1)
            statements.append(stmt)
        self.advance()
        return Definiton(name, parameters, statements)
    
    def parse_return(self):
        value = self.parse_expr()
        return Return(value)

    def parse_stmt(self):
        beginning = self.advance()
        if type(beginning) == tokeniser.T_Ident and type(self.consume()) == tokeniser.T_LeftParen:
            return self.parse_call()
        elif type(beginning) == tokeniser.T_Ident and type(self.consume()) == tokeniser.T_SingleEquals:
            return self.parse_assign()
        elif type(beginning) == tokeniser.T_If:
            return self.parse_if()
        elif type(beginning) == tokeniser.T_Define:
            return self.parse_define()
        elif type(beginning) == tokeniser.T_Return:
            return self.parse_return()

    def parse(self, __tokens):
        self.tokens = __tokens
        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        return self.tree