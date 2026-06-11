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

class Tokeniser:
    def __init__(self):
        self.tokens = []
        self.current_token = ""
    
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
    
    def tokenise(self, content):
        in_string = 0
        string_char = ""
        in_comment = 0
        for index in range(len(content)):
            char = content[index]
            if char == "\n":
                self.append_token()
                in_comment = 0
            elif char == "/" and not in_string:
                if content[index + 1]:
                    in_comment = 1
            elif char in ["'", '"'] and not in_string:
                self.current_token += "'"
                in_string = 1
                string_char = char
            elif char == string_char and in_string:
                in_string = 0
            elif in_string:
                self.current_token += char
            elif in_comment:
                continue
            elif char == " " and not in_string:
                self.append_token()
            elif char == "(":
                self.append_token("(")
            elif char == ")":
                self.append_token(")")
            elif char == "=":
                self.append_token("=")
            else:
                self.current_token += char
        self.append_token()
        self.tokens.append(T_End("END"))
        return self.tokens