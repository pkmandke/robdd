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
