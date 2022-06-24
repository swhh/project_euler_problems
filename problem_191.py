from functools import cache

"""A particular school offers cash rewards to children with good attendance and punctuality. If they are absent for three consecutive days or late on more than one occasion then they forfeit their prize.

During an n-day period a trinary string is formed for each child consisting of L's (late), O's (on time), and A's (absent).

Although there are eighty-one trinary strings for a 4-day period that can be formed, exactly forty-three strings would lead to a prize:

OOOO OOOA OOOL OOAO OOAA OOAL OOLO OOLA OAOO OAOA
OAOL OAAO OAAL OALO OALA OLOO OLOA OLAO OLAA AOOO
AOOA AOOL AOAO AOAA AOAL AOLO AOLA AAOO AAOA AAOL
AALO AALA ALOO ALOA ALAO ALAA LOOO LOOA LOAO LOAA
LAOO LAOA LAAO

How many "prize" strings exist over a 30-day period?"""


def remove(numbers, k_consecutive):
    power = numbers - k_consecutive + 1
    sub_result = sum(pow(numbers, power - j) * scs(j - 2, numbers, k_consecutive) for j in range(k_consecutive + 2, power + 1))
    return (numbers - 1) * sub_result


@cache
def scs(length, numbers, k_consecutive):
    """Calculate no of sequences with at least k_consecutive-length single char subsequence for string of length
    and numbers of chars e.g. no of sequences with at least one 'AAA'"""
    if k_consecutive > length:
        return 0
    if length == k_consecutive:
        return 1
    power = length - k_consecutive
    total = pow(numbers, power)
    total += (numbers - 1) * pow(numbers, power - 1) * power
    if k_consecutive >= length / 2:
        return total
    to_remove = remove(numbers, k_consecutive)
    total -= to_remove
    return total


def number_prize_strings(days):
    fewer_than_two_late_and_fewer_than_three_absences = pow(2, days) - scs(days, 2, 3)
    fewer_than_two_late_and_fewer_than_three_absences += days * pow(2, days - 1)
    for j in range(days):
        subtotal = scs(j, 2, 3) * pow(2, days - 1 - j)
        subtotal += (scs(days - 1 - j, 2, 3) * (pow(2, j) - scs(j, 2, 3)))
        fewer_than_two_late_and_fewer_than_three_absences -= subtotal
    return fewer_than_two_late_and_fewer_than_three_absences


print(number_prize_strings(4))