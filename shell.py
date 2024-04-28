'''
Chase Dallmann & John Petrie
4/28/2024
Shell
I 
'''
import Lexer
import Parser
import Interpreter

while True:
    option = input("Enter '1' to enter a command, '2' to read commands from a file: ")
    while option != '':
        if option == '1':
            text = input("Enter a Token: ")
            if not text.endswith('\n'):
                text += '\n'
        elif option == '2':
            with open('bankinginput.txt', 'r') as file:
                lines = file.readlines()
            text = ''.join(line.rstrip() + '\n' for line in lines)
        result, error = Lexer.run(text)
        parser = Parser.Parser(result)
        astList = parser.parse()
        Interpreter.Interpreter(astList).interpret()
