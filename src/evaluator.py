import parser

class Evaluator:
    def __init__(self):
        self.tree = []
        self.variables = {
            "-1": {"print": "<built-in function 'print'>"}
        }
        self.id = 0    # to be used later
    
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
                definition:parser.Definiton = self.variables.get(str(scope)).get(str(node.name.name))
                if type(definition) != parser.Definiton:
                    print("Missing definition")
                    exit(1)
                # create scope
                parent = scope
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
                for stmt in definition.statements:
                    if type(stmt) == parser.Return:
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
            self.variables.get(str(scope)).update({node.name: value})
        elif type(node) == parser.Variable:
            # attempt to get variable from current scope
            value = self.variables.get(str(scope)).get(node.name)
            if value is None:
                # if that fails, check parent scope
                if parent_scope is None:
                    value = None
                else:
                    value = self.variables.get(str(parent_scope)).get(node.name)
                if value is None:
                    # the variable doesnt exist
                    print("ERROR: Variable '" + str(node.name) + "' doesn't exist")
                    exit(1)
                else:
                    return value
            else:
                return value
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
            self.variables.get(str(scope)).update({str(node.name): node})
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
    
    def evaluate(self, __tree):
        self.tree = __tree
        for node in self.tree:
            self.evaluate_tree(node, -1, None)