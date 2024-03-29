'''
Parsing utilities.

Includes commandline argument parser, a Lexical Analyzer and a Recursive Descent Parser.

Classes:

1. Options: Handles commandline arguments.
2. Lexer: A Lexical Analyzer that parses the commandline input and feeds the Recursive Descent Parser. Note that the input expression is assumed to be valid.
3. RecursiveDescentParser: A Recursive Descent Parser that builds an expression tree that is traversed by various utilities (mainly Build) to evaluate the expression.

Note: The expression itself is handled by a separate Expression API defined in the expression.py file.
This is done so that the ROBDD can have a unified API for expression evaluation regardless of the way the expression is actually stored or processed.

Author: Prathamesh Mandke
'''

import argparse

import utils

class Options:

    def __init__(self):

        self.initialized = False

    def __build_parser(self, parser):

        parser.add_argument('--nvars', type=int, default=2, help='Number of variables x0, x1, etc. in the default expression.')
        parser.add_argument('--expr', type=str, default='', help='The main expression input as a string. No correctness check will be performed. Expression is assumed to be valid.')
        parser.add_argument('--op', type=str, default='', help='Operation to perform during Apply function.')
        parser.add_argument('--nvars1', type=int, default=2, help='Number of variables x0, x1, etc. in expression1.')
        parser.add_argument('--nvars2', type=int, default=2, help='Number of variables x0, x1, etc. in expression2.')
        parser.add_argument('--expr1', type=str, default='', help='Expression 1 for Apply function.')
        parser.add_argument('--expr2', type=str, default='', help='Expression 2 for Apply function.')

        parser.add_argument('--j', type=int, default=1, help='Variable number to restrict in expr.')
        parser.add_argument('--b', type=int, default=0, help='Variable value to restrict.')

        parser.add_argument('--call', type=str, default='', help='Function in main to be called.')

        self.initialized = True
        self.parser = parser

    def parse(self):

        self.parser = argparse.ArgumentParser()
        self.__build_parser(self.parser)

        return self.parser.parse_args()

class Lexer:
    '''The Lexical Analyzer.'''
    def __init__(self, expression):

        self.expr = expression
        self.index = 0

    def get_next_item(self):
        '''Returns one item at a time to the RecursiveDescentParser.'''
        i = self.index

        while i < len(self.expr) and self.expr[i] in [' ', ',', '(', ')']:
            i += 1

        # Check for expressions
        if (i+3) < len(self.expr) and self.expr[i:i+3] in ['and', 'not', 'imp']:
            self.index = i + 3
            return self.expr[i:i+3]
        elif (i+2) < len(self.expr) and self.expr[i:i+2] == 'or':
            self.index = i + 2
            return self.expr[i:i+2]
        elif (i+5) < len(self.expr) and self.expr[i:i+5] == 'equiv':
            self.index = i + 5
            return self.expr[i:i+5]

        # Check for variables (assuming variables are denoted by x1, x2 and so on)
        if (i+1) < len(self.expr) and self.expr[i] == 'x':
            k = 1
            while (i + k) < len(self.expr) and self.expr[i + k] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                k += 1

            self.index = i + k
            return self.expr[i:i+k]

        # If it's niether variable nor operation then it must be a constant!
        if i < len(self.expr):
            assert int(self.expr[i]) in [0, 1]

            self.index = i + 1

            return self.expr[i]

        return None

    def reset_lexer(self):
        self.index = 0

class RecursiveDescentParser:
    '''The Recursive Descent Parser (RDP).'''
    def __init__(self, lexer):

        self.lexer = lexer # The Lexical Analyzer associated with this RDP.
        self.root = utils.RDP_node() # Root of the RDP
        self.variables_index = 0 # The variables as encountered are stored in this variable. Only the variable with max index is stored here.

    def build(self):
        '''Query the Lexical Analyzer and build a parse tree.'''
        def __build(node):
            item = self.lexer.get_next_item()

            while item:
                if item in ['0', '1']:

                    if node.left:
                        node.right = utils.RDP_node(val=item, type='const', is_terminal=True)
                    else:
                        node.left = utils.RDP_node(val=item, type='const', is_terminal=True)

                    if node.val == 'not':
                        return
                elif item[0] == 'x':
                    if node.left:
                        node.right = utils.RDP_node(val=item, type='var', is_terminal=True,\
                        is_var=True, var_index=int(item[1:]))
                    else:
                        node.left = utils.RDP_node(val=item, type='var', is_terminal=True, \
                        is_var=True, var_index=int(item[1:]))

                    if int(item[1:]) > self.variables_index:
                        self.variables_index = int(item[1:])

                    if node.val == 'not':
                        return
                elif item in ['and', 'or', 'not', 'equiv', 'imp']:
                    if node.left:
                        node.right = utils.RDP_node(val=item, type='func', is_func=True)
                        __build(node.right)
                    else:
                        node.left = utils.RDP_node(val=item, type='func', is_func=True)
                        __build(node.left)
                if node.left and node.right:
                    return

                item = self.lexer.get_next_item()

        value = self.lexer.get_next_item()
        if value in ['and', 'or', 'not', 'equiv', 'imp']:
            self.root.val = value
            self.root.is_func = True
            self.root.type = 'func'
            __build(self.root)
        else:
            print("First input cannot be constant or variable. It must be a boolean function among: ['and', 'or', 'not', 'equiv', 'imp']")

    def parse_tree(self, variable_val=[]) -> int:
        '''Parse the tree given a variable instantiation.'''
        def traverse(node):

            if node:
                if node.type == 'func':
                    if node.val == 'not':
                        return utils.apply(node.val, traverse(node.left))
                    else:
                        return utils.apply(node.val, traverse(node.left), rexpr=traverse(node.right))
                elif node.type == 'var':
                    if variable_val[node.var_index] == -1:
                        print("Variable {} is not initialized".format(node.var_index))
                    return variable_val[node.var_index]
                elif node.type == 'const':
                    return int(node.val)

        if self.root:
            return traverse(self.root)
