import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns

# 1. Loading the data
data_all = pd.read_csv("combined_porogen_data.csv", sep=",")

# 2. Splitting columns for the composition tipe and membrane side
data_all["Composition"] = data_all["Composites"].apply(
    lambda x: x.split("_")[0]
)
data_all["Side"] = data_all["Composites"].apply(
    lambda x: x.split("_")[1] if "_" in str(x) else "unknown"
)
data_all["Side"] = data_all["Side"].str.lower()

# 3. Converting µm² to nm²
data_all["Area_nm2"] = data_all["Area"] * 1e6

# 4. Calculating base-10 logarithm
data_all["Log_Area_nm2"] = np.log10(data_all["Area_nm2"])

# Setting up specific sequence of samples on X axis
comp_order = ["PLA70", "PLA75", "PLA80", "PLA85", "PLA90", "PLA95"]

# 5. Setting up the boxplot
fig, ax = plt.subplots(figsize=(12, 7))

# Using standard boxplot visualization
sns.boxplot(
    x="Composition",
    y="Log_Area_nm2",
    hue="Side",
    data=data_all,
    order=comp_order,
    hue_order=["top", "bottom"],
    palette="Purples",
    linewidth=1.5,
    fliersize=4,
    ax=ax,
)

# 6. Setting up visually clear Y axis in microns (Recalculating it from log nanometers)
ax.set_ylabel("Pore Area, $\mu m^2$ (Log Scale)", fontsize=18, labelpad=15)

def to_microns_label(y, pos):
    val_nm2 = 10**y  # Converting logarithm back to nm²
    val_um2 = val_nm2 / 1e6  # Converting nm² to µm²

    if val_um2 >= 1:
        return f"{val_um2:g}"
    elif val_um2 >= 0.001:
        return f"{val_um2:.3f}".rstrip("0").rstrip(".")
    else:
        return f"{val_um2:.5f}".rstrip("0").rstrip(".")


ax.yaxis.set_major_formatter(ticker.FuncFormatter(to_microns_label))

# 7. Setting up axis and grid
plt.grid(True, color="grey", linewidth="0.2", axis="y")

ax.set_xlabel("Composites", fontsize=18, labelpad=10)
ax.tick_params(axis="x", labelsize=18)
ax.tick_params(axis="y", labelsize=18)

# Setting up the legend
ax.legend(title="Side", title_fontsize=14, fontsize=12, loc="upper right")

plt.tight_layout()
plt.savefig('boxplot_pores.png', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.savefig('boxplot_pores.tiff', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()
