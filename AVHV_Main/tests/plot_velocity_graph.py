import numpy as np
import matplotlib.pyplot as plt

from AVHV_Main.Utilities.constants import max_velocity


def plot_velocity_graph(cars, file_path, current_file_name):
    time_lists = []
    velocity_lists = []

    for car in cars:
        time_lists.append(car.data['time'])
        velocity_lists.append(car.data['velocity'])

    speed_lists = [[velocity.magnitude() for velocity in velocity_list] for
                   velocity_list in velocity_lists]

    s_ = speed_lists[:16]
    t_ = time_lists[:16]

    speed_list = []
    time_list = []

    for i in range(len(s_)):
        speed_list.append([j for j in s_[i]])

    for i in range(len(t_)):
        time_list.append(t_[i][:len(speed_list[i])])

    try:
        s_ = np.array(speed_list, dtype=object).reshape(-1, 4)
        t_ = np.array(time_list, dtype=object).reshape(-1, 4)

        cars_to_plot = np.array(cars[:16]).reshape(-1, 4)
    except ValueError:
        return

    plt.figure(figsize=(10, 10))
    fig, axs = plt.subplots(int(len(cars[:16]) / 4), 4)

    # Plot a grid of plots with 4 rows per rows.
    for i in range(int(len(cars[:16]) / 4)):
        time, speed = t_[i], s_[i]
        cars_ = cars_to_plot[i]

        for j in range(4):
            axs[i, j].plot(time[j], speed[j])
            axs[i, j].set_title(cars_[j].name, pad=1)

        for ax in axs.flat:
            ax.set(xlabel='Time', ylabel='Speed')
            ax.axis([0, time[j][-1] + 5, 0, max_velocity + 10])
            ax.margins(x=0.0, y=0.0, tight=False)

    fig.tight_layout(pad=0.05)
    plt.savefig(file_path + current_file_name + ".png")
