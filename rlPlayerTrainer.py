# Written by Michelle Blom, 2019
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from model import *
from utils import *
import random
import os, torch
import numpy as np


class PlayerTrainer(Player):
    def __init__(self, _id, model, vector_type):
        super().__init__(_id)
        self.model = model
        self.epsilon = 0.9
        self.vector_type = vector_type

    def SelectMove(self, moves, game_state):
        # Choose Move
        if random.random() < self.epsilon:
            best_move = None
            best_val = float("-inf")
            for m in moves:
                # Get feature vec
                temp_game_state = copy.deepcopy(game_state)
                temp_game_state.ExecuteMove(0, m)
                featureVec = getFeatureVec(temp_game_state, requested_vec=self.vector_type)
                
                # Evaluate and choose best
                state0 = torch.tensor(featureVec, dtype=torch.float)
                val = self.model(state0).item()
                
                if val > best_val:
                    best_val = val
                    best_move = m

            move = best_move
        else:
            move = random.choice(moves)

        return move
    
    def save_model(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
