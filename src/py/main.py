'''

Main trigger script.
'''

from wrapper import Wrapper

def main():

    test_obj = Wrapper(use_rdp=True)

    print("Root is {}".format(test_obj.build_robdd()))
    print(test_obj.robdd.T)

    print(test_obj.stat_utils())

    print(test_obj.stat_utils(util='AnySat'))

    print(test_obj.stat_utils(util='StatCount'))

    print("APPLY: ")
    print()

    print(test_obj.apply().T)

    print("RESTRICT: ")
    res_rbd = test_obj.restrict(j=1, b=0)

    print("T: {0}, root {1}".format(res_rbd.T, res_rbd.root_u))
main()
