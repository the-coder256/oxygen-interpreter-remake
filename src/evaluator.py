import parser

class Evaluator:
    def __init__(self):
        self.tree = []
        self.variables = {
            "-1": {"print": "<built-in function 'print'>"}
        }
    
    def evaluate_tree(self, node, scope = -1):
        if type(node) == parser.Call:
            if self.variables.get("-1").get(node.name) == "<built-in function 'print'>":
                print(*node.arguments)
    
    def evaluate(self, __tree):
        self.tree = __tree
        for node in self.tree:
            self.evaluate_tree(node)