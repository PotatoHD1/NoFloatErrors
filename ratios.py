from math import gcd, lcm


class LongFloat(object):
    @staticmethod
    def get_count(a):
        if a == 0:
            return 0
        if str(a).__contains__("."):
            if not str(a).__contains__("e"):
                leng = len(str(a).split('.')[1])
            else:
                tmp = str(a).split('.')[1].split('e')
                leng = len(tmp[0]) - int(tmp[1])
        else:
            if not str(a).__contains__("e"):
                leng = 0
            else:
                leng = -int(str(a).split('e')[1])
        return leng

    @staticmethod
    def to_tuple(a):
        if type(a) == tuple:
            return a
        m_a = LongFloat.get_count(a)
        if str(a).__contains__("e"):
            res = str(a).replace(".", "").split('e')[0]
        else:
            res = str(a).replace(".", "")
        return (m_a, int(res))

    @staticmethod
    def remove_zeros(m_p, m):
        if m != 0:
            while m % 10 == 0:
                m_p -= 1
                m //= 10
        else:
            m_p = 0
        return m_p, m

    def __init__(self, a):
        if type(a) == type(self):
            self.a, self.b = a.asTuple()
        elif type(a) == tuple:
            self.a, self.b = a
        else:
            m_p, m = self.to_tuple(a)
            m_p, m = self.remove_zeros(m_p, m)
            self.a, self.b = self.as_integer_ratio(m, m_p)

    @staticmethod
    def as_integer_ratio(m, m_p):
        a = m
        if m_p > 0:
            b = 10 ** m_p
        else:
            a *= 10 ** (-m_p)
            b = 1
        c = gcd(a, b)
        a //= c
        b //= c
        return a, b

    def __reduce__(self):
        c = gcd(self.a, self.b)
        self.a //= c
        self.b //= c
        return self

    def __add__(self, other):
        a, b = self.a, self.b
        a_other, b_other = LongFloat(other).asTuple()
        c = lcm(b, b_other)
        a *= c // b
        a_other *= c // b_other
        return LongFloat((a + a_other, c)).__reduce__()

    def __mul__(self, other):
        a_other, b_other = LongFloat(other).asTuple()
        return LongFloat((self.a * a_other, self.b * b_other)).__reduce__()

    def __truediv__(self, other):
        a_other, b_other = LongFloat(other).asTuple()
        if a_other < 0:
            a_other *= -1
            b_other *= -1
        return LongFloat((self.a * b_other, self.b * a_other)).__reduce__()

    def __pow__(self, other):
        a, b = LongFloat(other).asTuple()
        if b != 1:
            print("Степень должна быть целым числом")
            return 0
        if a >= 0:
            return LongFloat((self.a ** a, self.b ** a)).__reduce__()
        else:
            a *= -1
            return LongFloat((self.b ** a, self.a ** a)).__reduce__()

    def __abs__(self):
        return LongFloat((abs(self.a), self.b))

    def __mod__(self, other):
        res = self / LongFloat(other)
        res = res.asTuple()
        res = LongFloat((res[0] % res[1], res[1]))
        return res

    def __divmod__(self, other):
        res = self / LongFloat(other)
        res = res.asTuple()
        res = float(LongFloat((res[0] % res[1], res[1]))), float(LongFloat((res[0] // res[1], 1)))
        return res

    def __floordiv__(self, other):
        res = self / LongFloat(other)
        res = res.asTuple()
        res = LongFloat((res[0] // res[1], 1))
        return res

    def __reversed__(self):
        return LongFloat(1) / self

    def __neg__(self):
        return LongFloat((-self.a, self.b))

    def __sub__(self, other):
        return self + (-LongFloat(other))

    def __eq__(self, other):
        if isinstance(other, (int, float, type(self), tuple)):
            return LongFloat(other).asTuple() == self.asTuple()
        else:
            return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, (int, float, type(self), tuple)):
            return (self - LongFloat(other)).asTuple()[0] < 0

    def __le__(self, other):
        if isinstance(other, (int, float, type(self), tuple)):
            return (self - LongFloat(other)).asTuple()[0] <= 0

    def __gt__(self, other):
        if isinstance(other, (int, float, type(self), tuple)):
            return (self - LongFloat(other)).asTuple()[0] > 0

    def __ge__(self, other):
        if isinstance(other, (int, float, type(self), tuple)):
            return (self - LongFloat(other)).asTuple()[0] >= 0

    def asTuple(self):
        return (self.a, self.b)

    def __int__(self):
        return self.__floordiv__(1).asTuple()[0]

    def __float__(self):
        return self.a / self.b

    def __str__(self):
        return f"LongFloat({self.a} / {self.b} = {self.a / self.b})"


a = LongFloat(0)
b = LongFloat(3)
print(int(LongFloat(2.5)))
