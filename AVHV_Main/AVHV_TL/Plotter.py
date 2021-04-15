import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, file_path=None):
        self.i = 0
        self.j = 100

        self.mean1 = None
        self.std1 = None
        self.mean2 = None
        self.std2 = None

        self.file_path = file_path

    @staticmethod
    def generate_concat_values(self, df_obj, fp, fn):
        df_obj['safe_distance'] = \
            df_obj['safe_distance'].sort_values(ascending=True).values
        df_obj['reaction_time'] = \
            df_obj['reaction_time'].sort_values(ascending=True).values

        def dist1(x):
            return round(1 / (self.std1 * np.sqrt(2 * np.pi)) *
                         np.exp(-(x - self.mean1) ** 2 /
                                (2 * self.std1 ** 2)), 4)

        def dist2(x):
            if 2 * self.std2 ** 2 == 0:
                return 0

            return round(1 / (self.std2 * np.sqrt(2 * np.pi)) *
                         np.exp(-(x - self.mean2) ** 2 /
                                (2 * self.std2 ** 2)), 4)

        self.mean1 = df_obj['safe_distance'].mean()
        self.std1 = df_obj['safe_distance'].std()

        self.mean2 = df_obj['reaction_time'].mean()
        self.std2 = df_obj['reaction_time'].std()

        dist_safe_dist_list = map(dist1, df_obj['safe_distance'])

        df_avg_safe_dist = pd.DataFrame({'average_safe_distance': [self.mean1]})
        df_std_safe_dist = pd.DataFrame({'std_safe_distance': [self.std1]})
        df_dist_safe_dist = \
            pd.DataFrame({'distrib_safe_distance': dist_safe_dist_list})

        dist_reaction_time_list = map(dist2, df_obj['reaction_time'])

        df_avg_reaction_time = pd.DataFrame({'average_reaction_time': [self.mean2]})
        df_std_reaction_time = pd.DataFrame({'std_reaction_time': [self.std2]})
        df_dist_reaction_time = \
            pd.DataFrame({'distrib_reaction_time': dist_reaction_time_list})

        df_combined = pd.concat(
            [df_obj, df_avg_safe_dist, df_std_safe_dist, df_dist_safe_dist,
             df_avg_reaction_time, df_std_reaction_time,
             df_dist_reaction_time], axis=1)

        # save normal distribution to file
        df_combined.to_csv(fp + fn + '.csv', index=False)

        # get averages of values by each car
        df_obj_mean = df_obj.groupby(['car_name'], as_index=False).mean()
        df_obj.drop_duplicates(subset="car_name", keep='first', inplace=True)

        ax_num = []
        ax_num_mean = []

        for c in range(len(df_combined['distrib_safe_distance'])):
            ax_num.append(c)

        for c in range(len(df_obj_mean['safe_distance'])):
            ax_num_mean.append(c)

        cars_list = df_obj_mean['car_name'].values.tolist()

        prefix = "car"
        color = "#FF0000"

        if "av" in fn:
            prefix = "AV"
            color = "#0000FF"
        elif "hv" in fn:
            prefix = "HV"
            color = "#FF0000"

        # -------- Normal Distribution for Safe Distance ------------------- #
        fig, ax = plt.subplots()
        fig.set_size_inches(40, 20)
        p1 = ax.plot(ax_num, df_combined['distrib_safe_distance'], 'r')
        ax.set_title('Normal Distribution of Safe Distance ' +
                     '(' + prefix + ')', fontsize=20, pad=20)

        # rotate the tick labels on the x-axis
        ax.set_xticks([i for i in ax_num])
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)

        # legend
        ax.legend((p1[0],), ('Safe Distance Normal Distribution Values',),
                  fontsize=20)

        ax.autoscale_view()  # autoscale the figure along the x-axis and y-axis

        # size of tick labels
        ax.tick_params(axis='x', labelsize=16)
        ax.tick_params(axis='y', labelsize=16)

        # add grid on both x and y axes
        plt.grid(which='major', axis='both')

        plt.yticks(np.arange(0, df_combined['distrib_safe_distance']
                             .max() + 0.01, 0.001))
        plt.xticks(np.arange(0, len(df_combined['safe_distance']) + 500, 250))

        plt.ylabel('Value (Normal Distribution Form)', fontsize=20, labelpad=20)
        plt.xlabel('Observation', fontsize=20, labelpad=30)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.savefig(fp + fn + '_normal_distrib_safe_distance' + '.png')
        plt.close()

        # -------- Scatter Plot of Stopping Time and Speed ------------------ #
        fig, ax = plt.subplots()
        fig.set_size_inches(40, 20)

        for item in ['stopping_time', 'speed']:
            if item == 'stopping_time':
                ax.scatter(ax_num_mean, df_obj_mean['stopping_time'], c='r',
                           label="Stopping Time")
            else:
                ax.scatter(ax_num_mean, df_obj_mean['speed'], c='b',
                           label='Speed')

        ax.set_title('Scatter Plot of Stopping Time and Speed ' +
                     '(' + prefix + ') - Averages of each car\'s values',
                     fontsize=20, pad=20)

        # rotate the tick labels on the x-axis
        ax.set_xticks([i for i in ax_num])
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)

        # x-axis label
        ax.set_xticklabels([str(x) for x in cars_list], fontsize=16)

        # legend
        ax.legend(fontsize=20)

        ax.autoscale_view()  # autoscale the figure along the x-axis and y-axis

        # size of tick labels
        ax.tick_params(axis='x', labelsize=16)
        ax.tick_params(axis='y', labelsize=16)

        # add grid on both x and y axes
        plt.grid(which='major', axis='both')

        plt.yticks(np.arange(0, max(df_obj_mean['stopping_time'].max(),
                                    df_obj_mean['speed'].max()) + 1, 1))

        plt.ylabel('Values', fontsize=20, labelpad=20)
        plt.xlabel('Observation', fontsize=20, labelpad=30)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)

        plt.savefig(fp + fn + '_scatter_plot_stopping_time_speed' + '.png')
        plt.close()

        # -------- Line Plot of Reaction Time and Time -------------------- #
        fig, axs = plt.subplots(2, 3)
        fig.set_size_inches(40, 20)

        axs[0, 0].hist(df_combined['safe_distance'], 40, facecolor=color,
                       alpha=0.75, density=True)
        axs[0, 0].set_title("Safe Distance", size=20, pad=20)

        axs[0, 1].hist(df_combined['speed'], 40, facecolor=color, alpha=0.75,
                       density=True)
        axs[0, 1].set_title("Speed", size=20, pad=20)

        # axs[0, 2].hist(df_combined['deceleration_force'], 40, facecolor=color,
        #                alpha=0.75, density=True)
        axs[0, 2].set_title("Deceleration Force", size=20, pad=20)

        axs[1, 0].hist(df_combined['reaction_time'], 40, facecolor=color,
                       alpha=0.75, density=True)
        axs[1, 0].set_title("Reaction Time", size=20, pad=20)

        axs[1, 1].hist(df_combined['stopping_time'], 40, facecolor=color,
                       alpha=0.75, density=True)
        axs[1, 1].set_title("Stopping Time", size=20, pad=20)

        fig.tight_layout()

        # plt.set_title('Histograms of Values' + '(' + prefix + ')',
        #              fontsize=20, pad=20)

        for ax in axs.flat:
            ax.set(xlabel='Value')
            ax.set(ylabel='Count')

            ax.xaxis.label.set_size(20)
            ax.yaxis.label.set_size(20)

            # size of tick labels
            ax.tick_params(axis='x', labelsize=20)
            ax.tick_params(axis='y', labelsize=20)

        # y-axis labels
        plt.yticks(np.arange(0, df_combined['reaction_time'].max() + 1, 0.1))

        # x-axis labels
        plt.xticks(np.arange(0, len(df_combined['reaction_time']), 1000),
                   fontsize=16)

        # legend
        # ax.legend((p1[0], p2[0]), ('Safe Distance', 'Speed'), fontsize=20)

        ax.autoscale_view()  # autoscale the figure along the x-axis and y-axis

        plt.tight_layout(pad=5)

        # add grid on both x and y axes
        # plt.grid(which='major', axis='both')

        # plt.ylabel('Reaction Time', fontsize=20, labelpad=20)
        # plt.xlabel('Time', fontsize=20, labelpad=30)
        # plt.xlim(xmin=0)
        # plt.ylim(ymin=0)
        plt.savefig(fp + fn + '_histograms' + '.png')
        plt.close()

    def read_csv(self, file_name):
        # handle exception elegantly
        try:
            df = pd.read_csv(self.file_path + file_name + '.csv', sep=",")
            self.generate_concat_values(self, df, self.file_path, file_name)
        except FileNotFoundError as e:
            pass
