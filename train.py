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

if len(sys.argv) != 4:
    print("usage: python train.py {network size} {feature vector type} {num layers}")
    exit()

NETWORK_SIZE = int(sys.argv[1])
FEATURE_VEC = str(sys.argv[2])
NUM_LAYERS = int(sys.argv[3])
if FEATURE_VEC == "initial":
    NETWORK_INPUT_SIZE = 42
elif FEATURE_VEC == "no_matrix":
    NETWORK_INPUT_SIZE = 20
elif FEATURE_VEC == "no_floor":
    NETWORK_INPUT_SIZE = 35
else:
    print(f"error: uknown feature vector type {FEATURE_VEC}")
    exit()
model = Linear_QNet(NETWORK_INPUT_SIZE, NETWORK_SIZE, 1)
trainer = QTrainer(model, lr=0.01, gamma=0.9)

def runGame(n_random=0):
    # players = [PlayerTrainer(0, model, FEATURE_VEC), RandomPlayer(1), RandomPlayer(2), RandomPlayer(3)]
    players = [PlayerTrainer(0, model, FEATURE_VEC), NaivePlayer(1), RandomPlayer(2), RandomPlayer(3)]
    # players = [RandomPlayer(0), RandomPlayer(1), RandomPlayer(2), RandomPlayer(3)]
    # players = [NaivePlayer(0), RandomPlayer(1), RandomPlayer(2), RandomPlayer(3)]
    # players = [PlayerTrainer(0, model), RandomPlayer(1), RandomPlayer(2), NaivePlayer(3)]
    # players = [RandomPlayer(0), RandomPlayer(1), RandomPlayer(2), RandomPlayer(3)]
    # players = [RandomPlayer(0), RandomPlayer(1), RandomPlayer(2), NaivePlayer(3)]
    gr = GameRunner(players, random.randint(0, 1000000000), model, trainer, FEATURE_VEC)
    # gr = GameRunner(players, 592, model, trainer)
    activity = gr.Run(False)

    return [activity[0][0], activity[1][0], activity[2][0], activity[3][0]]

def computeAvg(arr):
    return float(np.sum(arr)) / 1


def main():
    model_basename = f"{FEATURE_VEC}_features_{NETWORK_SIZE}_{NUM_LAYERS}_layers_against_naive"
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
            open(data_path, 'a').writelines(model_stats)
            model_stats.clear()
    
    model.save(model_name)
    open(data_path, 'a').writelines(model_stats)
    model_stats.clear()

if __name__ == "__main__":
    main()
