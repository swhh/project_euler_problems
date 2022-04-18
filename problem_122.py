import math
"""
The most naive way of computing n15 requires fourteen multiplications:

n × n × ... × n = n15

But using a "binary" method you can compute it in six multiplications:

n × n = n2
n2 × n2 = n4
n4 × n4 = n8
n8 × n4 = n12
n12 × n2 = n14
n14 × n = n15

However it is yet possible to compute it in only five multiplications:

n × n = n2
n2 × n = n3
n3 × n3 = n6
n6 × n6 = n12
n12 × n3 = n15

We shall define m(k) to be the minimum number of multiplications to compute nk; for example m(15) = 5.

For 1 ≤ k ≤ 200, find ∑ m(k).

"""


def min_multiply_sum(z):
    """Return ∑ m(k) for 1 ≤ k ≤ z where z > 8"""
    # if x is a power of 2
    l = math.log2(z)
    k = int(math.floor(l))
    total = 0

    for i in range(1, k + 1):
        total += (i * len_min_multiple(i))
    if l - k:  # if z not a power of 2, add to total; two cases: 1. m(z) = k + 1 2. m(z) = k + 2 for k >= 4
        x, y = calc_x_and_y(k + 1)
        if x <= z <= y:  # case 2a
            total += ((k + 1) * len_min_multiple(k + 1))
            if z == x:
                return total - (2 * (k + 1))
            if z == y:
                return total - (k + 1)
            total += ((z - x) * (k + 2))
        elif y < z < pow(2, k + 1):  #case 2b
            total += ((k + 1) * len_min_multiple(k + 1))
            total += ((y - x) + (z - y) - 1) * (k + 2)
        else:  # case 1
            missing = calculate_missing(k)
            total += (missing * (k + 1))
            total += ((z - pow(2, k)) * (k + 1))

    return total


def calc_x_and_y(power):
    """Calculate the values x and y for which x < k < y, m(k) == power + 1"""
    x = 11 * (pow(2, power - 4))
    y = 12 * (pow(2, power - 4))
    return x, y


def calculate_missing(power):
    """Calculate the size of the set of numbers k for which log(ceil(k)) = power and m(k) = power + 1"""
    if power == 3:
        return 1
    x, y = calc_x_and_y(power)
    z = (y - x) + (pow(2, power) - y) - 2
    return z


def len_min_multiple(power):
    """Calculate the size of set of numbers {k: m(k) = power}"""
    if power < 4:
        return power
    z = calculate_missing(power)
    earlier_z = calculate_missing(power - 1)
    return earlier_z + pow(2, power - 1) - z


def test():
    assert min_multiply_sum(32) == 93
    assert min_multiply_sum(16) == 38
    assert min_multiply_sum(18) == 25 + min_multiply_sum(16)
    assert min_multiply_sum(15) == 15 + min_multiply_sum(16)
    assert min_multiply_sum(24) == min_multiply_sum(32) - 5
    assert min_multiply_sum(22) == min_multiply_sum(32) - 10


if __name__ == '__main__':
    test()
    print(min_multiply_sum(200))

