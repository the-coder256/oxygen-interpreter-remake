from sys import argv
import tokeniser
import parser
import evaluator

if len(argv) < 2:
    print("ERROR: No file given")
    exit(1)

if argv[1] in ["-v", "--version"]:
    print("Oxygen Interpreter v0.6")
    exit(0)

with open(argv[1], "r") as file:
    content = file.read()

tokens = tokeniser.Tokeniser().tokenise(content)
tree = parser.Parser().parse(tokens)
evaluator.Evaluator().evaluate(tree)