from advanced import *
from my_algorithm.Minimax import *


class MiniMaxPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)

    def SelectMove(self, moves, game_state):
        # No need to think if only one move is provided
        selector = Minimax(self.id, game_state, moves)
        return selector.FindNextMove()
