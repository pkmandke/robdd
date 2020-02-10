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


def Apply(op: str, u_1, u_2):
    '''u_1 and u_2 are RDP_nodes.'''
    G = dict()
    u = robdd.ROBDD() # u is an uninitialized ROBDD 

    def apply_util(u1, u2):

        try:
            return self.G[str(u1) + str(',') + str(u2)]
        except:
            if (int(u1) in [0, 1]) and (int(u2) in [0, 1]):
                u = utils.apply(op, u1, u2)
            elif (u1[0] == u2[0] and u1[0] == 'x') and (u1[1] == u2[1]):
                util
