
import utils
import math

class ROBDD:

    def __init__(self, nvars=None, expr=None):

        self.T = dict()
        self.T_len = 0
        self.H = dict()
        self.__init_T()
        self.root_u = -1

        self.nvars = nvars
        self.expr = expr
        if self.expr:
            self.build_initialized = True
        else:
            sel.build_initialized = False

    def __init_T(self):
        self.T[0] = (self.nvars + 1, -1, -1)
        self.T[1] = (self.nvars + 1, -1, -1)
        self.T_len = 2

    def __init_H(self):
        self.H = dict()

    def __add_T(self, i, l, h) -> int:

        self.T[self.T_len] = (i, l, h)
        self.T_len += 1
        return int(self.T_len - 1)

    def var_T(self, u: int) -> int:

        try:
            return self.T[u][0]
        except:
            return None

    def low_T(self, u: int) -> int:

        try:
            return self.T[u][1]
        except:
            return None

    def high_T(self, u: int) -> int:

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

        try:
            val = int(self.H[str(i) + str(',') + str(l) + str(',') + str(h)])
        except KeyError:
            return None

        return val

    def __insert_H(self, i, l, h, u):

        self.H[str(i) + str(',') + str(l) + str(',') + str(h)] = u

    def Mk(self, i: int, l: int, h: int) -> int:

        if l == h:
            return l

        if self.__member_H(i, l, h):
            return __lookup_H(i, l, h)

        u = self.__add_T(i, l, h)

        self.__insert_H(i, l, h, u)

        return u

    # DEPRECATED
    # helpers for Build follow
    # def __init_build(self):
    #
    #     # Either use the Expression API from expression.py or the RDP API from parsing.py
    #     self.expr = Expression(4, use_rdp=self.use_rdp)
    #     self.nvars = 4
    #     self.build_initialized = True

    def Build(self, expr=None):

        if not self.build_initialized and expr:
             # self.__init_build(self)
             self.expr = expr

         if not self.nvars and nvars:
             self.nvars = nvars
             self.__init_T()
             self.__init_H()

        def build_util(i):
            if i > self.nvars:
                expr_val = self.expr.evaluate()
                return 1 if expr_val else 0

            self.expr.x[i] = 0
            v0 = build_util(i + 1)

            self.expr.x[i] = 1
            v1 = build_util(i + 1)

            return self.Mk(i, v0, v1)

        if self.expr:
            return build_util(1)
        else:
            print("Expression not initialized.")
            return None

    def Restrict(self, values=[]): # Call build and save the returned u before calling Restrict.

        assert len(values) > 0

        def restrict(u, j, b):

            if self.var_T(u) > j:
                return u
            elif self.var_T(u) < j:
                return self.Mk(self.var_T(u), restrict(self.low_T(u), j, b), restrict(self.high_T(u), j, b))
            elif self.var_T(u) == j:
                if b == 0:
                    return restrict(self.low_T(u))
                elif b == 1:
                    return restrict(self.high_T(u))

        for i, val in enumerate(range(values[1:])):
            if val != -1:
                self.root_u = restrict(self.root_u, i + 1, val)

    def StatCount(self, u_=None):

        assert self.root_u != -1

        def count(u):
            if u == 0:
                res = 0
            elif u == 1:
                res = 1
            else:
                res = int(math.pow(2, self.var_T(self.low_T(u)) - self.var_T(u) - 1) * count(self.low_T(u)) \
                          + math.pow(2, self.var_T(self.high_T(u)) - self.var_T(u) - 1) * count(self.high_T(u)))

            return res
        if not u_:
            u_ = self.root_u
        return int(math.pow(2, self.var_T(u_) - 1) * count(u_))

    def AnySat(self, u_=None):

        assert self.root_u != -1
        var_sat = {'var_idx': [], 'val': []}

        def anysat(u):

            if u == 0:
                return None
            elif u == 1:
                return None
            elif self.low_T(u) == 0:
                var_sat['var_idx'].append(self.var_T(u))
                var_sat['val'].append(1)
                anysat(self.high_T(u))
            else:
                var_sat['var_idx'].append(self.var_T(u))
                var_sat['val'].append(0)
                anysat(self.low_T(u))

        if not u_:
            u_ = self.root_u
        anysat(u_)
        return var_sat

    def AllSat(self, u_=None):

        assert self.root_u != -1

        # all_sats = [{'var_idx': [], 'val': []} for _ in range(self.nvars)]
        all_sats = []

        def allsat(u):
            if u == 0:
                return None
            elif u == 1:
                return allsat.extend([{'var_idx': [], 'val': []}])
            else:
                for _ in allsat(self.low_T(u)):
                    _['var_idx'].append(self.var_T(u))
                    _['val'].append(0)
                for _ in allsat(self.high_T(u)):
                    _['var_idx'].append(self.var_T(u))
                    _['val'].append(1)

        if not u_:
            u_ = self.root_u

        allsat(u_)

        return all_sats
