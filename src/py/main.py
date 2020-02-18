'''

Main trigger script.

The user must call this script with appropriate commandline arguments.

This script initializes a Wrapper object (from wrapper.py) based on the commandline arguments.

This script consists of various methods named test_*

These methods test various functions of the ROBDDs built in the Wrapper object.

The --call argument is the name of the method (among those defined in this file) that will be called after initializing the Wrapper object.'''


from wrapper import Wrapper
import utils
import sys
import time
from datetime import timedelta

def main():

    test_obj = Wrapper(use_rdp=True)

    getattr(sys.modules['__main__'], test_obj.args.call)(test_obj)

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
    print("Working with expr: {0}".format(test_obj.args.expr))
    test_obj.build_robdd()
    # utils.print_neat_T(test_obj.robdd)
    #print()
    test_obj.compute_all_stats()


def test_restrict(test_obj):
    test_obj.build_robdd()
    print("Restricting expr {0} with j={1} with value {2}.".format(test_obj.args.expr, test_obj.args.j, test_obj.args.b))
    utils.print_neat_T(test_obj.restrict(test_obj.args.j, test_obj.args.b))

def test_time_checks(test_obj):

    t1 = time.monotonic()
    test_obj.build_robdd()
    t2 = time.monotonic()
    print("Build and Make: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.apply()
    t2 = time.monotonic()
    print("Apply: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.restrict(test_obj.args.j, test_obj.args.b)
    t2 = time.monotonic()
    print("Restrict: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.stat_utils(util='StatCount')
    t2 = time.monotonic()
    print("StatCount: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.stat_utils(util='AnySat')
    t2 = time.monotonic()
    print("AnySat: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.stat_utils(util='AllSat')
    t2 = time.monotonic()
    print("AllSat: {}s".format(timedelta(seconds=t2 - t1)))

def test_apply_etal(test_obj):

    t1 = time.monotonic()
    r, _, _ = test_obj.apply()
    t2 = time.monotonic()
    print("Number of nodes in expression 1 {0}.\nNumber of nodes in expression 2 {1}.".format(len(test_obj.robdds[0].T.keys()), len(test_obj.robdds[1].T.keys())))
    print("Apply: {}s".format(timedelta(seconds=t2 - t1)))

def test_restrict_etal(test_obj):

    test_obj.build_robdd()
    print("Number of nodes in the ROBDD = {}".format(len(test_obj.robdd.T.keys())))
    t1 = time.monotonic()
    test_obj.restrict(test_obj.args.j, test_obj.args.b)
    t2 = time.monotonic()
    print("Restrict: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.stat_utils(util='StatCount')
    t2 = time.monotonic()
    print("StatCount: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.stat_utils(util='AnySat')
    t2 = time.monotonic()
    print("AnySat: {}s".format(timedelta(seconds=t2 - t1)))

    t1 = time.monotonic()
    test_obj.stat_utils(util='AllSat')
    t2 = time.monotonic()
    print("AllSat: {}s".format(timedelta(seconds=t2 - t1)))


if __name__ == '__main__':
    main()
