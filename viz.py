import os
import matplotlib.pyplot as plt
import tqdm


def max_seen_so_far(stats):
    max_so_far = -1.
    maxes = []
    for s in stats:
        if s > max_so_far:
            max_so_far = s
        maxes.append(max_so_far)
    return maxes


def iter_wr(wins):
    wrs = []
    for i, w in enumerate(wins):
        n_w = 0
        for j, w in enumerate(wins[:i+1]):
            if w == 1:
                n_w += 1
        wrs.append(n_w/(i+1))
    return wrs


def read_and_plot(model_basename):
    data_path = f"model/{model_basename}.txt"
    stats = []
    wins = []
    with open(data_path) as infile:
        for line in infile.readlines():
            line.strip()
            score, win = line.split(',')

            stats.append(float(score))
            wins.append(int(win))

    maxes = max_seen_so_far(stats)
    wrs = iter_wr(wins)

    plt.rcParams["figure.figsize"] = (8, 10)
    fig, axs = plt.subplots(3, 1)
    plt.title(f"{model_basename}")
    axs[0].plot(stats)
    axs[0].set_title(f"{model_basename} Score")
    axs[1].plot(maxes)
    axs[1].set_title("Max Score")
    axs[2].plot(wrs)
    axs[2].set_title("WR")
    axs[2].axhline(y=0.5, color='r', linestyle='dashed')

    if not os.path.exists(model_folder_path := "figures"):
        os.makedirs(model_folder_path)
    plt.savefig(f"{model_folder_path}/{model_basename}.png")


def main():
    model_names = [
        "initial_features_128",
        "initial_features_256",
        "initial_features_512",
        "initial_features_1024",
        "no_matrix_features_128",
        "no_matrix_features_256",
        "no_matrix_features_512",
        "no_matrix_features_1024",
    ]
    for model in tqdm.tqdm(model_names):
        read_and_plot(model)


if __name__ == "__main__":
    main()
