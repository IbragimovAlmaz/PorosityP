import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import seaborn as sns
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
    # bounds_error=False и fill_value="extrapolate" saves the day if it is less than 800 nm, but for my data it's ok
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

# Making logical order in the legend and plotting results
desired_order = ['PLA75', 'PLA80', 'PLA85', 'PLA90', 'PLA95']
plot_df['SampleType'] = pd.Categorical(plot_df['SampleType'], categories=desired_order, ordered=True)
fig, ax = plt.subplots(figsize=(6, 5))
plt.xlim(400, 800)

# Using custom colors for the palette
custom_colors = {
    'PLA95': '#1f77b4',  # blue
    'PLA90': '#ff7f0e',  # orange
    'PLA85': '#2ca02c',  # green
    'PLA80': '#d9383a',  # red
    'PLA75': '#815ca3'   # violet
}

# errorbar='sd' makes shaded errorbar with SDs
sns.lineplot(
    data=plot_df,
    x='Wavelength',
    y='OD',
    hue='SampleType',
    hue_order=desired_order,    # Legend order
    palette=custom_colors,      # Custom colors
    errorbar='sd',
    linewidth=2,
    ax=ax
)

ax.legend(title='Type', loc='best', frameon=True, fontsize=12)

#plt.title('Spectroturbidimetric profiles of PLA:PVP blending emulsions (Mean ± SD, n=3, N=3)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Optical Density (OD)')
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('curves_od_new.png', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.savefig('curves_od_new.tiff', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()

