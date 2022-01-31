from state import *


def ai_random_strategy(next_states):
    state = random.choice(next_states)
    return state


def ai_play_turn(state: State):
    while not state.turn_is_over:
        next_states = state.next_states
        if len(next_states) == 0:
            return state.action_farkle()
        state = ai_random_strategy(next_states)
        # print('score: ' + str(state.score) + ', total score: ' + str(state.score_total))
    return state


def play_round(ai_state: State):
    while not ai_state.turn_is_over:
        ai_state = ai_play_turn(ai_state)
    return ai_state


def get_num_round(ai_state: State):
    """
    Simulate
    :param ai_state:
    :return:
    """
    num_round = 1
    while not ai_state.game_over:
        # print('Round ' + str(num_round))
        ai_state = play_round(ai_state)
        num_round += 1
        ai_state.turn_is_over = False
    return num_round


def ai_minMax(ai_state):
    num_win = 0
    num_simulation = 1000
    ai_state1 = ai_state
    ai_state2 = ai_state
    for i in range(num_simulation):
        # define the action we need to test
        ai_state1 = ai_state.action_bank()
        ai_state2 = ai_state.action_throw()

        num_round1 = get_num_round(ai_state1)
        num_round2 = get_num_round(ai_state2)
        if 1/num_round1 > 1/num_round2:
            num_win += 1
    if num_win/num_simulation >= 0.5:
        return ai_state1
    else:
        return ai_state2


def main():
    """
    method for testing AI
    :return:
    """
    print('AI Test:')

    # init state
    # ai_state = State(StateDice('', [])).action_throw()

    # simulate throw state
    combo = '5'
    ai_state = State(StateDice('224455', []), need_to_score=True).action_score(combo)

    print(ai_minMax(ai_state).last_action)
    # print(str(num_round))


if __name__ == "__main__":
    main()
