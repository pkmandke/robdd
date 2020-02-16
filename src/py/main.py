'''

Main trigger script.
'''

from wrapper import Wrapper
import utils
import sys

def main():

    test_obj = Wrapper(use_rdp=True)

    getattr(sys.modules['__main__'], test_obj.args.call)(test_obj)
    exit(0)
    print("ROBDD constructed from inout expression. T table is {0} and root node is {1}".format(test_obj.robdd.T, test_obj.build_robdd()))

    print("AllSat utlitity output: {}".format(test_obj.stat_utils()))

    print("AnySat utlitity output: {}".format(test_obj.stat_utils(util='AnySat')))

    print("StatCount utlitity output: {}".format(test_obj.stat_utils(util='StatCount')))


    print(test_obj.apply().T)

    res_rbd = test_obj.restrict(j=1, b=0)
    print("RESTRICT returns robdd {0} with root {1}.".format(res_rbd.T, res_rbd.root_u))


def test_build_mk(test_obj):
    test_obj.build_robdd()
    utils.print_neat_T(test_obj.robdd)

def test_apply(test_obj):
    rbd, rbd1, rbd2 = test_obj.apply()
    print("ROBDD of expr 1 is:")
    utils.print_neat_T(rbd1)
    print("ROBDD of expr 2 is:")
    utils.print_neat_T(rbd2)
    print("Applying expr1 op expr2 returns:")
    utils.print_neat_T(rbd)

def test_stats(test_obj):
    print("Working with expr {0}.".format(test_obj.args.expr))
    test_obj.build_robdd()
    utils.print_neat_T(test_obj.robdd)

    
def test_restrict(test_obj):
    test_obj.build_robdd()
    print("Restricting expr {0} with j={1} with value {2}.".format(test_obj.args.expr, test_obj.args.j, test_obj.args.b))
    utils.print_neat_T(test_obj.restrict(test_obj.args.j, test_obj.args.b))

if __name__ == '__main__':
    main()
