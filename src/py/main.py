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
    test_obj.restrict([-1, 1])

    print("T: {0}, root {1}".format(test_obj.robdd.T, test_obj.robdd.root_u))
main()
