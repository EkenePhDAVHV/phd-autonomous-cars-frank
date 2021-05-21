from copy import copy
import numpy as np
import matplotlib.pyplot as plt


def plot_velocity_graph(cars, file_path):
    time_lists = []
    velocity_lists = []

    for car in cars:
        time_lists.append(car.data['time'])
        velocity_lists.append(car.data['velocity'])

    speed_lists = [[velocity.magnitude() for velocity in velocity_list] for
                   velocity_list in velocity_lists]

    s_ = speed_lists[:12]
    t_ = [[round(_time, 2) for _time in _sublist] for _sublist in time_lists[
                                                                  :12]]
    speed_list = []
    time_list = []

    # Multiply speed by 2.237 to convert from m/s to miles/hr
    for i in range(len(s_)):
        speed_list.append([round(j * 2.237, 2) for j in s_[i]])

    for i in range(len(t_)):
        time_list.append(t_[i][:len(speed_list[i])])

    cars_to_plot = [car.name for car in cars[:12]]
    cars_long_names = copy(cars_to_plot)

    # Change long names to abbreviations.
    for car in cars_to_plot:
        if "GentleCar" in car:
            cars_to_plot[cars_to_plot.index(car)] = "G.C" + car[9:]
        else:
            cars_to_plot[cars_to_plot.index(car)] = "A.C" + car[13:]

    s_ = speed_list
    t_ = time_list
    cars = cars_to_plot

    # try:
    #     s_ = np.array(speed_list, dtype=object).reshape(-1, 4)
    #     t_ = np.array(time_list, dtype=object).reshape(-1, 4)
    #
    #     print(cars_to_plot[:12])
    #
    #     cars = np.array(cars_to_plot).reshape(-1, 4)
    # except ValueError:
    #     return

    # plt.figure(figsize=(40, 10))
    # fig, axs = plt.subplots(int(len(cars[:12]) / 4), 3)
    # fig.set_size_inches(40, 20)
    #
    # # Plot a grid of plots with 4 rows per rows.
    # for i in range(int(len(cars[:12]) / 4)):
    #     time, speed = t_[i], s_[i]
    #     cars_ = cars_to_plot[i]
    #
    #     for j in range(3):
    #         axs[i, j].plot(time[j], speed[j])
    #         axs[i, j].set_title(cars_[j].name, fontsize=32, pad=40,
    #                             fontweight='bold')
    #
    #     for ax in axs.flat:
    #         # ax.set(xlabel='Time', ylabel='Speed')
    #         ax.axis([0, time[j][-1] + 5, 0, max_velocity + 10])
    #         ax.margins(x=0.0, y=0.0, tight=False)
    #
    #         # x and y-axes labels
    #         ax.set_xlabel('Time', fontsize=22, labelpad=30)
    #         ax.set_ylabel('Speed', fontsize=22, labelpad=30)
    #
    #         ax.set_xticklabels(time[j], fontsize=22)
    #         ax.set_yticklabels(speed[j], fontsize=22)
    #         # ax.setxticks(fontsize=22)
    #         # ax.yticks(fontsize=22)
    #
    # fig.tight_layout(pad=3.25)
    # fig.subplots_adjust(bottom=0.2)
    # plt.savefig(file_path + "speed-time" + ".png")

    # Use the last's cars simulation time as the limit.
    simulation_time = t_[9][-1]

    if simulation_time >= 60:
        simulation_time_label = str(round(simulation_time / 60, 1)) + \
                                " min(s)"
    elif simulation_time >= 3600:
        simulation_time_label = str(round(simulation_time / 3600, 2)) + \
                                " hr(s)"
    else:
        simulation_time_label = str(round(simulation_time, 2)) + " sec(s)"

    try:
        fig, ax = plt.subplots()
        fig.set_size_inches(40, 25)

        ax.set_facecolor("#EAEAF2")

        ax.set_title(
            "Speed over Time" + ' - ' + simulation_time_label,
            fontsize=50, pad=50, fontweight='bold')
        p1 = ax.plot(t_[0], s_[0],
                     color='red', linewidth=4.0,
                     marker='o', markersize=16)
        p2 = ax.plot(t_[1], s_[1],
                     color='blue', linewidth=4.0,
                     marker='o', markersize=16)
        p3 = ax.plot(t_[2], s_[2],
                     color='green', linewidth=4.0,
                     marker='o', markersize=16)
        p4 = ax.plot(t_[3], s_[3],
                     color='purple', linewidth=4.0,
                     marker='o', markersize=16)
        p5 = ax.plot(t_[4], s_[4],
                     color='orange', linewidth=4.0,
                     marker='o', markersize=16)
        p6 = ax.plot(t_[5], s_[5],
                     color='red', linewidth=4.0,
                     marker='o', markersize=16)
        p7 = ax.plot(t_[6], s_[6],
                     color='blue', linewidth=4.0,
                     marker='o', markersize=16)
        p8 = ax.plot(t_[7], s_[7],
                     color='green', linewidth=4.0,
                     marker='o', markersize=16)
        p9 = ax.plot(t_[8], s_[8],
                     color='purple', linewidth=4.0,
                     marker='o', markersize=16)
        p10 = ax.plot(t_[9], s_[9],
                     color='orange', linewidth=4.0,
                     marker='o', markersize=16)

        plt.margins(x=0.0, y=0.0, tight=False)

        plt.grid(color="#FFFFFF")

        # legend
        ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0], p8[0],
                   p9[0], p10[0]),
                  (cars_long_names[0],
                   cars_long_names[1],
                   cars_long_names[2],
                   cars_long_names[3],
                   cars_long_names[4],
                   cars_long_names[5],
                   cars_long_names[6],
                   cars_long_names[7],
                   cars_long_names[8],
                   cars_long_names[9]
                   ),
                  fontsize=36)

        col_label = (
            "t = " + simulation_time_label,
            f"$\\bf{cars[0]}$",
            f"$\\bf{cars[1]}$",
            f"$\\bf{cars[2]}$",
            f"$\\bf{cars[3]}$",
            f"$\\bf{cars[4]}$",
            f"$\\bf{cars[5]}$",
            f"$\\bf{cars[6]}$",
            f"$\\bf{cars[7]}$",
            f"$\\bf{cars[8]}$",
            f"$\\bf{cars[9]}$"
        )

        cell_text = (("$\\bf{Minimum}$",
                      str(round(min(s_[0]), 2)),
                      str(round(min(s_[1]), 2)),
                      str(round(min(s_[2]), 2)),
                      str(round(min(s_[3]), 2)),
                      str(round(min(s_[4]), 2)),
                      str(round(min(s_[5]), 2)),
                      str(round(min(s_[6]), 2)),
                      str(round(min(s_[7]), 2)),
                      str(round(min(s_[8]), 2)),
                      str(round(min(s_[9]), 2))
                      ),
                     ("$\\bf{Maximum}$",
                      str(round(max(s_[0]), 2)),
                      str(round(max(s_[1]), 2)),
                      str(round(max(s_[2]), 2)),
                      str(round(max(s_[3]), 2)),
                      str(round(max(s_[4]), 2)),
                      str(round(max(s_[5]), 2)),
                      str(round(max(s_[6]), 2)),
                      str(round(max(s_[7]), 2)),
                      str(round(max(s_[8]), 2)),
                      str(round(max(s_[9]), 2))
                      ),
                     ("$\\bf{Average}$",
                      str(round(sum(s_[0]) / len(s_[0]), 2)),
                      str(round(sum(s_[1]) / len(s_[1]), 2)),
                      str(round(sum(s_[2]) / len(s_[2]), 2)),
                      str(round(sum(s_[3]) / len(s_[3]), 2)),
                      str(round(sum(s_[4]) / len(s_[4]), 2)),
                      str(round(sum(s_[5]) / len(s_[5]), 2)),
                      str(round(sum(s_[6]) / len(s_[6]), 2)),
                      str(round(sum(s_[7]) / len(s_[7]), 2)),
                      str(round(sum(s_[8]) / len(s_[8]), 2)),
                      str(round(sum(s_[9]) / len(s_[9]), 2))
                      ))

        the_table = ax.table(cellText=cell_text,
                             colLabels=col_label,
                             colWidths=[.1] * len(col_label),
                             loc='bottom',
                             bbox=[0.0, -0.43, 1.0, 0.27])

        the_table.auto_set_font_size(False)
        the_table.set_fontsize(40)
        the_table.scale(1.0, 1.0)

        # for (row, col), cell in the_table.get_celld().items():
        #     cell.set_text_props(
        #         fontproperties=FontProperties(weight='normal', size=28))

        cellDict = the_table.get_celld()
        for i in range(0, len(col_label)):
            cellDict[(0, i)].set_height(.1)
            for j in range(1, len(cell_text) + 1):
                cellDict[(j, i)].set_height(.07)

        cellDict = the_table.get_celld()
        cellDict[(0, 0)].set_width(0.25)
        cellDict[(1, 0)].set_width(0.25)
        cellDict[(2, 0)].set_width(0.25)
        cellDict[(3, 0)].set_width(0.25)

        # fig.text(0.682, .198,
        #          "Note that speed is in " + "$\\bf{miles}$" + "$\\bf{/}$" +
        #          "$\\bf{hr.}$", fontsize=24)

        min_y = min([min(s_[0]),
                     min(s_[1]),
                     min(s_[2]),
                     min(s_[3]),
                     min(s_[4]),
                     min(s_[5]),
                     min(s_[6]),
                     min(s_[7]),
                     min(s_[8]),
                     min(s_[9])
                     ])

        max_y = max([max(s_[0]),
                     max(s_[1]),
                     max(s_[2]),
                     max(s_[3]),
                     max(s_[4]),
                     min(s_[5]),
                     min(s_[6]),
                     min(s_[7]),
                     min(s_[8]),
                     min(s_[9])])

        min_x = min([min(t_[0]),
                     min(t_[1]),
                     min(t_[2]),
                     min(t_[3]),
                     min(t_[4]),
                     min(t_[5]),
                     min(t_[6]),
                     min(t_[7]),
                     min(t_[8]),
                     min(t_[9])
                     ])

        max_x = max([max(t_[0]),
                     max(t_[1]),
                     max(t_[2]),
                     max(t_[3]),
                     max(t_[4]),
                     min(t_[5]),
                     min(t_[6]),
                     min(t_[7]),
                     min(t_[8]),
                     min(t_[9])])

        ax.set_ylim(ymin=min_y, ymax=max_y + 1.0)
        ax.set_xlim(xmin=min_x, xmax=max_x + 1.0)

        # x and y-axes labels
        plt.xlabel("Time (secs)", fontsize=40, labelpad=40,
                   fontweight='bold')
        plt.ylabel("Speed (miles / hr)", fontsize=40, labelpad=40,
                   fontweight='bold')

        plt.xticks(np.arange(min_x, max_x + 1.0, 1.0), fontsize=30)
        plt.yticks(np.arange(min_y, max_y + 1.0, 1.0), fontsize=30)

        fig.subplots_adjust(bottom=0.3)
        print(file_path + "speed-time" + '.png')
        plt.savefig(file_path + "speed-time" + '.png')
        plt.close()
    except Exception as e:
        print(e)
