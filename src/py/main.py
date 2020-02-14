'''

Main trigger script.
'''

from wrapper import Wrapper

def main():

    test_obj = Wrapper(use_rdp=True)

    print("Root is {}".format(test_obj.build()))
    print(test_obj.robdd.H)

main()
