'''
Class ROBDD

This file defines the main ROBDD class.
It also includes such methods as Build, Mk, AnySat, AllSat and StatCount among other private methods.

This class also handles the T and H lookup tables.
These have been defined in the form of Python dictionaries.
'''

import utils
import math

class ROBDD:

    def __init__(self, nvars=None, expr=None):
        '''Custom Constructor.'''

        # Lookup Table T used for storing ROBDD
        self.T = dict()
        self.T_len = 0

        # H table for fast lookup
        self.H = dict()
        self.root_u = -1

        # The expression handled by this ROBDD and it's associated number of variables.
        self.nvars = nvars
        self.expr = expr

        if self.expr:
            self.build_initialized = True
        else:
            self.build_initialized = False

        self.__init_T()


    def __init_T(self):
        '''Initialize T'''
        self.T[0] = (self.nvars + 1, -1, -1)
        self.T[1] = (self.nvars + 1, -1, -1)
        self.T_len = 2

    def __init_H(self):
        '''Initialize H'''
        self.H = dict()

    def __add_T(self, i, l, h) -> int:
        '''Add an entry to T'''
        self.T[self.T_len] = (i, l, h)
        self.T_len += 1
        return int(self.T_len - 1)

    def var_T(self, u: int) -> int:
        '''Get variable of the node numbered u. Return None if this node doesn't exist.'''
        try:
            return self.T[u][0]
        except:
            return None

    def low_T(self, u: int) -> int:
        '''Return low child of node u if it exists.'''
        try:
            return self.T[u][1]
        except:
            return None

    def high_T(self, u: int) -> int:
        '''return high child of node u if it exists.'''
        try:
            return self.T[u][2]
        except:
            return None

    def __member_H(self, i, l, h):
        '''Check if i, l, h entry exists in H.'''
        try:
            _ = self.H[str(i) + str(',') + str(l) + str(',') + str(h)]
        except KeyError:
            return False

        return True

    def __lookup_H(self, i, l, h):
        '''Return the u entry for given i, l, h pair.'''
        try:
            val = int(self.H[str(i) + str(',') + str(l) + str(',') + str(h)])
        except KeyError:
            return None

        return val

    def __insert_H(self, i, l, h, u):
        '''Insert an entry in H.'''
        self.H[str(i) + str(',') + str(l) + str(',') + str(h)] = u

    def Mk(self, i: int, l: int, h: int) -> int:
        '''The Make utility from the Anderson's paper.'''
        if l == h:
            return l

        if self.__member_H(i, l, h):
            return self.__lookup_H(i, l, h)

        u = self.__add_T(i, l, h)

        self.__insert_H(i, l, h, u)

        return u

    def Build(self, nvars=None, expr=None):
        '''The Build utility from the Anderson's paper.'''
        if not self.build_initialized and expr:
            # self.__init_build(self)
            self.expr = expr

        if not self.nvars and nvars:
            self.nvars = nvars
            self.__init_T()
            self.__init_H()

        def build_util(i):
            '''The build sub function that actually does the heavy lifting.'''
            if i > self.nvars:
                expr_val = self.expr.evaluate()
                return 1 if expr_val else 0

            self.expr.x[i] = 0
            v0 = build_util(i + 1)

            self.expr.x[i] = 1
            v1 = build_util(i + 1)

            return self.Mk(i, v0, v1)

        if self.expr:
            self.root_u = build_util(1)
            return self.root_u
        else:
            print("Expression not initialized.")
            return None

    def StatCount(self):
        '''The StatCount method from the Anderson's paper.'''
        assert self.root_u != -1

        def count(u):
            if u == -1:
                print("Error in StatCount; u == -1")
            if u == 0:
                res = 0
            elif u == 1:
                res = 1
            else:
                res = int(math.pow(2, self.var_T(self.low_T(u)) - self.var_T(u) - 1) * count(self.low_T(u)) \
                          + math.pow(2, self.var_T(self.high_T(u)) - self.var_T(u) - 1) * count(self.high_T(u)))
            return res

        return int(math.pow(2, self.var_T(self.root_u) - 1) * count(self.root_u))

    def AnySat(self):
        '''The AnySat method from the Anderson's paper. Returns a single satisfying truth assignment as a tuple.'''
        assert self.root_u != -1

        def anysat(u, tup):

            if u in [-1, 0, 1]:
                return tup
            elif self.low_T(u) == 0:
                tl = list(tup)
                tl[self.var_T(u)] = 1
                tup = tuple(tl)
                return anysat(self.high_T(u), tup)
            else:
                tl = list(tup)
                tl[self.var_T(u)] = 0
                tup = tuple(tl)
                return anysat(self.low_T(u), tup)

        return anysat(self.root_u, tuple([-1 for _ in range(self.nvars + 1)]))

    def AllSat(self):
        '''The AllSat method from the Anderson's paper. Returns all satisfying truth assignments as a tuple of dictionaries.
        Note that don't cares are not exhaustively listed in the return value of this function. These are separately generated from the return value of this method.'''

        assert self.root_u != -1

        def allsat(u, tup):

            if u == 0:
                return tup, 0
            elif u == 1:
                return tup + tuple([{'var_idx': [], 'val': []}]), 1
            else:
                tupL, lowT = allsat(self.low_T(u), tup)
                if lowT:
                    for _ in tupL:
                        _['var_idx'].append(self.var_T(u))
                        _['val'].append(0)
                tupH, highT = allsat(self.high_T(u), tup)
                if highT:
                    for _ in tupH:
                        _['var_idx'].append(self.var_T(u))
                        _['val'].append(1)
                return tupL + tupH, 1 if lowT or highT else 0

        return allsat(self.root_u, tuple())[0]
