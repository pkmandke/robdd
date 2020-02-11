'''
General helper classes and functions.
'''

class RDP_node:

    def __init__(self, val=None, type='', is_terminal=False, is_var=False, var_index=-1, is_func=False):

        self.val = val
        self.left, self.right = None, None

        self.type = type  # Either of ['const', 'var', 'func']
        self.is_terminal = is_terminal
        self.is_var = is_var
        self.var_index = var_index
        self.is_func = is_func

def apply(op: str, lexpr: int, rexpr=None) -> int:

    if op == 'not':
        return 0 is lexpr == 1 else 1

    assert rexpr is not None

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
        rbd = robdd.ROBDD() # rbd is an uninitialized ROBDD

    def apply_util(u1, u2):

        try:
            # if this set of u1, u2 have been cached, just fetch and return.
            u = self.G[str(u1) + str(',') + str(u2)]
            return u
        except:
            if (u1 in [0, 1]) and (u2 in [0, 1]): # If u1 and u2 are constants, peform the op and return result.
                u = utils.apply(op, u1, u2)
            elif rbd1.T[u1][0] == rbd2[u2][0]: # If both u1 and u2 have the same var() value.
                u = rbd.Mk(rbd1.T[u1][0], \
                apply_util(rbd1[u1][1], rbd2[u2][1]), \
                apply_util(rbd1[u1][2], rbd2[u2][2]))
            elif rbd1[u1][0] < rbd2[u2][0]: # If var(u1) < var(u2)
                u = rbd.Mk(rbd1.T[u1][0], \
                apply_util(rbd1[u1][1], u2), \
                apply_util(rbd1[u1][2], u2))
            else: # If var(u1) > var(u2)
                u = rbd.Mk(rbd1.T[u2][0], \
                apply_util(u1, rbd2[u2][1]), \
                apply_util(u1, rbd2[u2][2]))

        self.G[str(u1) + str(',') + str(u2)] = u # Cache this pair of u1 and u2 if niether of the above works.
        return u

    return apply_util(u_1, u_2), u # Return both the root node's 'u' value and the ROBDD object.
