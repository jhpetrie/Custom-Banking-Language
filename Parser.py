'''
Chase Dallmann & John Petrie
4/28/2024
Parser
We pledge that all the code we have written is our own code and not copied from any other source 4/28/24
'''

import Nodes
import Lexer

#The Parser class
class Parser:

    #Defining the operator types
    operator_types = (Lexer.PLUS, Lexer.MINUS, Lexer.MULTIPLY, Lexer.CREATE, Lexer.DROP, Lexer.VIEW)

    #Initializing the Parser class with a list of tokens setting the token index to 0 to start with the first token
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = 0
        self.currentToken = self.tokens[self.tokenIndex]

    #The function to create the AST with our nodes
    def parse(self):
        res = self.transaction()
        return res

    #A function used to advance to the next token in the list
    def advance(self):
        self.tokenIndex += 1
        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]
        return self.currentToken

    #Creating a name node with a first and lastname
    def fullName(self, firstName, lastName):
        return Nodes.NameNode(firstName, lastName)

    #Creating a number node from an INT or FLOAT
    def number(self, tok):
        if tok.type in (Lexer.INT, Lexer.FLOAT):
            return Nodes.NumberNode(tok.value)

    # Creating an ID node from a unique ID
    def id(self, tok):
        if tok.type in (Lexer.ID):
            return Nodes.IDNode(tok.value)
        else:
            return None

    # Creating an operator node from one of the above operator types defined
    def operator(self, tok):
        tok = tok.type
        if tok in self.operator_types:
            operation = tok
        else:
            raise Exception(f"Unsupported operator: {tok}")
        
        # Get the tokens before and after the operator
        account_node = self.id(self.tokens[self.tokenIndex - 1])
        number_node = self.number(self.tokens[self.tokenIndex + 1])
        self.advance()
        return Nodes.OperatorNode(tok, operation, account_node, number_node)

    # Creates a transaction AST by passing in seperate nodes, then adds it to a list of ASTs to be interpreted
    def transaction(self):
        transList = []
        while self.currentToken is not None and self.tokenIndex < len(self.tokens):
            tok = self.currentToken
            if tok.type in self.operator_types: #Operator Token handling
                op = self.operator(tok)
            elif tok.type == (Lexer.WORD): #Word Token handling
                first = self.currentToken
                self.advance()
                if self.currentToken.type == (Lexer.WORD):
                    last = self.currentToken
                    full = self.fullName(first, last)
            elif self.currentToken.type == Lexer.NEWTRANS: #New transaction handling
                trans = Nodes.TransactionNode(full, op)
                transList.append(trans)
                self.advance()
            else:
                self.advance() #If the token doesnt match advance to the next token
        return transList
