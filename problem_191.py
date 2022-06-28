from functools import cache
import itertools

"""A particular school offers cash rewards to children with good attendance and punctuality. If they are absent for three consecutive days or late on more than one occasion then they forfeit their prize.

During an n-day period a trinary string is formed for each child consisting of L's (late), O's (on time), and A's (absent).

Although there are eighty-one trinary strings for a 4-day period that can be formed, exactly forty-three strings would lead to a prize:

OOOO OOOA OOOL OOAO OOAA OOAL OOLO OOLA OAOO OAOA
OAOL OAAO OAAL OALO OALA OLOO OLOA OLAO OLAA AOOO
AOOA AOOL AOAO AOAA AOAL AOLO AOLA AAOO AAOA AAOL
AALO AALA ALOO ALOA ALAO ALAA LOOO LOOA LOAO LOAA
LAOO LAOA LAAO

How many "prize" strings exist over a 30-day period?"""


def brute_force_prize_string_count(days):
    count = 0
    for seq in itertools.product('ALO', repeat=days):
        str_seq = ''.join(seq)
        if 'AAA' not in str_seq:
            if str_seq.count('L') < 2:
                count += 1
    return count


@cache
def tribo(n):
    """Version of the Tribonacci numbers to calculate no of binary strings of length n
    with fewer than 3 consecutive 111"""
    if n < 3:
        return pow(2, n)
    return sum(tribo(n - i) for i in range(1, 4))


def number_prize_strings(days):
    fewer_than_two_late_and_fewer_than_three_absences = tribo(days)
    for j in range(days):
        subtotal = tribo(j) * tribo(days - 1 - j)
        fewer_than_two_late_and_fewer_than_three_absences += subtotal
    return fewer_than_two_late_and_fewer_than_three_absences


def test():
    for i in range(4, 10):
        assert brute_force_prize_string_count(i) == number_prize_strings(i)


if __name__ == '__main__':
    test()