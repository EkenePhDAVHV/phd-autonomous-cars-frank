import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def plot_occupancy_matrix(obj, x_vals, y_vals, title, x_label, y_label, all_fp,
                          file_title):
    fig, ax = plt.subplots()
    fig.set_size_inches(40, 20)

    # plt.subplots_adjust(left=0.2, top=0.8)

    ax.set_facecolor("#EAEAF2")

    try:
        ax.set_title(
            title + ' - ' + obj.simulation_time_label,
            fontsize=38, pad=50, fontweight='bold')
        p1 = ax.plot(x_vals, y_vals[0],
                     color='red',
                     marker='o', markersize=10)
        p2 = ax.plot(x_vals, y_vals[1],
                     color='blue',
                     marker='o', markersize=10)
        p3 = ax.plot(x_vals, y_vals[2],
                     color='green',
                     marker='o', markersize=10)
        plt.margins(x=0.0, y=0.0, tight=False)

        plt.grid(color="#FFFFFF")

        fig.text(0.762, .24,
                 "$\\bf{Total}$" + " " + "$\\bf{Num.}$:" + " " +
                 "$\\bf{of}$:" + " " + "$\\bf{Cars}$:" + " " +
                 str(obj.num_of_all_cars),
                 fontsize=26)

        # Ratio code legend
        fig.text(0.1, 0.19,
                 "$\\bf{1}$" + " " + "$\\bf{-}$" + " " +
                 "100%" + " " + "AV" + " | " +
                 "0%" + " " + "HV" + " - " +
                 "(" +
                 str(round(1.0 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.0 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.26, 0.19,
                 "$\\bf{2}$" + " " + "$\\bf{-}$" + " " +
                 "95%" + " " + "AV" + " | " +
                 "5%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.95 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.05 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.42, 0.19,
                 "$\\bf{3}$" + " " + "$\\bf{-}$" + " " +
                 "90%" + " " + "AV" + " | " +
                 "10%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.90 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.10 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.58, 0.19,
                 "$\\bf{4}$" + " " + "$\\bf{-}$" + " " +
                 "85%" + " " + "AV" + " | " +
                 "15%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.85 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.15 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.74, 0.19,
                 "$\\bf{5}$" + " " + "$\\bf{-}$" + " " +
                 "80%" + " " + "AV" + " | " +
                 "20%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.80 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.20 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.1, 0.15,
                 "$\\bf{6}$" + " " + "$\\bf{-}$" + " " +
                 "75%" + " " + "AV" + " | " +
                 "25%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.75 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.25 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.26, 0.15,
                 "$\\bf{7}$" + " " + "$\\bf{-}$" + " " +
                 "70%" + " " + "AV" + " | " +
                 "30%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.70 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.30 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.42, 0.15,
                 "$\\bf{8}$" + " " + "$\\bf{-}$" + " " +
                 "65%" + " " + "AV" + " | " +
                 "35%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.65 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.35 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.58, 0.15,
                 "$\\bf{9}$" + " " + "$\\bf{-}$" + " " +
                 "60%" + " " + "AV" + " | " +
                 "40%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.60 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.40 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.74, 0.15,
                 "$\\bf{10}$" + " " + "$\\bf{-}$" + " " +
                 "55%" + " " + "AV" + " | " +
                 "45%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.55 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.45 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.1, 0.11,
                 "$\\bf{11}$" + " " + "$\\bf{-}$" + " " +
                 "50%" + " " + "AV" + " | " +
                 "50%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.50 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.50 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.26, 0.11,
                 "$\\bf{12}$" + " " + "$\\bf{-}$" + " " +
                 "45%" + " " + "AV" + " | " +
                 "55%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.45 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.55 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.42, 0.11,
                 "$\\bf{13}$" + " " + "$\\bf{-}$" + " " +
                 "40%" + " " + "AV" + " | " +
                 "60%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.40 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.60 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.58, 0.11,
                 "$\\bf{14}$" + " " + "$\\bf{-}$" + " " +
                 "35%" + " " + "AV" + " | " +
                 "65%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.35 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.65 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.74, 0.11,
                 "$\\bf{15}$" + " " + "$\\bf{-}$" + " " +
                 "30%" + " " + "AV" + " | " +
                 "70%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.30 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.70 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.1, 0.07,
                 "$\\bf{16}$" + " " + "$\\bf{-}$" + " " +
                 "25%" + " " + "AV" + " | " +
                 "75%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.25 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.75 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.26, 0.07,
                 "$\\bf{17}$" + " " + "$\\bf{-}$" + " " +
                 "20%" + " " + "AV" + " | " +
                 "80%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.20 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.80 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.42, 0.07,
                 "$\\bf{18}$" + " " + "$\\bf{-}$" + " " +
                 "15%" + " " + "AV" + " | " +
                 "85%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.15 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.85 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.58, 0.07,
                 "$\\bf{19}$" + " " + "$\\bf{-}$" + " " +
                 "10%" + " " + "AV" + " | " +
                 "90%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.10 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.90 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.74, 0.07,
                 "$\\bf{20}$" + " " + "$\\bf{-}$" + " " +
                 "5%" + " " + "AV" + " | " +
                 "95%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.05 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(0.95 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

        fig.text(0.1, 0.03,
                 "$\\bf{21}$" + " " + "$\\bf{-}$" + " " +
                 "0%" + " " + "AV" + " | " +
                 "100%" + " " + "HV" + " - " +
                 "(" +
                 str(round(0.0 * obj.num_of_all_cars)) + "," +
                 " " +
                 str(round(1.0 * obj.num_of_all_cars)) +
                 ")",
                 fontsize=24)

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

    ax.set_xlim(xmin=min(x_vals),
                xmax=max(x_vals) + 1)

    plt.xlabel(x_label, fontsize=26, labelpad=40,
               fontweight='bold')
    plt.ylabel(y_label, fontsize=26, labelpad=40,
               fontweight='bold')

    # x and y-axes labels
    plt.xticks(np.arange(min(x_vals), max(x_vals) + 1, 1), fontsize=22)
    plt.yticks(np.arange(min([min(y_vals[0]),
                              min(y_vals[1]),
                              min(y_vals[2])]) - 0.1,
                         max([max(y_vals[0]),
                              max(y_vals[1]),
                              max(y_vals[2])]) + 1.0), fontsize=22)

    fig.subplots_adjust(bottom=0.3)
    print(all_fp + file_title + '.png')
    plt.savefig(all_fp + file_title + '.png')
    plt.close()
