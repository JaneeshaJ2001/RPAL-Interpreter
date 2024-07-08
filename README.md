# RPAL Interpreter

## Problem Description

The project requirement was to implement a lexical analyzer and a parser for the RPAL language. The output of the parser should be the Abstract Syntax Tree (AST) for the given input program. Then an algorithm must be implemented to convert the Abstract Syntax Tree (AST) into Standardize Tree (ST) and the CSE machine should be implemented. The program should be able to read an input file that contains an RPAL program. The output of the program should match the output of “rpal.exe“ for the relevant program.

## Solution

<p align="center">
    <picture>
      <source 
        srcset="how proposed compiler works.jpg"
        media="(prefers-color-scheme: dark)"
      />
      <img 
        src="how proposed compiler works.jpg" 
        alt="How Compiler works Image"
        width="300"
       />
    </picture>
</p>

## Overview of each phase in a compiler.

1. Tokenizer (Scanner+Screener):

- Implement a lexical analyzer to process an input file, generate tokens, identify reserved keywords, remove comments and whitespace and return an array of tokens.

2. Abstract SyntaxTree parser:

- Iterate through the token sequence and build an Abstract Syntax Tree (AST) using recursive descent parsing.

3. Standardizer:

- Standardize the Abstract Syntax Tree usinga given set of standardizing rules.

4. Control Structure Generation:

- Perform a pre-order traversal of the AST nodes while maintaining a FIFO queue to generate control structures.

5. Control Structure Environment evaluation

- Maintain a control structure array and a stack. Pop each element in the control structure array and execute a rule based on the stack top and the environment.

## Structure of the Project:

1. myrpal.py The main executable script for the interpreter which contains the parser as well.

2. Tokenizer.py Handles the tokenization of the input RPAL program into meaningful units (tokens).

3. ASTNode.py Handles the creation ,manipulation and Standarization of nodes within the Abstract Syntax Tree (AST).

4. cseMachine.py Implements the Control structure environment machine, crucial for executing the Standardized Tree.

5. Environment.py Manages environment settings such as variable bindings, essential for the execution phase.

6. controlStructure.py Generates and Manages the control structures within the interpreter.

## Getting Started

*   As prerequisites you should have,
    *    Python environment with Python version 3.11 or higher.

To get started with the platform, follow these steps : 

1. Clone the repository:
   ```plaintext
   git clone https://github.com/JaneeshaJ2001/RPAL-Interpreter.git
   ```

2. Navigate to the project directory:
```plaintext
    cd RPAL-Interpreter
```

3. Execution Instructions:

- In order to get the output only,
```plaintext
    Python .\myrpal.py file_name
```

- In order to get the AST tree printed in the command line
```plaintext
    Python .\myrpal.py file_name -ast
```





