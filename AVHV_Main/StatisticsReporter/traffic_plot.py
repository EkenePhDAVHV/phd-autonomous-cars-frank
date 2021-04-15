import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def plot_traffic(obj, x_vals, y_vals, title, x_label, y_label, fp,
                 file_title, x_column_title='', y_column_title='',
                 x_val_only_in_table=False, y_val_only_in_table=False):
    fig, ax = plt.subplots()
    fig.set_size_inches(40, 20)

    # plt.subplots_adjust(left=0.2, top=0.8)

    ax.set_facecolor("#EAEAF2")

    try:
        ax.set_title(
            title + ' - ' + obj.simulation_time_label,
            fontsize=38, pad=50, fontweight='bold')
        p1 = ax.plot(x_vals[0], y_vals[0],
                     color='red',
                     marker='o', markersize=10)
        p2 = ax.plot(x_vals[1], y_vals[1],
                     color='blue',
                     marker='o', markersize=10)
        p3 = ax.plot(x_vals[2], y_vals[2],
                     color='green',
                     marker='o', markersize=10)
        plt.margins(x=0.0, y=0.0, tight=False)

        plt.grid(color="#FFFFFF")

        if x_val_only_in_table:
            col_label = (
                "t = " + "8 sec(s)",
                "$\\bf{Min.}$" + f"$\\bf{x_column_title}$",
                "$\\bf{Max.}$" + f"$\\bf{x_column_title}$",
                "$\\bf{Avg.}$" + f"$\\bf{x_column_title}$",
                "$\\bf{Reached}$" + " " + "$\\bf{Dest.}$" +
                "\n" +
                "$\\bf{AV}$" + " : " + "$\\bf{HV}$"
            )

            cell_text = (("$\\bf{TL}$",
                          str(min(x_vals[0])),
                          str(max(x_vals[0])),
                          str(round(
                              sum(x_vals[0]) / len(
                                  x_vals[0]),
                              2)),
                          str(obj.num_of_passed_cars[0][0]) + ":" +
                          str(obj.num_of_passed_cars[0][1])
                          # + ":" + str(num_of_passed_cars[0][2])
                          ),
                         ("$\\bf{CAwSD4WI}$",
                          str(min(x_vals[1])),
                          str(max(x_vals[1])),
                          str(round(
                              sum(x_vals[1]) / len(
                                  x_vals[1]),
                              2)),
                          str(obj.num_of_passed_cars[1][0]) + ":" +
                          str(obj.num_of_passed_cars[1][1])
                          # + ":" + str(num_of_passed_cars[1][2])
                          ),
                         ("$\\bf{RN}$",
                          str(min(x_vals[1])),
                          str(max(x_vals[1])),
                          str(round(
                              sum(x_vals[1]) / len(
                                  x_vals[1]),
                              2)),
                          str(obj.num_of_passed_cars[2][0]) + ":" +
                          str(obj.num_of_passed_cars[2][1])
                          )
                         )
        elif y_val_only_in_table:
            col_label = (
                "t = " + "8 sec(s)",
                "$\\bf{Min.}$" + f"$\\bf{y_column_title}$",
                "$\\bf{Max.}$" + f"$\\bf{y_column_title}$",
                "$\\bf{Avg.}$" + f"$\\bf{y_column_title}$",
                "$\\bf{Reached}$" + " " + "$\\bf{Dest.}$" +
                "\n" +
                "$\\bf{AV}$" + " : " + "$\\bf{HV}$"
            )

            cell_text = (("$\\bf{TL}$",
                          str(min(y_vals[0])),
                          str(max(y_vals[0])),
                          str(round(
                              sum(y_vals[0]) / len(
                                  y_vals[0]),
                              2)),
                          str(obj.num_of_passed_cars[0][0]) + ":" +
                          str(obj.num_of_passed_cars[0][1])
                          # + ":" + str(num_of_passed_cars[0][2])
                          ),
                         ("$\\bf{CAwSD4WI}$",
                          str(min(y_vals[1])),
                          str(max(y_vals[1])),
                          str(round(
                              sum(y_vals[1]) / len(
                                  y_vals[1]),
                              2)),
                          str(obj.num_of_passed_cars[1][0]) + ":" +
                          str(obj.num_of_passed_cars[1][1])
                          # + ":" + str(num_of_passed_cars[1][2])
                          ),
                         ("$\\bf{RN}$",
                          str(min(y_vals[2])),
                          str(max(y_vals[2])),
                          str(round(
                              sum(y_vals[2]) / len(
                                  y_vals[2]),
                              2)),
                          str(obj.num_of_passed_cars[2][0]) + ":" +
                          str(obj.num_of_passed_cars[2][1])
                          )
                         )
        else:
            col_label = (
                "t = " + "8 sec(s)",
                "$\\bf{Min.}$" + f"$\\bf{x_column_title}$",
                "$\\bf{Max.}$" + f"$\\bf{x_column_title}$",
                "$\\bf{Avg.}$" + f"$\\bf{x_column_title}$",
                "$\\bf{Min.}$" + f"$\\bf{y_column_title}$",
                "$\\bf{Max.}$" + f"$\\bf{y_column_title}$",
                "$\\bf{Avg.}$" + f"$\\bf{y_column_title}$",
                "$\\bf{Reached}$" + " " + "$\\bf{Dest.}$" +
                "\n" +
                "$\\bf{AV}$" + " : " + "$\\bf{HV}$"
            )

            cell_text = (("$\\bf{TL}$",
                          str(min(x_vals[0])),
                          str(max(x_vals[0])),
                          str(round(
                              sum(x_vals[0]) / len(
                                  x_vals[0]),
                              2)),
                          str(min(y_vals[0])),
                          str(max(y_vals[0])),
                          str(round(
                              sum(y_vals[0]) / len(
                                  y_vals[0]),
                              2)),
                          str(obj.num_of_passed_cars[0][0]) + ":" +
                          str(obj.num_of_passed_cars[0][1])
                          # + ":" + str(num_of_passed_cars[0][2])
                          ),
                         ("$\\bf{CAwSD4WI}$",
                          str(min(x_vals[1])),
                          str(max(x_vals[1])),
                          str(round(
                              sum(x_vals[1]) / len(
                                  x_vals[1]),
                              2)),
                          str(min(y_vals[1])),
                          str(max(y_vals[1])),
                          str(round(
                              sum(y_vals[1]) / len(
                                  y_vals[1]),
                              2)),
                          str(obj.num_of_passed_cars[1][0]) + ":" +
                          str(obj.num_of_passed_cars[1][1])
                          # + ":" + str(num_of_passed_cars[1][2])
                          ),
                         ("$\\bf{RN}$",
                          str(min(x_vals[1])),
                          str(max(x_vals[1])),
                          str(round(
                              sum(x_vals[1]) / len(
                                  x_vals[1]),
                              2)),
                          str(min(y_vals[2])),
                          str(max(y_vals[2])),
                          str(round(
                              sum(y_vals[2]) / len(
                                  y_vals[2]),
                              2)),
                          str(obj.num_of_passed_cars[2][0]) + ":" +
                          str(obj.num_of_passed_cars[2][1])
                          # + ":" + str(num_of_passed_cars[2][2])
                          )
                         )

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

        fig.text(0.762, .19,
                 "$\\bf{Total}$" + " " + "$\\bf{AV}$:" + " " +
                 str(obj.total_av) + "   " +
                 "$\\bf{Total}$" + " " + "$\\bf{HV}$:" + " " +
                 str(obj.total_hv),
                 fontsize=26)

        # the_table.set_fontsize(30)

    except Exception as e:
        print(e)

    # legend
    ax.legend((p1[0], p2[0], p3[0]),
              ('Traffic Lights',
               'Collision Avoidance w/ Safe Distance & 4 Way Intersection',
               'Reservation Nodes'),
              fontsize=24)

    ax.set_ylim(ymin=min([min(y_vals[0]),
                          min(y_vals[1]),
                          min(y_vals[2])]) - 0.1,
                ymax=max([max(y_vals[0]),
                          max(y_vals[1]),
                          max(y_vals[2])]) + 0.1)

    ax.set_xlim(xmin=min([min(x_vals[0]),
                          min(x_vals[1]),
                          min(x_vals[2])]),
                xmax=max([max(x_vals[0]),
                          max(x_vals[1]),
                          max(x_vals[2])]) + 1)

    plt.xlabel(x_label, fontsize=26, labelpad=40,
               fontweight='bold')
    plt.ylabel(y_label, fontsize=26, labelpad=40,
               fontweight='bold')

    # x and y-axes labels
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)

    fig.subplots_adjust(bottom=0.3)
    print(fp + file_title + '.png')
    plt.savefig(fp + file_title + '.png')
    plt.close()