'''

Main trigger script.
'''

from wrapper import Wrapper

def main():

    test_obj = Wrapper(use_rdp=True)

    print("ROBDD constructed from inout expression. T table is {0} and root node is {1}".format(test_obj.robdd.T, test_obj.build_robdd()))

    print("AllSat utlitity output: {}".format(test_obj.stat_utils()))

    print("AnySat utlitity output: {}".format(test_obj.stat_utils(util='AnySat')))

    print("StatCount utlitity output: {}".format(test_obj.stat_utils(util='StatCount')))

    print("Applying expr1 op expr2 returns:")
    print("ROBDD: {0}.".format(test_obj.apply().T))

    print(test_obj.apply().T)

    res_rbd = test_obj.restrict(j=1, b=0)
    print("RESTRICT returns robdd {0} with root {1}.".format(res_rbd.T, res_rbd.root_u))

main()
