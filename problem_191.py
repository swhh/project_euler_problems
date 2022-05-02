"""A particular school offers cash rewards to children with good attendance and punctuality. If they are absent for three consecutive days or late on more than one occasion then they forfeit their prize.

During an n-day period a trinary string is formed for each child consisting of L's (late), O's (on time), and A's (absent).

Although there are eighty-one trinary strings for a 4-day period that can be formed, exactly forty-three strings would lead to a prize:

OOOO OOOA OOOL OOAO OOAA OOAL OOLO OOLA OAOO OAOA
OAOL OAAO OAAL OALO OALA OLOO OLOA OLAO OLAA AOOO
AOOA AOOL AOAO AOAA AOAL AOLO AOLA AAOO AAOA AAOL
AALO AALA ALOO ALOA ALAO ALAA LOOO LOOA LOAO LOAA
LAOO LAOA LAAO

How many "prize" strings exist over a 30-day period?"""


def number_prize_strings(days):
    string_number = pow(3, days)
    three_or_more_consecutive_absence = 0
    three_or_more_absence_and_two_or = 0
    for k in range(days - 2):
        power = days - 3 - k
        subtotal = pow(2, k) * pow(3, power)
        three_or_more_consecutive_absence += subtotal
        new_subtotal = subtotal - (k + 1) * pow(2, power)
        new_subtotal -= power * pow(2, power - 1)
        three_or_more_absence_and_two_or += new_subtotal

    fewer_than_two_late = pow(2, days) + days * pow(2, days - 1)
    two_or_more_late = string_number - fewer_than_two_late

    return string_number - two_or_more_late - three_or_more_consecutive_absence + three_or_more_absence_and_two_or


print(number_prize_strings(4))