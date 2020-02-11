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

        self.RDP_parsers = [parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr1)), \
                            parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr1))]

        self.expressions = [e.Expression(self.RDP_parsers[0].variables_index + 1, self.RDP_parsers[0]), \
                            e.Expression(self.RDP_parsers[1].variables_index + 1, self.RDP_parsers[1])]

        self.robdds = [robdd.ROBDD(self.expressions[0]), robdd.ROBDD(self.expressions[1])]

        u, rbd = utils.Apply(self.args.op, self.robdds[0].build(), self.robdds[1].build(), self.robdds[0], self.robdds[1])

        
