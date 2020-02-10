'''
Wrapper class that initializes all others.
'''

import parsing
import robdd
import expression as e

class Wrapper:

    def __init__(self, use_rdp=False, expr=[]):

        self.args = parsing.Options().parse()
        if use_rdp:
            # Create an instance of the RecursiveDescentParser by indirectly creating a lexical analyzer.
            self.RDP_parser = parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr))
            self.RDP_parser.build()

            self.expr = e.Expression(self.RDP_parser.variables_index + 1, self.RDP_parser)

        self.robdd = robdd.ROBDD(self.expr)

    def apply(self):

        utils.Apply(self.expr)
