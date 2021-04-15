import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

car_densities = [[], [], []]
time_graduation = []

num_of_cars = [145, 157, 0]
num_of_passed_cars = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

with open('task_5_density.csv', 'r') as f:
    # using csv.writer method from CSV package
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 0:
            car_densities[0].append(float(row[0]))
            car_densities[1].append(float(row[1]))
            car_densities[2].append(float(row[2]))
            time_graduation.append(float(row[3]))

car_densities[0] = car_densities[0][1:]
car_densities[1] = car_densities[1][1:]
car_densities[2] = car_densities[2][1:]
time_graduation = time_graduation[1:]

fig, ax = plt.subplots()
fig.set_size_inches(40, 20)

ax.set_facecolor("#EAEAF2")
ax.set_title('Density of Vehicle' + ' - ',
             fontsize=38, pad=50, fontweight='bold')
p1 = ax.plot(time_graduation, car_densities[0], color='red',
             marker='o', markersize=12)
p2 = ax.plot(time_graduation, car_densities[1], color='blue',
             marker='o', markersize=12)
p3 = ax.plot(time_graduation, car_densities[2], color='green',
             marker='o', markersize=12)
plt.margins(x=0.0, y=0.0, tight=False)

plt.grid(color="#FFFFFF")

col_label = (
    "t = " + "8 sec(s)",
    "$\\bf{Min.}$" + "$\\bf{Density}$",
    "$\\bf{Max.}$" + "$\\bf{Density}$",
    "$\\bf{Avg.}$" + "$\\bf{Density}$",
    "$\\bf{Reached}$" + " " + "$\\bf{Dest.}$" +
    "\n" +
    "$\\bf{AV}$" + " : " + "$\\bf{HV}$" + " : "
    # + "$\\bf{No}$" + " " + "$\\bf{Label}$"
)

cell_text = (("$\\bf{TL}$",
              str(min(car_densities[0])),
              str(max(car_densities[0])),
              str(round(sum(car_densities[0]) / len(car_densities[0]), 2)),
              str(num_of_passed_cars[0][0]) + ":" +
              str(num_of_passed_cars[0][1])
              # + ":" + str(num_of_passed_cars[0][2])
              ),
             ("$\\bf{CAwSD4WI}$",
              str(min(car_densities[1])),
              str(max(car_densities[1])),
              str(round(sum(car_densities[1]) / len(car_densities[1]), 2)),
              str(num_of_passed_cars[1][0]) + ":" +
              str(num_of_passed_cars[1][1])
              # + ":" + str(num_of_passed_cars[1][2])
              ),
             ("$\\bf{RN}$",
              str(min(car_densities[2])),
              str(max(car_densities[2])),
              str(round(sum(car_densities[2]) / len(car_densities[0]), 2)),
              str(num_of_passed_cars[2][0]) + ":" +
              str(num_of_passed_cars[2][1])
              # + ":" + str(num_of_passed_cars[2][2])
              )
             )

the_table = ax.table(cellText=cell_text,
                     colLabels=col_label,
                     colWidths=[.1] * len(col_label),
                     loc='bottom',
                     bbox=[0.0, -0.43, 0.55, 0.27])

the_table.scale(1.0, 1.0)

for (row, col), cell in the_table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='normal', size=28))

cellDict = the_table.get_celld()
for i in range(0, len(col_label)):
    cellDict[(0, i)].set_height(.09)
    for j in range(1, len(cell_text) + 1):
        cellDict[(j, i)].set_height(.05)

fig.text(0.764, .17,
         "$\\bf{Total}$" + " " + "$\\bf{AV}$:" + "120" + "   " +
         "$\\bf{Total}$" + " " + "$\\bf{HV}$:" + "120" + "\n", fontsize=26,
         linespacing=2)

# legend
ax.legend((p1[0], p2[0], p3[0]),
          ('Traffic Lights',
           'Collision Avoidance w/ Safe Distance & 4 Way Intersection',
           'Reservation Nodes'),
          fontsize=24)

ax.set_ylim(ymin=min([min(car_densities[0]),
                      min(car_densities[1]),
                      min(car_densities[2])]) - 0.1,
            ymax=max([max(car_densities[0]),
                      max(car_densities[1]),
                      max(car_densities[2])]) + 0.1)

ax.set_xlim(xmin=min(time_graduation),
            xmax=max(time_graduation) + 1)

plt.xlabel('Intervals in seconds (secs)', fontsize=26, labelpad=40,
           fontweight='bold')
plt.ylabel('Density (veh / kilometre)', fontsize=26, labelpad=40,
           fontweight='bold')

# x and y-axes labels
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

fig.subplots_adjust(bottom=0.3)
plt.savefig('density' + '.png')
plt.close()
