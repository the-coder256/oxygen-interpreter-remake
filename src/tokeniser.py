class T_Token:     # generic token type
    def __init__(self, value):
        self.value = value
class T_Number:
    def __init__(self, value):
        x = float(value)
        if x == int(float(value)):
            self.value = int(x)
        else:
            self.value = x
class T_String:
    def __init__(self, value):
        self.value = value[1:]
class T_Ident:
    def __init__(self, value):
        self.value = value
class T_End:
    def __init__(self, value):
        self.value = value
class T_LeftParen:
    def __init__(self, value):
        self.value = value
class T_RightParen:
    def __init__(self, value):
        self.value = value
class T_SingleEquals:
    def __init__(self, value):
        self.value = value
class T_LeftBrace:
    def __init__(self, value):
        self.value = value
class T_RightBrace:
    def __init__(self, value):
        self.value = value
class T_If:
    def __init__(self, value):
        self.value = value
class T_Else:
    def __init__(self, value):
        self.value = value
class T_Define:
    def __init__(self, value):
        self.value = value
class T_Comma:
    def __init__(self, value):
        self.value = value
class T_Return:
    def __init__(self, value):
        self.value = value
class T_Plus:
    def __init__(self, value):
        self.value = value
class T_Minus:
    def __init__(self, value):
        self.value = value
class T_Star:
    def __init__(self, value):
        self.value = value
class T_Slash:
    def __init__(self, value):
        self.value = value
class T_DoubleEquals:
    def __init__(self, value):
        self.value = value
class T_Less:
    def __init__(self, value):
        self.value = value
class T_Greater:
    def __init__(self, value):
        self.value = value
class T_LessEquals:
    def __init__(self, value):
        self.value = value
class T_GreaterEquals:
    def __init__(self, value):
        self.value = value
class T_For:
    def __init__(self, value):
        self.value = value

class Tokeniser:
    def __init__(self):
        self.content = ""
        self.tokens = []
        self.current_token = ""
        self.index = 0
    
    def create_token(self, value):
        t_type = None
        if value == "(":
            t_type = T_LeftParen
        elif value == ")":
            t_type = T_RightParen
        elif value[0] == "'":
            t_type = T_String
        elif value == "=":
            t_type = T_SingleEquals
        elif value == "{":
            t_type = T_LeftBrace
        elif value == "}":
            t_type = T_RightBrace
        elif value == "if":
            t_type = T_If
        elif value == "else":
            t_type = T_Else
        elif value == "define":
            t_type = T_Define
        elif value == ",":
            t_type = T_Comma
        elif value == "return":
            t_type = T_Return
        elif value == "+":
            t_type = T_Plus
        elif value == "-":
            t_type = T_Minus
        elif value == "*":
            t_type = T_Star
        elif value == "/":
            t_type = T_Slash
        elif value == "<":
            t_type = T_Less
        elif value == ">":
            t_type = T_Greater
        elif value == "==":
            t_type = T_DoubleEquals
        elif value == "<=":
            t_type = T_LessEquals
        elif value == ">=":
            t_type = T_GreaterEquals
        elif value == "for":
            t_type = T_For
        else:
            try:
                x = float(value)
                t_type = T_Number
            except:
                t_type = T_Ident
        return t_type(value)

    def append_token(self, extra=None):
        if self.current_token:
            self.tokens.append(self.create_token(self.current_token))
            self.current_token = ""
        if extra:
            self.tokens.append(self.create_token(extra))
    
    def peek(self, amount = 1):
        try:
            return self.content[self.index + amount]
        except:
            return ""
    
    def tokenise(self, content):
        self.content = content
        in_string = 0
        string_char = ""
        in_comment = 0
        in_ml_comment = 0
        for index in range(len(content)):
            self.index = index
            char = content[index]
            if char == "\n":
                self.append_token()
                in_comment = 0
            elif char == "/" and not in_string:
                if self.peek() == "/":
                    in_comment = 1
                elif self.peek() == "*":
                    in_ml_comment = 1
                elif self.peek(-1) not in ["*", "/"]:
                    self.append_token("/")
            elif char == "*" and in_ml_comment:
                if self.peek() == "/":
                    in_ml_comment = 0
            elif in_comment or in_ml_comment:
                continue
            elif char in ["'", '"'] and not in_string:
                self.current_token += "'"
                in_string = 1
                string_char = char
            elif char == string_char and in_string:
                in_string = 0
            elif in_string:
                self.current_token += char
            elif char == " " and not in_string:
                self.append_token()
            elif char == "(":
                self.append_token("(")
            elif char == ")":
                self.append_token(")")
            elif char == ",":
                self.append_token(",")
            elif char == "+":
                self.append_token("+")
            elif char == "-":
                self.append_token("-")
            elif char == "*":
                self.append_token("*")
            elif char == "=":
                if self.peek() == "=":
                    self.append_token("==")
                elif self.peek(-1) not in ["=", "<", ">"]:
                    self.append_token("=")
            elif char == "<":
                if self.peek() == "=":
                    self.append_token("<=")
                else:
                    self.append_token("<")
            elif char == ">":
                if self.peek() == "=":
                    self.append_token(">=")
                else:
                    self.append_token(">")
            else:
                self.current_token += char
        self.append_token()
        self.tokens.append(T_End("END"))
        return self.tokens