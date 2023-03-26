import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import scienceplots
import sys
import locale

# Style options
plt.style.use("science")
fig, ax = plt.subplots(figsize=(16, 8))

# First number gives you the set, second and third gives you the initial and final runs, respectively.
runset = int(sys.argv[1])
run_init = int(sys.argv[2])
run_fin = int(sys.argv[3])

# Initiate empty vectors
time = []  # Time vector (not working yet)
voltage = []  # Voltage points (first column in the file)
error = []  # Error points (second column)
distance = []  # Distance points (last column)
runends = []  # A vector to store the points at which each run ends.
runstart = 0

# For every run in the range, open the corresponding file and then extend the global vectors
for run in range(run_init, run_fin + 1):
    filename = "Set_" + str(runset) + "/regelungsrun_1." + str("{:04d}".format(run))
    v, e, d = np.genfromtxt(filename, unpack=True)
    t = np.arange(len(voltage))
    time.extend(t)
    voltage.extend(v)
    error.extend(e)
    distance.extend(d)
    runends.append(len(voltage))
    runstart = len(voltage)


# Chose max and min for plotting
distance = [x + 19.7 for x in distance]
miny = min(distance) - min(distance) % 5
maxy = min(max(distance) + (5 - max(distance) % 5), 50)

# Add vertical lines at the last point of every run
ax.vlines(
    runends,
    ymin=miny,
    ymax=maxy,
    color="Grey",
    linestyle="-",
)

# For every run, add a label under the x-axis and slightly to the right of the drawn line
for run in range(run_init, run_fin + 1):
    if run == run_init:
        ax.text(500, miny - 2.5, "Run " + str(run), rotation="vertical")
    else:
        ax.text(
            runends[run - 4] + 500, miny - 2.5, "Run " + str(run), rotation="vertical"
        )

# Plot plunger distances
distcol = "C0"
ax.plot(distance, color=distcol)
ax.set_ylim(miny, maxy)
ax.set_ylabel("Plunger opening [µm]")
# ax.spines["left"].set_color(distcol)
# ax.yaxis.label.set_color(distcol)
# ax.tick_params(axis="y", colors=distcol)
ax.grid(which="both")

ax.set_xlim(0, len(voltage))
ax.set_xticks([])  # Remove axis ticks

# Plot voltages on the same plot as before
"""
voltcol = "C3"
ax2 = ax.twinx()
ax2.plot(voltage, color=voltcol)
ax2.set_ylabel("Plunger Voltage [V]")
ax2.spines["right"].set_color(voltcol)
ax2.yaxis.label.set_color(voltcol)
ax2.tick_params(axis="y", colors=voltcol)
"""

# Save the fig as a pdf with an automatic name
plt.savefig(
    "outputs/PlungerDistance_Set"
    + str(runset)
    + "_"
    + str(run_init)
    + "_"
    + str(run_fin)
    + ".pdf",
    bbox_inches="tight",
    transparent="True",
)
print("Average distance", "{:.2f}".format(sum(distance) / len(distance)), "µm")
