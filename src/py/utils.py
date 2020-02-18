'''
General helper classes and functions.

Class: RDP_node -> A node in the RecursiveDescentParser.
Also implements the Apply and Restrict utilities as functions that operate on ROBDD objects.
'''

import robdd

class RDP_node:
    '''A single node in a Recursive Descent Parser.'''
    def __init__(self, val=None, type='', is_terminal=False, is_var=False, var_index=-1, is_func=False):
        '''Note: is_var, is_terminal and is_func are now deprecated in light of type and are kept for backward compatibility.'''
        self.val = val # The value at this node. Can be either a constant, variable or boolean function.
        self.left, self.right = None, None # left and right nodes of type RDP_node

        self.type = type  # Either of ['const', 'var', 'func']
        # Below variables are (mostly) deprecated.
        self.is_terminal = is_terminal
        self.is_var = is_var
        self.var_index = var_index
        self.is_func = is_func

def apply(op: str, lexpr: int, rexpr=None) -> int:
    '''This is NOT the Apply utility from Anderon's paper. This function simply takes in two constants and returns the result of the required boolean operation.'''

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
    '''The Apply utility from Anderson's paper.
    u_1 and u_2 are root values of the nodes of the 2 ROBDDs.
    op: The operator to be applied on the two expressions.
    rbd1 and rbd2 are ROBDD objects to be combined.
    rbd (optional) is the ROBDD object to be returned.'''
    G = dict() # For Dynamic programming

    if not rbd:
        rbd = robdd.ROBDD(nvars=rbd1.nvars) # rbd is an uninitialized ROBDD

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

    rbd = robdd.ROBDD(nvars=rbd1.nvars) # Removing one less variable constraint since a variable with smaller index can be removed as well

    def restrict(u):

        if rbd1.var_T(u) > j:
            rbd.Mk(rbd1.var_T(u), rbd1.low_T(u), rbd1.high_T(u))
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
        for i in rbd1.T.keys():
            if rbd1.var_T(i) != j:
                rt = restrict(i)

        for key in rbd.T.copy().keys(): # Remove any keys greater than the new root
            if key > rt:
                del rbd.T[key]

        ref_keys = []
        for key in sorted(rbd.T.keys()): # Collect only referenced keys
            if key > 1:
                ref_keys.extend([rbd.T[key][1], rbd.T[key][2]])

        ref_keys = list(set(ref_keys))
        for _ in rbd.T.copy().keys(): # Remove unrefenced keys
            if _ in ref_keys or _ == rt:
                continue
            del rbd.T[_]


    return rbd

def print_neat_T(r):
    '''Some sugarcoat to print the T table for an ROBDD neatly.'''
    print("| u | i |  l |  h |")

    for _ in sorted(r.T.keys()):
        print("| {0} | {1} | {2} | {3} |".format(_, r.T[_][0], r.T[_][1], r.T[_][2]))
    print()

def print_neat_allsat(tup, nvars):
    '''Print all the satisfying assignments returned by ROBDD.AllSat nicely.'''
    for _ in tup:
        pass
