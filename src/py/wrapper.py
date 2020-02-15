'''
Wrapper class that initializes all others.
'''

import parsing
import robdd
import expression as e
import utils

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

            self.expr = e.Expression(nvars=self.RDP_parser.variables_index, rdp=self.RDP_parser)
            # print("Obtained expression")
        self.robdd = robdd.ROBDD(nvars=self.args.nvars, expr=self.expr)
        # print("Formed robdd")
    def apply(self):

        self.RDP_parsers = [parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr1)), \
                            parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr2))]
        self.RDP_parsers[0].build(), self.RDP_parsers[1].build()

        self.expressions = [e.Expression(nvars=self.RDP_parsers[0].variables_index, rdp=self.RDP_parsers[0]), \
                            e.Expression(nvars=self.RDP_parsers[1].variables_index, rdp=self.RDP_parsers[1])]

        self.robdds = [robdd.ROBDD(nvars=self.args.nvars1, expr=self.expressions[0]),\
                       robdd.ROBDD(nvars=self.args.nvars2, expr=self.expressions[1])]
        self.robdds[0].Build(), self.robdds[1].Build()
        print("Before u1 {0}, u2 {1}".format(self.robdds[0].root_u, self.robdds[1].root_u))
        u, rbd = utils.Apply(self.args.op, self.robdds[0].root_u, self.robdds[1].root_u, self.robdds[0], self.robdds[1])

        return rbd

    def build_robdd(self):

        return self.robdd.Build()

    def stat_utils(self, util='AllSat'):

        return getattr(self.robdd, util)()
