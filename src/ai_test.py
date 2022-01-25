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


def main():
    print('Farkle AI Test:')
    ai_state = State(StateDice('', [])).action_throw()
    num_round = get_num_round(ai_state)

    print(str(num_round))


if __name__ == "__main__":
    main()
