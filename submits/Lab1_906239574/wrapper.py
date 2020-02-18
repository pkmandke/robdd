'''
Class: Wrapper
This class helps instantiate the ROBDD, the Lexical Analyzer, the Recursive Descent Parser and the Expression classes.
It also serves as an API for calling the various methods of the ROBDD for verification.

This mainly helps abstract away the need to deal with the various Constructors and setup methods of each class.
'''

import parsing
import robdd
import expression as e
import utils
import math

class Wrapper:

    def __init__(self, use_rdp=True, expr=[]):

        self.expr = expr
        self.args = parsing.Options().parse()
        if use_rdp and self.args.expr:

            # Create an instance of the RecursiveDescentParser by indirectly creating a lexical analyzer.
            self.RDP_parser = parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr))

            self.RDP_parser.build() # Building the parser

            self.expr = e.Expression(nvars=self.args.nvars, rdp=self.RDP_parser)

            self.robdd = robdd.ROBDD(nvars=self.args.nvars, expr=self.expr)
        if self.args.expr1:
            self.RDP_parsers = [parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr1)), \
                                parsing.RecursiveDescentParser(parsing.Lexer(self.args.expr2))]
            self.RDP_parsers[0].build(), self.RDP_parsers[1].build()

            self.expressions = [e.Expression(nvars=self.args.nvars1, rdp=self.RDP_parsers[0]), \
                                e.Expression(nvars=self.args.nvars2, rdp=self.RDP_parsers[1])]

            self.robdds = [robdd.ROBDD(nvars=self.args.nvars1, expr=self.expressions[0]),\
                           robdd.ROBDD(nvars=self.args.nvars2, expr=self.expressions[1])]
            self.robdds[0].Build(), self.robdds[1].Build()


    def apply(self):

        u, rbd = utils.Apply(self.args.op, self.robdds[0].root_u, self.robdds[1].root_u, self.robdds[0], self.robdds[1])

        return rbd, self.robdds[0], self.robdds[1]

    def build_robdd(self):
        '''A wrapper that calls the Build utility of the robdd.'''
        return self.robdd.Build()

    def stat_utils(self, util='AllSat'):
        '''A wrapper that calls statistical utilities of the ROBDD.'''
        return getattr(self.robdd, util)()

    def restrict(self, j: int, b: int):

        return utils.Restrict(self.robdd, self.robdd.root_u, j, b)

    def compute_all_stats(self):

        print("Computing all Statistics for given expression.")
        print("StatCount = {}".format(self.stat_utils('StatCount')))
        print("AnySat: [x1...xN]: {}".format(list(self.stat_utils('AnySat'))[1:]))
        allsats = self.stat_utils('AllSat')

        num = 0
        for sat in allsats:
            if len(sat['var_idx']) < self.args.nvars:
                num += math.pow(2, self.args.nvars - len(sat['var_idx']))
            else:
                num += 1
        print("\nAllSat returns:")
        for _ in allsats:
            print("Variable numbers = {0}. Values: {1}".format(_['var_idx'], _['val']))
        print("Total truth assignments considering don't cares from the above list is {}. This number must be same as StatCount.".format(int(num)))
