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
    
    def evaluate_tree(self, node, scope = -1):
        if type(node) == parser.Call:
            if not self.is_base_type(node.name):
                name = self.evaluate_tree(node.name, scope)
            else:
                name = node.name
            arguments = []
            for arg in node.arguments:
                if not self.is_base_type(arg):
                    arguments.append(self.evaluate_tree(arg, scope))
                else:
                    arguments.append(arg)
            if name == "<built-in function 'print'>":
                print(*arguments)
            else:
                print("Not implemented")
                exit(1)
        elif type(node) == parser.Assign:
            if not self.is_base_type(node.value):
                value = self.evaluate_tree(node.value, scope)
            else:
                value = node.value
            self.variables.get(str(scope)).update({node.name: value})
        elif type(node) == parser.Variable:
            value = self.variables.get(str(scope)).get(node.name)
            if value is None:
                print("Variable '" + str(node.name) + "' doesn't exist")
                print(value)
                exit(1)
            else:
                return value
    
    def evaluate(self, __tree):
        self.tree = __tree
        for node in self.tree:
            self.evaluate_tree(node)