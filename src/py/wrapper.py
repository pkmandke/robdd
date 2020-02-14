'''
Wrapper class that initializes all others.
'''

import parsing
import robdd
import expression as e

class Wrapper:

    def __init__(self, use_rdp=False, expr=[]):

        self.expr = expr
        self.args = parsing.Options().parse()
        if use_rdp:
            # print("Building parser")
            # Create an instance of the RecursiveDescentParser by indirectly creating a lexical analyzer.
            self.RDP_parser = parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr))
            # print("Building the parser")
            self.RDP_parser.build()

            self.expr = e.Expression(nvars=self.RDP_parser.variables_index + 1, rdp=self.RDP_parser)
            # print("Obtained expression")
        self.robdd = robdd.ROBDD(nvars=self.args.nvars, expr=self.expr)
        # print("Formed robdd")
    def apply(self):

        self.RDP_parsers = [parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr1)), \
                            parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr1))]

        self.expressions = [e.Expression(self.RDP_parsers[0].variables_index + 1, self.RDP_parsers[0]), \
                            e.Expression(self.RDP_parsers[1].variables_index + 1, self.RDP_parsers[1])]

        self.robdds = [robdd.ROBDD(self.expressions[0]), robdd.ROBDD(self.expressions[1])]

        u, rbd = utils.Apply(self.args.op, self.robdds[0].build(), self.robdds[1].build(), self.robdds[0], self.robdds[1])

    def build(self):

        return self.robdd.Build()
