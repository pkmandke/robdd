'''
General helper classes and functions.
Also implements the Apply and Restrict utilities as functions that operate on ROBDD objects.
'''

import robdd

class RDP_node:
    '''A single node in a Recursive Descent Parser.'''
    def __init__(self, val=None, type='', is_terminal=False, is_var=False, var_index=-1, is_func=False):

        self.val = val
        self.left, self.right = None, None

        self.type = type  # Either of ['const', 'var', 'func']
        self.is_terminal = is_terminal
        self.is_var = is_var
        self.var_index = var_index
        self.is_func = is_func

def apply(op: str, lexpr: int, rexpr=None) -> int:

    assert lexpr in [0, 1]
    if op == 'not':
        return 0 if lexpr == 1 else 1

    assert rexpr is not None
    assert rexpr in [0, 1]

    if op == 'and':
        return 1 if lexpr and rexpr else 0
    elif op == 'or':
        return 1 if lexpr or rexpr else 0
    elif op == 'imp':
        return 0 if (lexpr == 1) and (rexpr == 0) else 1
    elif op == 'equiv':
        return 1 if lexpr == rexpr else 0


def Apply(op: str, u_1: int, u_2: int, rbd1, rbd2, rbd=None):
    '''u_1 and u_2 are root values of the nodes of the 2 ROBDDs.'''
    G = dict()

    if not rbd:
        rbd = robdd.ROBDD(nvars=rbd1.nvars + rbd2.nvars) # rbd is an uninitialized ROBDD

    def apply_util(u1, u2):

        try:
            # if this set of u1, u2 have been cached, just fetch and return.
            u = G[str(u1) + str(',') + str(u2)]
            return u
        except:
            if (u1 in [0, 1]) and (u2 in [0, 1]): # If u1 and u2 are constants, peform the op and return result.
                u = apply(op, u1, u2)
            elif rbd1.var_T(u1) == rbd2.var_T(u2): # If both u1 and u2 have the same var() value.
                u = rbd.Mk(rbd1.var_T(u1), \
                apply_util(rbd1.low_T(u1), rbd2.low_T(u2)), \
                apply_util(rbd1.high_T(u1), rbd2.high_T(u2)))
            elif rbd1.var_T(u1) < rbd2.var_T(u2): # If var(u1) < var(u2)
                u = rbd.Mk(rbd1.var_T(u1), \
                apply_util(rbd1.low_T(u1), u2), \
                apply_util(rbd1.high_T(u1), u2))
            else: # If var(u1) > var(u2)
                u = rbd.Mk(rbd2.var_T(u2), \
                apply_util(u1, rbd2.low_T(u2)), \
                apply_util(u1, rbd2.high_T(u2)))

        G[str(u1) + str(',') + str(u2)] = u # Cache this pair of u1 and u2 if niether of the above works.
        return u

    return apply_util(u_1, u_2), rbd # Return the root node's 'u' value and the ROBDD object.

def Restrict(rbd1, u, j, b):
    '''
    Returns a new ROBDD object formed by restricting rbd1 by the given condition b on variable j.
    This is not a method of a given ROBDD but a function that is applied on it.
    '''
    assert j > 0
    assert b in [0, 1]

    rbd = robdd.ROBDD(nvars=(rbd1.nvars - 1)) # Create a new robdd with 1 less variable than the original.

    def restrict(u):

        if rbd1.var_T(u) > j:
            u = rbd.Mk(rbd1.var_T(u), rbd1.low_T(u), rbd1.high_T(u))
            return u
        elif rbd1.var_T(u) < j:
            return rbd.Mk(rbd1.var_T(u), restrict(rbd1.low_T(u)), restrict(rbd1.high_T(u)))
        elif rbd1.var_T(u) == j:
            if b == 0:
                return restrict(rbd1.low_T(u))
            elif b == 1:
                return restrict(rbd1.high_T(u))

    if rbd1.root_u == 0:
        rbd.root_u = 0
    elif rbd1.root_u == 1:
        rbd.root_u = 1
    else:
        rbd.root_u = restrict(rbd1.root_u)

    return rbd

def print_neat_T(r):

    print("| u | i |  l |  h |")

    for _ in sorted(r.T.keys()):
        print("| {0} | {1} | {2} | {3} |".format(_, r.T[_][0], r.T[_][1], r.T[_][2]))
    print()

def print_neat_allsat(tup, nvars):

    for _ in tup:
        pass
