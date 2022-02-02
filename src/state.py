from util import *
import enum


class Action(enum.Enum):
    throw = 1
    score = 2
    bank = 3

    farkle = 4
    hotDice = 5


class State(object):
    """
    Basic class of game information.

    One state corresponds to one player, it includes all the information of a game moment.
    When the game advances, an instance of State develop to the next State,
    and there are 3 actions (throw, score, bank) to realize it.

    How to use:
    self.next_states: to get the list of possible next state
    (could be developed by action throw, score or bank, it depends on the variable need_to_score)
    self.action_throw: to get the next state after executing the action throw. Score, bank too.

    Attributes:
        state_dice: information of dice state
        last_action: last action
        score: score obtained in this turn
        score_total: total score that has been banked
        need_to_score: if it is necessary to score a combo in the current state
        turn_is_over: if this turn has overed
    """

    def __init__(self, state_dice: StateDice, last_action: Action = None, score=0, score_total=0, turn_is_over=False,
                 need_to_score=False):
        self.state_dice = state_dice
        self.last_action = last_action
        self.score = score
        self.score_total = score_total
        self.need_to_score = need_to_score
        self.turn_is_over = turn_is_over

    def __repr__(self):
        res = str(self.state_dice) + ', last_action: ' + str(self.last_action) + ", score: " + str(
            self.score) + ", score total: " + str(self.score_total)
        res += ", need to score: " + str(self.need_to_score) + ", turn_is_over: " + str(self.turn_is_over)
        return res

    @property
    def available_combos(self):
        """
        Get all the possible combo dices without combination
        :return: list of string  e.g. ['1', '5']
        """
        if self.need_to_score:
            combos = [combo for combo in POINTS if combo in self.state_dice.remaining_dice]
            return [combo for combo in combos]
        else:
            return []

    @property
    def next_states(self):
        """
        Develop to the next state of game
        :return: list of State
        """
        if self.need_to_score:
            combined_combos = combination(self.available_combos)
            # list of tuple of string  e.g. [('1'), ('5'), ('1', '5')]
            return [self.action_score(combo) for combo in combined_combos]
        else:
            return [self.action_throw(), self.action_bank()]

    @property
    def game_over(self):
        return TARGET_SCORE <= self.score_total

    def action_throw(self):
        """
        Action to throw the dices
        :return: next state after throwing
        """
        if self.state_dice.number_of_remaining() == 0:
            new_remaining_dice = roll_dice(6)
        else:
            new_remaining_dice = roll_dice(self.state_dice.number_of_remaining())
        new_state_data = StateDice(new_remaining_dice, self.state_dice.scoring_dice)
        new_state = State(new_state_data, Action.throw, self.score, self.score_total, need_to_score=True)

        if len(new_state.available_combos) == 0 and len(new_state.state_dice.remaining_dice) != 0:
            # Farkle !
            return State(StateDice(roll_dice(6), []), Action.farkle, score=0, score_total=self.score_total,
                         need_to_score=True, turn_is_over=True)
        else:
            return new_state

    def action_score(self, scoring_combos: tuple[str]):
        """
        Action to score selected dices.
        Move the selected dices (scoring_combos) from remaining_dice to scoring_dice.

        :param scoring_combos: e.g. ['1', '5'], ['1'] or ['5']
        :return: next state after scoring
        """
        new_remaining_dice = self.state_dice.remaining_dice
        new_scoring_dice = self.state_dice.scoring_dice + list(scoring_combos)
        new_score = self.score

        temp_score = 0
        for scoring_combo in scoring_combos:
            new_remaining_dice = new_remaining_dice.replace(scoring_combo, '', 1)
            new_score += POINTS[scoring_combo]
            temp_score += POINTS[scoring_combo]

        new_state_data = StateDice(new_remaining_dice, new_scoring_dice, scoring_combos, temp_score)
        new_state = State(new_state_data, Action.score, new_score, self.score_total)

        if len(new_state.state_dice.remaining_dice) == 0:
            # Hot dice!
            return State(StateDice(roll_dice(6), [], scoring_combos, temp_score), Action.hotDice, new_state.score,
                         self.score_total,
                         need_to_score=True)
        else:
            return new_state

    def action_bank(self):
        """
        Action to bank the score
        :return: end state with total score
        """
        new_score_total = self.score + self.score_total
        return State(StateDice(roll_dice(6), []), Action.bank, score=0, score_total=new_score_total,
                     need_to_score=True, turn_is_over=True)

    def action_farkle(self):
        return State(StateDice(roll_dice(6), []), Action.farkle, score=0, score_total=self.score_total,
                     need_to_score=True, turn_is_over=True)

    def pop(self):
        return self.next_states
