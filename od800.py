import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['font.size'] = 16

# data import
raw_data = pd.read_csv('spectroturbidimetry.csv', sep=',')

# 1. Making united grid from 400 to 800 nm with 1 nm step
target_wavelengths = np.arange(400, 801, 1)

interpolated_rows = []
all_sample_names = raw_data['SampleName'].unique()

# 2. Automated cycle of interpolation
for name in all_sample_names:
    # Taking each sample (e.g. PLA85_n1_N1)
    sub_df = raw_data[raw_data['SampleName'] == name]

    # Taking its X and Y
    x_real = sub_df['Wavelength'].values
    y_real = sub_df['OD'].values

    # Checking for data sufficiency
    if len(x_real) < 2:
        continue

    # Taking function of linear interpolation
    # bounds_error=False and fill_value="extrapolate" saves the day if it is less than 800 nm, but for my data it's ok
    f_interp = interp1d(x_real, y_real, kind='linear', bounds_error=False, fill_value="extrapolate")

    # Taking proper OD values for united grid
    y_interpolated = f_interp(target_wavelengths)

    # Writing results in 'flat' way
    for wl, od in zip(target_wavelengths, y_interpolated):
        interpolated_rows.append({
            'SampleType': sub_df['SampleType'].iloc[0],
            'SampleName': name,
            'Wavelength': wl,
            'OD': od
        })

# 3. Final dataset with finally united grid
plot_df = pd.DataFrame(interpolated_rows)

# 1. Taking values between 799 and 800 nm
# it automatically takes all 9 repeats for each SampleType)
od800_data = plot_df[(plot_df['Wavelength'] > 799) & (plot_df['Wavelength'] < 801)]

# 2. Calculating means and SDs
stats = od800_data.groupby('SampleType')['OD'].agg(['mean', 'std']).reset_index()
# Sorting
custom_order = ['PLA95', 'PLA90', 'PLA85', 'PLA80', 'PLA75']
stats['SampleType'] = pd.Categorical(stats['SampleType'], categories=custom_order, ordered=True)
stats = stats.sort_values('SampleType')
print(stats)
# Error bars
labels = stats['SampleType'].values      # group names: e.g. ['PLA75', 'PLA80', 'PLA85']
means = stats['mean'].values            # set of mean OD800s
errors = stats['std'].values            # set of SDs
x_coords = range(len(labels))           # x coordinates

# 3. Plotting
plt.figure(figsize=(6, 5))

# Dots with errorbars
plt.errorbar(
    x_coords,
    means,
    yerr=errors,
    fmt="o",  # 'o' circular marker for mean values
    color="#1f77b4",  # blue color
    markersize=8,  # central dot size
    markeredgecolor="black",  # borderline color
    markeredgewidth=1.5,  # borderline width
    linewidth=2,  # errorbar borderline width
    capsize=6,  # the width of horizontal errorbar lines
    ecolor="black",  # errorbar color)
    label="Mean ± SD",
    zorder=3,
)

# Line between points
plt.plot(
    x_coords,
    means,
    linestyle="--",
    color="#1f77b4",
    linewidth=2,
    alpha=0.6,
    label="line",
    zorder=2,
)

# Optical density of the blending emulsions at λ = 800 nm as a function of composition (Mean ± SD)
plt.xticks(x_coords, labels)
plt.xlabel("Composite Type")
plt.ylabel("OD800")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig('od800_new.png', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.savefig('od800_new.tiff', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()