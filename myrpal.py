import Tokenizer
from Tokenizer import Screener
import controlStructure
from cseMachine import CSEMachine
from ASTNode import ASTNode


class ASTParser:

    def __int__(self, tokens):
        # Initialize the ASTParser object with the provided tokens.

        self.tokens = tokens
        self.current_token = None
        self.index = 0

    def read(self):
        # Read the current token and move to the next one.

        if self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT, Tokenizer.TokenType.STRING] :

            terminalNode = ASTNode( str(self.current_token.type))
            terminalNode.value= self.current_token.value
            stack.append(terminalNode)
            
        if self.current_token.value in  ['true', 'false', 'dummy', 'nil']:
            
            terminalNode = ASTNode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)
        
        self.index += 1

        if (self.index < len(self.tokens)):
            self.current_token = self.tokens[self.index]
     

    def build_tree(self, token, ariness):
        # Build the abstract syntax tree.

        node = ASTNode(token)

        node.value = None
        node.sourceLineNumber = -1
        node.child = None
        node.sibling = None
        node.previous = None

        while ariness > 0:
            
            child = stack[-1]
            stack.pop()
            
            if node.child is not None:
                child.sibling = node.child
                node.child.previous = child
                
            node.child = child
            node.sourceLineNumber = child.sourceLineNumber
            ariness -= 1
        

        stack.append(node)  # Assuming push() is a function that pushes a node onto a stack
        
        for node in stack:
            pass
            

    def procE(self):
        # Process the expression.
        
        if self.current_token.value == 'let':
            self.read()
            self.procD()

            if self.current_token.value != 'in':
                return

            self.read()
            self.procE()
            self.build_tree("let", 2)

        elif self.current_token.value == 'fn':
            n = 0
            self.read()

            while self.current_token.type == Tokenizer.TokenType.ID or self.current_token.value == '(':
                self.procVb()
                n += 1

            if n == 0:
                return

            if self.current_token.value != '.':
                return

            self.read()
            self.procE()
            self.build_tree("lambda", n+1)
        else:    
            self.procEw()

    def procEw(self):
        self.procT()

        # Process expression with 'where' clause
        if self.current_token.value == 'where':
            self.read()
            self.procDr()
            self.build_tree("where", 2) # Build AST node for 'where' clause with arity 2

    def procT(self):
        self.procTa()

        n = 0   # Initialize counter for tuple types
        while self.current_token.value == ',':
            self.read()
            self.procTa()
            n += 1  # Increment tuple type counter
        if n > 0:
            self.build_tree("tau", n + 1)   # Build AST node for tuple type with arity n+1
        else:
            pass

    def procTa(self):
        self.procTc()
        while self.current_token.value == 'aug':
            self.read()
            self.procTc()
            self.build_tree("aug", 2)   # Build AST node for augmented type with arity 2`

    def procTc(self):

        self.procB()    # Process boolean expression

        if self.current_token.type == Tokenizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.procTc()

            if self.current_token.value != '|':
                print("Error: | is expected")   # Print error message if '|' is missing
                return
            self.read()
            self.procTc()
            self.build_tree("->", 3)    # Build AST node for conditional type with arity 3

    def procB(self):

        self.procBt()
        while self.current_token.value == 'or':
            self.read()
            self.procBt()
            self.build_tree("or", 2)    # Build AST node for logical OR operation with arity 2

    def procBt(self):

        self.procBs()
        while self.current_token.value == '&':
            self.read()
            self.procBs()
            self.build_tree("&", 2) # Build AST node for logical AND operation with arity 2

    def procBs(self):

        if self.current_token.value == 'not':
            self.read()
            self.procBp()
            self.build_tree("not", 1)   # Build AST node for logical NOT operation with arity 1
        else:
            self.procBp()   # Process boolean primary expression

    def procBp(self):
        # Process boolean predicates

        self.procA()
        
        # Check for comparison operators and build corresponding AST nodes
        if self.current_token.value == '>':
            self.read()
            self.procA()
            self.build_tree("gr", 2)    # Build AST node for greater than comparison
        elif self.current_token.value == 'gr':
            self.read()
            self.procA()
            self.build_tree("gr", 2)    # Build AST node for greater than comparison
        elif self.current_token.value == 'ge':
            self.read()
            self.procA()
            self.build_tree("ge", 2)    # Build AST node for greater than or equal comparison
        elif self.current_token.value == '>=':
            self.read()
            self.procA()
            self.build_tree("ge", 2)    # Build AST node for greater than or equal comparison
        elif self.current_token.value == '<':
            self.read()
            self.procA()
            self.build_tree("ls", 2)     # Build AST node for less than comparison
        elif self.current_token.value == 'ls':
            self.read()
            self.procA()
            self.build_tree("ls", 2)     # Build AST node for less than comparison
        elif self.current_token.value == '<=':
            self.read()
            self.procA()
            self.build_tree("le", 2)     # Build AST node for less than or equal comparison
        elif self.current_token.value == 'le':
            self.read()
            self.procA()
            self.build_tree("le", 2)     # Build AST node for less than or equal comparison
        elif self.current_token.value == 'eq':
            self.read()
            self.procA()
            self.build_tree("eq", 2)     # Build AST node for equal comparison
        elif self.current_token.value == 'ne':
            self.read()
            self.procA()
            self.build_tree("ne", 2)    # Build AST node for not equal comparison
        else:
            return

        
    def procA(self):

        # Check for unary plus operator
        if self.current_token.value == '+':
            self.read()
            self.procAt()
            
        # Check for unary minus operator
        elif self.current_token.value == '-':
            self.read()
            self.procAt()
            self.build_tree("neg", 1)   # Build AST node for unary negation

        else:
            self.procAt()
        plus = '+'  # Initialize operator to handle consecutive additions
        while self.current_token.value == '+' or self.current_token.value == '-':
            # Process consecutive addition and subtraction operations

            if self.current_token.value=='-':
                plus='-'

            self.read()
            self.procAt()
            self.build_tree(plus, 2)    # Build AST node for addition or subtraction


    def procAt(self):

        # Process the first factor
        self.procAf()

        # Continue processing multiplication and division operations
        while self.current_token.value == '*' or self.current_token.value == '/':
            self.read()
            self.procAf()
            self.build_tree("*", 2) # Build AST node for multiplication or division

    def procAf(self):
        # Process arithmetic factors

        self.procAp()

        # Continue processing exponentiation operations
        while self.current_token.value == '**':
            self.read()
            self.procAf()
            self.build_tree("**", 2)    # Build AST node for exponentiation

    def procAp(self):

        # Process the primary expression
        self.procR()
        while self.current_token.value == '@':
            self.read()
            self.procR()
            self.build_tree("@", 2) # Build AST node for application

    def procR(self):

        self.procRn()

        # Continue processing expressions until no more valid tokens are found
        while (self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT, Tokenizer.TokenType.STRING] or self.current_token.value in ['true', 'false',
                                                                                                       'nil', 'dummy',
                                                                                                        "("]):
            if self.index >= len(self.tokens):
                break
            self.procRn()
            # Build AST node for function application
            self.build_tree("gamma", 2)


    def procRn(self):

        # Check if the current token represents an identifier, integer, or string
        if self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT, Tokenizer.TokenType.STRING]:

            self.read()  # Read the current token

        # Check if the current token represents a boolean value or nil
        elif self.current_token.value in ['true', 'false', 'nil', 'dummy']:
            self.read()

        # Check if the current token represents the start of a parenthesized expression
        elif self.current_token.value == '(':
            self.read()
            self.procE()

            # Check if the expression is properly terminated with a ')'
            if self.current_token.value != ')':
                return  # Return if ')' is not found
            self.read()

    def procD(self):

        self.procDa()
        while self.current_token.value == 'within':
            self.read()
            self.procD()
            self.build_tree("within", 2)    # Build the AST node representing the 'within' clause

    def procDa(self):

        self.procDr()
        n = 0

        # Continue processing declarations separated by 'and'
        while self.current_token.value == 'and':

            # Increment the count of 'and' occurrences
            n += 1
            self.read()

            # Process the next declaration recursively
            self.procDa()

        # If there were multiple declarations separated by 'and', build an AST node for them
        if n > 0:
            self.build_tree("and", n + 1)

    def procDr(self):

        if self.current_token.value == 'rec':
            self.read()
            self.procDb()
            self.build_tree("rec", 1)

        # Process a non-recursive declaration
        self.procDb()

    def procDb(self):

        if self.current_token.value == '(':
            self.read()
            self.procD()
            if self.current_token.value != ')':
                return
            self.read()
            self.build_tree("()", 1)

        elif self.current_token.type == Tokenizer.TokenType.ID:
            self.read()

            if self.current_token.type == Tokenizer.TokenType.COMMA:
                self.read()
                self.procVb()

                if self.current_token.value != '=':
                    print("Error: = is expected")
                    return
                self.build_tree(",", 2)
                self.read()
                self.procE()
                self.build_tree("=", 2)
            else :
                if self.current_token.value == '=':
                    self.read()
                    self.procE()
                    self.build_tree("=", 2)

                else :
                    n = 0
                    while self.current_token.type == Tokenizer.TokenType.ID or self.current_token.value == '(':
                        self.procVb()
                        n += 1

                    if n == 0:
                        print("Error: ID or ( is expected")
                        return

                    if self.current_token.value != '=':
                        print("Error: = is expected")
                        return
                    self.read()
                    self.procE()
                    self.build_tree("function_form", n + 2)

        
    def procVb(self):
        if self.current_token.type == Tokenizer.TokenType.ID:
            self.read()

        elif self.current_token.value == '(':
            self.read()
            if self.current_token.type == ')':
                self.build_tree("()", 0)
                self.read()
            else:
                self.procVL()
                if self.current_token.value != ')':
                    print("Error: ) is expected")
                    return
            self.read()

        else:
            print("Error: ID or ( is expected")
            return

    def procVL(self):

        if self.current_token.type != Tokenizer.TokenType.ID:
            pass
        else:
            pass

            self.read()
            trees_to_pop = 0
            while self.current_token.value == ',':
                self.read()
                if self.current_token.type != Tokenizer.TokenType.ID:
                    print(" 572 VL: Identifier expected")  # Replace with appropriate error handling
                self.read()
                # print('VL->id , ?')

                trees_to_pop += 1
            
            if trees_to_pop > 0:
                self.build_tree(',', trees_to_pop +1)  # +1 for the child identifier



if __name__ == "__main__":
    import sys

    # Command-line argument parsing

    if len(sys.argv) > 1:
        argv_idx = 1  
        ast_flag = 0  

        if len(sys.argv) == 3:  
            argv_idx = 2
            if sys.argv[2] == "-ast":
                ast_flag = 1

            input_path = sys.argv[1]
        else:
            input_path = sys.argv[1]

    # Read program from file
    with open(input_path) as file:
        program = file.read()

    stack = []  # Initialize stack for AST nodes
    tokens = [] # Initialize list to store tokens

    # tokenize input
    tokenizer = Tokenizer.Tokenizer(program)
    token = tokenizer.get_next_token()
    while token.type != Tokenizer.TokenType.EOF:
        tokens.append(token)
        token = tokenizer.get_next_token()

    # sreen tokens
    screener = Screener(tokens)
    tokens = screener.screen()

    # Initialize AST parser
    parser = ASTParser()
    parser.tokens = tokens
    parser.current_token = tokens[0]
    parser.index = 0

    # Parse the expression
    parser.procE()
    root = stack[0]

    # Write AST to file

    with open("output_files/" + input_path.split("\\")[-1], "w") as file:
        root.indentation = 0
        root.print_tree_to_file(file)
        if ast_flag == 1: root.print_tree_to_cmd()

    if ast_flag == 0:
        # Standarize AST

        ASTStandarizer = ASTNode("ASTStandarizer")
        root = ASTStandarizer.standarize(root)

        with open( "output_files/"+input_path.split("\\")[-1] + "__standarized_output", "w") as file:
            root.indentation = 0
            root.print_tree_to_file(file)

        # Generate control structures
        ctrlStructGen = controlStructure.ControlStructureGenerator()
        ctr_structures = ctrlStructGen.generate_control_structures(root)
        
        # Execute CSE machine
        cseMachine = CSEMachine(ctr_structures, input_path)
        result = cseMachine.execute()
       

