

class Expression:

    def __init__(self, nvars: int, use_rdp=True, rdp=None):

        self.nvars = nvars
        self.use_rdp = use_rdp
        if use_rdp:
            self.rdp = rdp

        self.x = [-1 for _ in range(self.nvars + 1)]

    @staticmethod
    def __and(a, b):
        if a == -1 or b == -1:
            print("In AND utility, one of the variables was -1.")
            return None
        return 1 if a and b else 0

    @staticmethod
    def __or(a, b):
        if a == -1 or b == -1:
            print("In OR utility, one of the variables was -1.")
            return None
        return 1 if a or b else 0

    @staticmethod
    def __not(a):
        if a == -1:
            print("In NOT utility, the input variables was -1.")
            return None
        return 0 if a else 1

    @staticmethod
    def __impl(a, b):
        if a == -1 or b == -1:
            print("In IMPL utility, one of the variables was -1.")
            return None
        return 0 if (a == 1) and (b == 0) else 1

    @staticmethod
    def __equiv(a, b):
        if a == -1 or b == -1:
            print("In EQUIV utility, one of the variables was -1.")
            return None
        return 1 if a == b else 0

    def evaluate(self):
        if self.use_rdp and self.rdp:
            return self.rdp.parse_tree(self.x)
        else:
            '''Hard code an expression here.'''
            return Expression.__not(Expression.__and(self.x[1], Expression.__equiv(Expression.__or(self.x[4], self.x[2]), self.x[3])))
