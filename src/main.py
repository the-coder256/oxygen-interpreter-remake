from sys import argv
import tokeniser
import parser
import evaluator

if len(argv) < 2:
    print("No file given")
    exit(1)

with open(argv[1], "r") as file:
    content = file.read()

tokens = tokeniser.Tokeniser().tokenise(content)
tree = parser.Parser().parse(tokens)
evaluator.Evaluator().evaluate(tree)