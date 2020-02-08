

class Expression:

    def __init__(self, nvars: int):

        self.nvars = nvars
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

    def function():
        return Expression.__not(Expression.__and(x[1], Expression.__equiv(Expression.__or(x[4], x[2]), x[3])))
