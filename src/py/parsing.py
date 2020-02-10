
import argparse

import utils

class Options:

    def __init__(self):

        self.initialized = False

    def __build_parser(self, parser):

        parser.add_argument('--nvars', type=int, default=2, help='Number of variables x0, x1, etc.')
        parser.add_argument('--expr', type=str, required=True,help='The main expression input as a string. No correctness check will be performed. Expression is assumed to be valid.')

        self.initialized = True
        self.parser = parser

    def parse(self):

        self.parser = argparse.ArgumentParser()
        self.__build_parser(self.parser)

        return parser.parse_args()

class Lexer:

    def __init__(self, expression):

        self.expr = expression
        self.index = 0

    def get_next_item(self):
        '''Note that the input expression is assumed to be valid.'''

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

        # Check for variables (assuming variables are denoted by x0, x1 and so on)
        if (i+1) < len(self.expr) and self.expr[i] == 'x' and (int(self.expr[i+1]) >= 0):
            self.index = i + 2
            return self.expr[i:i+2]

        # If it's niether variable nor operation then it must be a constant!
        if i < len(self.expr):
            assert int(self.expr[i]) in [0, 1]

            self.index = i + 1

            return self.expr[i]

        return None

    def reset_lexer(self):
        self.index = 0

class RecursiveDescentParser:

    def __init__(self, lexer):

        self.lexer = lexer
        self.root = utils.RDP_node()
        self.variables_index = -1

    def build(self):

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
                        node.right = utils.RDP_node(val=item, type='var,' is_terminal=True, \
                        is_var=True, var_index=int(item[1]))
                    else:
                        node.left = utils.RDP_node(val=item, type='var', is_terminal=True, \
                        is_var=True, var_index=int(item[1]))

                    if int(item[1]) > self.variables_index:
                        self.variables_index = int(item[1])

                    if node.val == 'not':
                        return
                elif item in ['and', 'or', 'not', 'equiv', 'imp']:
                    if node.left:
                        node.right = utils.RDP_node(val=item, type='func', is_func=True)
                        self.build(node.right)
                    else:
                        node.left = utils.RDP_node(val=item, type='func', is_func=True)
                        self.build(node.left)

                item = self.lexer.get_next_item()

        value = self.lexer.get_next_item()
        if value in ['and', 'or', 'not', 'equiv', 'imp']:
            self.root.val = value
            self.root.is_func = True
            __build(self.root)
        else:
            print("First input cannot be constant or variable. It must be a boolean function among: ['and', 'or', 'not', 'equiv', 'imp']")

    def parse_tree(self, variable_val=[]) -> int:

        assert len(variable_val) == (self.variables_index + 1)

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
