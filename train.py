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
from model import GameRunner
from naive_player import NaivePlayer
from random_player import RandomPlayer
# from minimaxPlayer import MiniMaxPlayer
from rlPlayerTrainer import PlayerTrainer
from utils import *
import random
import numpy as np

## 
# import torch
import random
import numpy as np
import os, sys
from rl_model import Linear_QNet, QTrainer
import tqdm

NETWORK_SIZE = int(sys.argv[1])
model = Linear_QNet(42, NETWORK_SIZE, 1)
trainer = QTrainer(model, lr=0.01, gamma=0.9)

def runGame(n_random=0):
    players = [PlayerTrainer(0, model), RandomPlayer(1), RandomPlayer(2), RandomPlayer(3)]
    # players = [PlayerTrainer(0, model), RandomPlayer(1), RandomPlayer(2), NaivePlayer(3)]
    # players = [RandomPlayer(0), RandomPlayer(1), RandomPlayer(2), RandomPlayer(3)]
    # players = [RandomPlayer(0), RandomPlayer(1), RandomPlayer(2), NaivePlayer(3)]
    gr = GameRunner(players, random.randint(0, 1000000000), model, trainer)
    # gr = GameRunner(players, 592, model, trainer)
    activity = gr.Run(False)

    return [activity[0][0], activity[1][0], activity[2][0], activity[3][0]]

def computeAvg(arr):
    return float(np.sum(arr)) / 1


def main():
    model_basename = f"initial_state_{NETWORK_SIZE}"
    model_name = f"{model_basename}.pth"
    data_path = f"model/{model_basename}.txt"
    if os.path.exists(f"model/{model_name}"):
        print(f"error: model \"{model_name}\" already exists")
        exit()
    
    model_stats = []

    for k in (pbar := tqdm.tqdm(range(1000), dynamic_ncols=True)):
        pbar.set_description(f"Round: {k}")
        
        # totalScores = [0, 0, 0, 0]
        victories = [0, 0, 0, 0]

        # print(f"Round: {k}")
        newScores = runGame(n_random=k)
        victories[newScores.index(max(newScores))] += 1
        # for i in range(len(newScores)):
        #     totalScores[i] += newScores[i]

        # print(victories)
        # print(list(map(computeAvg, totalScores)))
        model_stats.append(f"{newScores[0]},{victories[0]}\n")

        if k % 100 == 0:
            model.save(model_name)
            # print(model.state_dict())
            open(data_path, 'a').writelines(model_stats)
            model_stats.clear()
    
    model.save()
    open(data_path, 'a').writelines(model_stats)
    model_stats.clear()

if __name__ == "__main__":
    main()
