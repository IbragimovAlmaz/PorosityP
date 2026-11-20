import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns

# 1. Loading the data
data_all = pd.read_csv("combined_porogen_data.csv", sep=",")

# 2. Preprocessing
data_all["Composition"] = data_all["Composites"].apply(
    lambda x: x.split("_")[0]
)
data_all["Side"] = data_all["Composites"].apply(
    lambda x: x.split("_")[1] if "_" in str(x) else "unknown"
)
data_all["Side"] = data_all["Side"].str.lower()

comp_order = ["PLA70", "PLA75", "PLA80", "PLA85", "PLA90", "PLA95"]

# Making to subplots: one for the 'Top', another for the 'Bottom' sides
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Setting palette (customized purples)
colors = sns.color_palette("Purples", len(comp_order) + 3)[3:]

for ax, side in zip([ax1, ax2], ["top", "bottom"]):
    ax.set_title(f"Surface Porosity: {side.upper()} side", fontsize=14, pad=10)

    for i, comp in enumerate(comp_order):
        # Filtering data for the specific composition and membrane side
        sub_data = data_all[
            (data_all["Composition"] == comp) & (data_all["Side"] == side)
        ]["Area"].dropna()

        if len(sub_data) == 0:
            continue

        # Sorting pore areas in ascending order (critical for cumulative distribution)
        sorted_areas = np.sort(sub_data)

        # Calculating the cumulative sum of pore areas in percents
        total_area = np.sum(sorted_areas)
        cum_area = np.cumsum(sorted_areas) / total_area * 100

        # Making cumulative curve
        ax.plot(
            sorted_areas,
            cum_area,
            label=comp,
            color=colors[i],
            lw=2.5,
            alpha=0.9,
        )

    # Setting subplot axis
    ax.set_xscale("log")
    ax.set_xlabel("Individual Pore Area ($\mu m^2$)", fontsize=12)
    ax.set_ylim(0, 102)
    ax.grid(True, which="both", ls="--", alpha=0.3, color="grey")
    ax.tick_params(axis="both", labelsize=11)

# Setting the Y axis
ax1.set_ylabel("Cumulative Area Fraction (%)", fontsize=12)

# Adding the legend to one subplot, just to avoid duplicating it
ax2.legend(title="Composition", fontsize=11, title_fontsize=12, loc="lower right")

# Formatting logarithmic X axis for the clear representation
for ax in [ax1, ax2]:
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f"{x:g}")
    )

plt.tight_layout()
plt.savefig('curves_cumulativep.png', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.savefig('curves_cumulativep.tiff', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()
