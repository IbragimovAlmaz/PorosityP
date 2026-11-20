import matplotlib.pyplot as plt

import pandas as pd

# 1. Enter processed file paths !!!
files = [
    'final_FranzPLA75_n123.csv',
    'final_FranzPLA80_n123.csv',
    'final_FranzPLA85_n123.csv'
]

# Setting up plot configurations
plt.figure(figsize=(8, 5), dpi=300)

for file in files:
    # Loading the dataset, setting up 'hours' as indexes
    df = pd.read_csv(file).set_index('hours')

    # Automatically cutting the correct name for the legend (For example, "PLA75")
    label_name = file.replace('final_Franz', '').split('_')[0]

    # Calculating mean and SD from strokes (axis=1) for all columns of all iterations
    df['Mean'] = df.mean(axis=1)
    df['SD'] = df.std(axis=1)

    # Plotting the basic line for the means
    line, = plt.plot(df.index, df['Mean'], marker='o', linewidth=2, label=label_name)

    # Plotting Shaded Error Bars
    plt.fill_between(
        df.index,
        df['Mean'] - df['SD'],
        df['Mean'] + df['SD'],
        color=line.get_color(),  # the same color as from line
        alpha=0.15  # transparency
    )

# Titles and labels
plt.title('Kinetics of membrane permeability via Franz Cells', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Time (hours)', fontsize=11)
plt.ylabel('Cumulative mass, $M_{cumul}$ ($\mu$g)', fontsize=11)

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(df.index)  # setting timepoints (0, 6, 12, 18...)
plt.legend(title="Membrane type", loc='upper left')

plt.tight_layout()
plt.savefig("franz18h.png", dpi=300)
plt.show()
