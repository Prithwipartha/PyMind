from math import sqrt


class Vector(list):
    def __init__(self, body=[], length=0, d_type=float):
        if len(body):
            pass
        else:
            body = array_1d(length, d_type)
        list.__init__(self, body)

    def __repr__(self):
        ret = '|'
        for i in self:
            ret += ' ' + str(i)
        ret += ' |'
        return ret

    def __mul__(self, other):
        ret = []
        if type(other) is int or type(other) is float:
            for i in self:
                ret += [i * other]
            return Vector(ret)

        if type(other) is Vector:
            for i in self.range():
                ret += [self[i] * other[i]]
            return Vector(ret)

    def __add__(self, other):
        ret = []
        if type(other) is int or type(other) is float:
            for i in self:
                ret += [i + other]
        elif type(other) is Vector or type(other) is list:
            for i in self.range():
                ret += [self[i] + other[i]]
        return Vector(ret)

    def __matmul__(self, other):
        if type(other) is Vector:
            return vec_vec(self, other)

    def apply(self, function=None, other_iterators=None):
        ret = []
        if type(other_iterators) is Matrix or type(other_iterators) is Vector:
            if type(other_iterators) is Matrix:
                other_iterators = other_iterators.transpose()
            for i in self.range():
                ret += [function(self[i], other_iterators[i])]
        elif other_iterators is None:
            for i in self:
                ret += [function(i)]
        return Vector(ret)

    def range(self):
        return range(len(self))

    def join(self, other):
        return Vector(list(self[:]) + list(other[:]))

    def mean(self):
        return sum(self)/len(self)

    def rms(self):
        return sqrt(sum(self * self)/len(self))


class Matrix(list):
    def __init__(self, body=[], rows=0, columns=0, d_type=float):
        if len(body):
            for i in range(len(body)):
                body[i] = Vector(body[i])
        else:
            body = array_2d(rows, columns, d_type)
            for i in range(len(body)):
                body[i] = Vector(body[i])
        list.__init__(self, body)

    def __repr__(self):
        ret = ''
        for i in self:
            ret += i.__repr__() + '\n'
        return ret

    def __mul__(self, other):
        if type(other) is Vector or type(other) is Matrix:
            return self @ other
        else:
            ret = []
            for i in self:
                ret += [i * other]
            return Matrix(ret)

    def __matmul__(self, other):
        if type(other) is Vector:
            return Vector(mat_vec(self, other))
        elif type(other) is Matrix:
            return Matrix(mat_mat(self, other))

    def __add__(self, other):
        ret = []
        if type(other) is Matrix:
            for i in range(self.rows()):
                ret += [self[i] + other[i]]
        elif type(other) is Vector:
            return self + [other]
        else:
            for i in range(self.rows()):
                ret += [self[i] + other]
        return Matrix(ret)

    def rows(self):
        return len(self)

    def columns(self):
        return len(self[0])

    def transpose(self):
        ret = transpose(self)
        return Matrix(ret)

    def apply(self, function=None, other_iterators=[]):
        ret = []
        if len(other_iterators):
            other_iterators = transpose(other_iterators)
            for i in range(self.rows()):
                ret += [function(self[i], other_iterators[i])]
        else:
            for i in range(self.rows()):
                ret += (function(self[i]))
        return Matrix(ret)


# Array definition functions:


def array_1d(length=0, d_type=float):
    ret = []
    for i in range(length):
        ret += [d_type()]
    return ret


def array_2d(rows=0, columns=0, d_type=float):
    ret = []
    for i in range(rows):
        sub_ret = []
        for j in range(columns):
            sub_ret += [d_type()]
        ret += [sub_ret]
    return ret


def identity_matrix(n=0):
    ret = array_2d(rows=n, columns=n, d_type=int)
    for i in range(n):
        ret[i][i] = 1
    return ret


def negation_matrix(n=0):
    ret = array_2d(rows=n, columns=n, d_type=int)
    for i in range(n):
        ret[i][n - i - 1] = 1
    return ret

# Matrix and Vector multiplication functions:


def transpose(a=[]):
    ret = []
    for i in range(len(a[0])):
        sub_ret = []
        for j in range(len(a)):
            sub_ret += [a[j][i]]
        ret += [sub_ret]
    return ret


def mat_vec(a=[], b=[]):
    ret = []
    for i in range(len(a)):
        ret += [0]
        for j in range(len(a[i])):
            ret[i] += a[i][j] * b[j]
    return ret


def vec_vec(a=[], b=[]):
    ret = 0
    print(a)
    for i in range(len(a)):
        ret += a[i] * b[i]
    return ret


def mat_mat(a=[], b=[]):
    ret = []
    b = transpose(b)
    for i in range(len(a)):
        sub_ret = []
        for j in range(len(b)):
            sub_ret += [0]
            for k in range(len(a[0])):
                sub_ret[j] += a[i][k] * b[j][k]
        ret += [sub_ret]
    return ret


def if_list_loop_it(lists=[], function=None):
    a = 1
    cols = len(lists[0])
    for i in lists:
        if len(i) is not cols:
            a = 0
    if a:
        ret = []
        lists = transpose(lists)
        for i in lists:
            ret += [function(i)]
        return ret
    else:
        print("ERROR:list sizes do not match.")
        raise IndexError
