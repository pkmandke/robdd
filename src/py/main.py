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

main()
