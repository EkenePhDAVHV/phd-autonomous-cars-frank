import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from AVHV_Main.Utilities.constants import max_velocity


def plot_velocity_graph(cars, file_path):
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

    # Multiply speed by 2.237 to convert from m/s to miles/hr
    for i in range(len(s_)):
        speed_list.append([j * 2.237 for j in s_[i]])

    for i in range(len(t_)):
        time_list.append(t_[i][:len(speed_list[i])])

    try:
        s_ = np.array(speed_list, dtype=object).reshape(-1, 4)
        t_ = np.array(time_list, dtype=object).reshape(-1, 4)

        cars_to_plot = np.array(cars[:16]).reshape(-1, 4)
    except ValueError:
        return

    # Use the last's cars simulation time as the limit.
    simulation_time = t_[1][0][-1]

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
        fig.set_size_inches(40, 20)

        ax.set_facecolor("#EAEAF2")

        ax.set_title(
            "Speed over Time" + ' - ' + simulation_time_label,
            fontsize=38, pad=50, fontweight='bold')
        p1 = ax.plot(t_[0][0], s_[0][0],
                     color='red',
                     marker='o', markersize=10)
        p2 = ax.plot(t_[0][1], s_[0][1],
                     color='blue',
                     marker='o', markersize=10)
        p3 = ax.plot(t_[0][2], s_[0][2],
                     color='green',
                     marker='o', markersize=10)
        p4 = ax.plot(t_[0][3], s_[0][3],
                     color='purple',
                     marker='o', markersize=10)
        p5 = ax.plot(t_[1][0], s_[1][0],
                     color='orange',
                     marker='o', markersize=10)

        plt.margins(x=0.0, y=0.0, tight=False)

        plt.grid(color="#FFFFFF")

        # legend
        ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0]),
                  (cars_to_plot[0][0].name,
                   cars_to_plot[0][1].name,
                   cars_to_plot[0][2].name,
                   cars_to_plot[0][3].name,
                   cars_to_plot[1][0].name),
                  fontsize=24)

        col_label = (
            "t = " + simulation_time_label,
            f"$\\bf{cars_to_plot[0][0].name}$",
            f"$\\bf{cars_to_plot[0][1].name}$",
            f"$\\bf{cars_to_plot[0][2].name}$",
            f"$\\bf{cars_to_plot[0][3].name}$",
            f"$\\bf{cars_to_plot[1][0].name}$"
        )

        cell_text = (("$\\bf{Minimum}$",
                      str(round(min(s_[0][0]), 2)),
                      str(round(min(s_[0][1]), 2)),
                      str(round(min(s_[0][2]), 2)),
                      str(round(min(s_[0][3]), 2)),
                      str(round(min(s_[1][0]), 2))
                      ),
                     ("$\\bf{Maximum}$",
                      str(round(max(s_[0][0]), 2)),
                      str(round(max(s_[0][1]), 2)),
                      str(round(max(s_[0][2]), 2)),
                      str(round(max(s_[0][3]), 2)),
                      str(round(max(s_[1][0]), 2))
                      ),
                     ("$\\bf{Average}$",
                      str(round(sum(s_[0][0]) / len(s_[0][0]), 2)),
                      str(round(sum(s_[0][1]) / len(s_[0][1]), 2)),
                      str(round(sum(s_[0][2]) / len(s_[0][2]), 2)),
                      str(round(sum(s_[0][3]) / len(s_[0][3]), 2)),
                      str(round(sum(s_[1][0]) / len(s_[1][0]), 2))
                      ))

        the_table = ax.table(cellText=cell_text,
                             colLabels=col_label,
                             colWidths=[.1] * len(col_label),
                             loc='bottom',
                             bbox=[0.0, -0.43, 0.70, 0.27])

        the_table.scale(1.0, 1.0)

        for (row, col), cell in the_table.get_celld().items():
            cell.set_text_props(
                fontproperties=FontProperties(weight='normal', size=28))

        cellDict = the_table.get_celld()
        for i in range(0, len(col_label)):
            cellDict[(0, i)].set_height(.09)
            for j in range(1, len(cell_text) + 1):
                cellDict[(j, i)].set_height(.05)

        fig.text(0.682, .198,
                 "Note that speed is in " + "$\\bf{miles}$" + "$\\bf{/}$" +
                 "$\\bf{hr.}$", fontsize=24)

        min_y = min([min(s_[0][0]),
                     min(s_[0][1]),
                     min(s_[0][2]),
                     min(s_[0][3]),
                     min(s_[1][0])])

        max_y = max([max(s_[0][0]),
                     max(s_[0][1]),
                     max(s_[0][2]),
                     max(s_[0][3]),
                     max(s_[1][0])])

        min_x = min([min(t_[0][0]),
                     min(t_[0][1]),
                     min(t_[0][2]),
                     min(t_[0][3]),
                     min(t_[1][0])])

        max_x = max([max(t_[0][0]),
                     max(t_[0][1]),
                     max(t_[0][2]),
                     max(t_[0][3]),
                     max(t_[1][0])])

        ax.set_ylim(ymin=min_y,
                    ymax=max_y + 1.0)

        ax.set_xlim(xmin=min_x,
                    xmax=max_x + 1.0)

        plt.xticks(np.arange(min_x, max_x + 1.0, 1.0))
        plt.yticks(np.arange(min_y, max_y + 1.0, 1.0))

        plt.xlabel("Time (secs)", fontsize=26, labelpad=40,
                   fontweight='bold')
        plt.ylabel("Speed (miles / hr)", fontsize=26, labelpad=40,
                   fontweight='bold')

        # x and y-axes labels
        plt.xticks(fontsize=22)
        plt.yticks(fontsize=22)

        fig.subplots_adjust(bottom=0.3)
        print(file_path + "speed-time" + '.png')
        plt.savefig(file_path + "speed-time" + '.png')
        plt.close()
    except Exception as e:
        print(e)
