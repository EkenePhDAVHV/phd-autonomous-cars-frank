import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

i = 0
j = 100


def generate_concat_values(df_obj, fp, fn):
    df_obj['safe_distance'] = df_obj['safe_distance'].sort_values(ascending=True).values
    df_obj['reaction_time'] = df_obj['reaction_time'].sort_values(ascending=True).values

    def dist1(x):
        return 1 / (std1 * np.sqrt(2 * np.pi)) * np.exp(-(x - mean1) ** 2 / (2 * std1 ** 2))

    def dist2(x):
        return 1 / (std2 * np.sqrt(2 * np.pi)) * np.exp(-(x - mean2) ** 2 / (2 * std2 ** 2))

    mean1 = df_obj['safe_distance'].mean()
    std1 = df_obj['safe_distance'].std()

    mean2 = df_obj['reaction_time'].mean()
    std2 = df_obj['reaction_time'].std()

    dist_safe_dist_list = map(dist1, df_obj['safe_distance'])

    df_avg_safe_dist = pd.DataFrame({'average_safe_distance': [mean1]})
    df_std_safe_dist = pd.DataFrame({'std_safe_distance': [std1]})
    df_dist_safe_dist = pd.DataFrame({'distrib_reaction_time': dist_safe_dist_list})

    dist_reaction_time_list = map(dist2, df_obj['reaction_time'])

    df_avg_reaction_time = pd.DataFrame({'average_reaction_time': [mean2]})
    df_std_reaction_time = pd.DataFrame({'std_reaction_time': [std1]})
    df_dist_reaction_time = pd.DataFrame({'distrib_reaction_time': dist_reaction_time_list})

    df_combined = pd.concat(
        [df_obj, df_avg_safe_dist, df_std_safe_dist, df_dist_safe_dist, df_avg_reaction_time, df_std_reaction_time,
         df_dist_reaction_time], axis=1)

    ax_num = []

    for c in range(len(df_obj['safe_distance'])):
        ax_num.append(c)

    # plot normal distribution and save to picture file
    fig, ax = plt.subplots()
    fig.set_size_inches(40, 20)
    p1 = ax.plot(ax_num, df_combined['distrib_safe_distance'], 'r')
    ax.set_title('Normal Distribution of Safe Distance', fontsize=20, pad=20)
    ax.legend((p1[0],), ('Safe Distance',), fontsize=20)
    ax.autoscale_view()
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    plt.grid(which='major', axis='both')
    plt.yticks(np.arange(0, df_combined['distrib_safe_distance'].max() + 0.01, 0.001))
    plt.xticks(np.arange(0, len(df_combined['safe_distance']) + 500, 250))
    plt.ylabel('Value', fontsize=20, labelpad=20)
    plt.xlabel('Observation', fontsize=20, labelpad=30)
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.savefig(fp + fn + '_normal_dist_safe_distance' + '.png')
    plt.close()

    # plot normal distribution and save to picture file
    # fig, ax = plt.subplots()
    # fig.set_size_inches(40, 20)
    # p1 = ax.plot(ax_num, df_combined['distrib_reaction_time'], 'r')
    # ax.set_title('Normal Distribution of Reaction Time', fontsize=20, pad=20)
    # ax.legend((p1[0],), ('Reaction Time',), fontsize=20)
    # ax.autoscale_view()
    # ax.tick_params(axis='x', labelsize=14)
    # ax.tick_params(axis='y', labelsize=14)
    # plt.grid(which='major', axis='both')
    # plt.yticks(np.arange(0, df_combined['distrib_reaction_time'].max() + 100000, 100000))
    # plt.xticks(np.arange(0, len(df_combined['safe_distance']) + 500, 250))
    # plt.ylabel('Value', fontsize=20, labelpad=20)
    # plt.xlabel('Observation', fontsize=20, labelpad=30)
    # plt.xlim(xmin=0)
    # plt.ylim(ymin=0)
    # plt.savefig(fp + fn + '_dist_reaction_time' + '.png')
    # plt.close()

    # save normal distribution to file
    df_combined.to_csv(fp + fn + '_dist' + '.csv', index=False)

    # plot scatter plot for stopping time and speed and save to picture file
    fig, ax = plt.subplots()
    fig.set_size_inches(40, 20)
    p1 = ax.scatter(ax_num, df_obj['stopping_time'], color='red')
    p2 = ax.scatter(ax_num, df_obj['speed'], color='blue')
    ax.set_title('Scatter plot for stopping time and speed', fontsize=20, pad=20)
    # ax.legend((p1[0]), ('Stopping Time'), fontsize=20)
    ax.autoscale_view()
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    plt.grid(which='major', axis='both')
    plt.yticks(np.arange(0, max(df_combined['stopping_time'].max(), df_combined['speed'].max()) + 5, 1))
    plt.xticks(np.arange(0, len(df_combined['safe_distance']) + 500, 250))
    plt.xlabel('Value', fontsize=20, labelpad=30)
    plt.ylabel('Observation', fontsize=20, labelpad=30)
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.savefig(fp + fn + '_scatter_plot_stopping_time_speed' + '.png')
    plt.close()

    # plot histogram for reaction time
    df_obj.drop_duplicates(subset="car_name", keep='first', inplace=True)

    # df_obj.to_csv(fp + fn + 'unique' + '.csv', index=False)

    N = len(df_obj)
    cars_list = df_obj['car_name'].values.tolist()

    # fig = plt.figure()

    fig, ax = plt.subplots()
    fig.set_size_inches(40, 20)
    ind = np.arange(N)
    width = 0.5

    p1 = ax.bar(ind, df_obj['reaction_time'], width, align='center')
    ax.set_title('Histogram of Reaction Time', fontsize=20, pad=20)
    ax.set_xticks(ind)
    ax.set_xticklabels(['car ' + str(cars_list.index(x) + 1) for x in cars_list], fontsize=16)
    ax.legend((p1[0],), ('Reaction Time',), fontsize=16)
    ax.autoscale_view()
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    plt.grid(which='major', axis='both')
    plt.yticks(np.arange(0, df_obj['reaction_time'].max() + 1, 0.1))
    # plt.xticks(np.arange(0, len(df_combined['safe_distance']) + 500, 250))
    plt.ylabel('Value', fontsize=20, labelpad=20)
    plt.xlabel('Observation', fontsize=20, labelpad=30)
    plt.savefig(fp + fn + '_histogram_reaction_time' + '.png')
    plt.close()

    # fig = plt.figure()

    N = len(df_combined)

    fig, ax = plt.subplots()
    fig.set_size_inches(40, 20)
    ind = np.arange(N)
    width = 0.5

    p1 = ax.bar(ind, df_combined['safe_distance'], width, align='center')
    ax.set_title('Histogram of Safe Distance', fontsize=20, pad=20)
    ax.set_xticks(ind)
    # ax.set_xticklabels(['car ' + str(cars_list.index(x) + 1) for x in cars_list], fontsize=16)
    ax.legend((p1[0],), ('Safe Distance',), fontsize=16)
    ax.autoscale_view()
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    plt.grid(which='major', axis='both')
    plt.yticks(np.arange(0, df_combined['safe_distance'].max() + 10, 1))
    # plt.xticks(np.arange(0, len(df_combined['safe_distance']) + 500, 250))
    plt.ylabel('Value', fontsize=20, labelpad=20)
    plt.xlabel('Observation', fontsize=20, labelpad=30)
    plt.savefig(fp + fn + '_histogram_safe_distance' + '.png')
    plt.close()


while j >= 0:
    file_path = './generated_values/' + f'{i}AV_{j}HV/'

    # handle exception elegantly
    try:
        file_name = f'hv_{i}_{j}'
        df = pd.read_csv(file_path + file_name + '.csv', sep=",")
        generate_concat_values(df, file_path, file_name)
    except FileNotFoundError as e:
        pass

    # handle exception elegantly
    try:
        file_name2 = f'av_{i}_{j}'
        df2 = pd.read_csv(file_path + file_name2 + '.csv', sep=",")
        generate_concat_values(df2, file_path, file_name2)
    except FileNotFoundError as e:
        pass

    i = i + 5
    j = j - 5

try:
    df = pd.read_csv(file_path + "full_capacity" + '.csv', sep=",")
    generate_concat_values(df, file_path, file_name)
except FileNotFoundError as e:
    pass

try:
    df = pd.read_csv(file_path + "half_capacity" + '.csv', sep=",")
    generate_concat_values(df, file_path, file_name)
except FileNotFoundError as e:
    pass
