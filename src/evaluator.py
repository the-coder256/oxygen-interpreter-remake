import parser

class Evaluator:
    def __init__(self):
        self.tree = []
        self.variables = {
            "-1": {"print": "<built-in function 'print'>"}
        }
        self.id = 0
    
    def is_base_type(self, value):
        return type(value) in [str, int, float]
    
    def create_new_scope(self):
        new_id = self.id
        self.variables.update({str(self.id): {"print": "<built-in function 'print'>"}})
        self.id += 1
        return new_id
    
    def destroy_scope(self, scope:int):
        if scope == -1:
            print("ERROR: Can't destroy global scope")
            exit(2)
        self.variables.pop(str(scope))
    
    def get_variable_value(self, name, scope = -1, parent_scope = None):
        # attempt to get variable from current scope
            value = self.variables.get(str(scope)).get(str(name))
            if value is None:
                # if that fails, check parent scope
                if parent_scope is None:
                    value = None
                else:
                    value = self.variables.get(str(parent_scope)).get(str(name))
                if value is None:
                    # the variable doesnt exist
                    print("ERROR: Variable '" + str(name) + "' doesn't exist")
                    exit(1)
                else:
                    return value
            else:
                return value
    
    def set_variable_value(self, name, value, scope = -1):
        self.variables.get(str(scope)).update({str(name): value})
    
    def get_scope_from_name(self, name, scope:int) -> int:
        # check current scope
        value = self.variables.get(str(scope)).get(name)
        if value:
            return scope
        else:
            # check global scope
            value = self.variables.get("-1").get(name)
            if value:
                return -1
            else:
                print("ERROR: Couldn't locate scope of", name)
                exit(2)
    
    def evaluate_tree(self, node, scope = -1, parent_scope:(int|None) = None):
        if type(node) == parser.Call:
            if not self.is_base_type(node.name):
                name = self.evaluate_tree(node.name, scope, parent_scope)
            else:
                name = node.name
            arguments = []
            for arg in node.arguments:
                if not self.is_base_type(arg):
                    arguments.append(self.evaluate_tree(arg, scope, parent_scope))
                else:
                    arguments.append(arg)
            if name == "<built-in function 'print'>":
                print(*arguments)
            else:
                definition:parser.Definiton = self.get_variable_value(node.name.name, scope, parent_scope)
                if type(definition) != parser.Definiton:
                    print("Missing definition")
                    exit(1)
                # create scope
                parent = self.get_scope_from_name(node.name.name, scope)
                new_scope = self.create_new_scope()
                # initialise parameter variables
                if len(definition.parameters) > len(node.arguments):
                    print("Not enough parameters")
                    exit(1)
                for index in range(len(definition.parameters)):    # we know there are enough arguments
                    if not self.is_base_type(node.arguments[index]):
                        arg = self.evaluate_tree(node.arguments[index], scope, parent_scope)
                    else:
                        arg = node.arguments[index]
                    param = str(definition.parameters[index])
                    self.variables.get(str(new_scope)).update({param: arg})
                # evaluate all statements
                for stmt in definition.statements:      # There is a bug where you cant put a return in a block in a definition
                    if type(stmt) == parser.Return:     # Yeah uhh i cant fix that (wait until bytecode vm :P)
                        if not self.is_base_type(stmt.value):
                            ret_val = self.evaluate_tree(stmt.value, new_scope, parent)
                        else:
                            ret_val = stmt.value
                        # destroy the scope
                        self.destroy_scope(new_scope)
                        return ret_val
                    else:
                        self.evaluate_tree(stmt, new_scope, parent)
                # destroy the scope
                self.destroy_scope(new_scope)
        elif type(node) == parser.Assign:
            if not self.is_base_type(node.value):
                value = self.evaluate_tree(node.value, scope, parent_scope)
            else:
                value = node.value
            self.set_variable_value(node.name, value, scope)
        elif type(node) == parser.Variable:
            return self.get_variable_value(node.name, scope, parent_scope)
        elif type(node) == parser.IfCondition:
            if not self.is_base_type(node.condition):
                condition = self.evaluate_tree(node.condition, scope, parent_scope)
            else:
                condition = node.condition
            if condition:
                for stmt in node.statements:
                    self.evaluate_tree(stmt, scope, parent_scope)
            else:
                if len(node.elif_statements) > 0:
                    trigger_else = True
                    for index in range(len(node.elif_statements)):
                        elif_condition = node.elif_conditions[index]
                        elif_stmts = node.elif_statements[index]
                        if not self.is_base_type(elif_condition):
                            this_condition = self.evaluate_tree(elif_condition, scope, parent_scope)
                        else:
                            this_condition = elif_condition
                        if this_condition:
                            trigger_else = False
                            for elif_stmt in elif_stmts:
                                self.evaluate_tree(elif_stmt, scope, parent_scope)
                            break
                    if trigger_else:
                        for stmt in node.else_statements:
                            self.evaluate_tree(stmt, scope, parent_scope)
                else:
                    for stmt in node.else_statements:
                        self.evaluate_tree(stmt, scope, parent_scope)
        elif type(node) == parser.Definiton:
            self.set_variable_value(node.name, node, scope)
        elif type(node) == parser.BinOp:
            if not self.is_base_type(node.left):
                left = self.evaluate_tree(node.left, scope, parent_scope)
            else:
                left = node.left
            if not self.is_base_type(node.right):
                right = self.evaluate_tree(node.right, scope, parent_scope)
            else:
                right = node.right
            if node.op == "+":
                return left + right
            elif node.op == "-":
                return left - right
            elif node.op == "*":
                return left * right
            elif node.op == "/":
                return left / right
            elif node.op == "==":
                return int(left == right)
            elif node.op == "<":
                return int(left < right)
            elif node.op == ">":
                return int(left > right)
            elif node.op == "<=":
                return int(left <= right)
            elif node.op == ">=":
                return int(left >= right)
        elif type(node) == parser.ForLoop:
            self.evaluate_tree(node.assign, scope, parent_scope)
            while True:
                # check condition
                if not self.is_base_type(node.condition):
                    condition = self.evaluate_tree(node.condition, scope, parent_scope)
                else:
                    condition = node.condition
                if not condition:
                    break
                # run statements
                for stmt in node.statements:
                    self.evaluate_tree(stmt, scope, parent_scope)
                # step
                self.evaluate_tree(node.step, scope, parent_scope)
    
    def evaluate(self, __tree):
        self.tree = __tree
        for node in self.tree:
            self.evaluate_tree(node, -1, None)