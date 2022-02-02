import random
import math
from itertools import combinations
from collections import OrderedDict


TARGET_SCORE = 2000
POINTS = OrderedDict((
    ('123456', 1500),
    ('12345', 500),
    ('23456', 700),
    ('11111', 4000),
    ('66666', 2400),
    ('55555', 2000),
    ('44444', 1600),
    ('33333', 1200),
    ('22222', 800),
    ('1111', 2000),
    ('6666', 1200),
    ('5555', 1000),
    ('4444', 800),
    ('3333', 600),
    ('2222', 400),
    ('111', 1000),
    ('666', 600),
    ('555', 500),
    ('444', 400),
    ('333', 300),
    ('222', 200),
    ('1', 100),
    ('5', 50),
))


def roll_dice(num):
    """
    Simulate dice roll
    :param num: number of dice
    :return: collection of dice represented by string, e.g. '123456'
    """
    return ''.join(sorted(str(random.randint(1, 6)) for _ in range(num)))


class StateDice(object):
    """
    This class stores information of dice state.

    The difference between scoring_dice and temp_dice is that scoring_dice can be stored in the next state data,
    but not for temp_dice. Basically using in the interaction of the user.

    Attributes:
        remaining_dice: dices that still can be thrown
        scoring_dice: type list[str], dices that have been selected and scored
        temp_dice: dices that have been selected only in the current state
        temp_score: score according to the sum of temp_dice
    """

    def __init__(self, remaining_dice: str, scoring_dice: list[str], temp_dice=None, temp_score=None):
        self.remaining_dice = remaining_dice
        self.scoring_dice = scoring_dice
        self.temp_dice = temp_dice
        self.temp_score = temp_score

    def __repr__(self):
        return "remaining dice: " + self.remaining_dice + ", scoring dice: " + str(self.scoring_dice)

    def number_of_remaining(self):
        return len(self.remaining_dice)

    def number_of_scoring(self):
        return len(self.scoring_dice)


def verify_combo(t: tuple[str]):
    """
    Make sure that the combo of tuple are not duplicated
    :param t: e.g. ('1', '5', '15') or ('12345', '1', '5') or ('111', '1')
    :return:
    """
    for i in range(0, len(t)):
        for j in range(i + 1, len(t)):
            if t[i] in t[j] or t[j] in t[i]:
                return False
    return True


def combination(original_list: list[str]):
    """
    Combination of list, using for find possible combos.

    Because list_combinations is a list of tuple, so we need to transform the variable to list_result
    (list of string)
    :param original_list:       e.g. ['1', '5']
    :return: list[tuple(str)]   e.g. ['1', '5', '15']
    """
    list_combinations = []
    for n in range(1, len(original_list) + 1):
        combos = combinations(original_list, n)
        for combo in combos:
            if verify_combo(combo):
                list_combinations.append(combo)
    return list_combinations


def sigmoid(z):
    return 1/(1+math.exp(-2*z))
