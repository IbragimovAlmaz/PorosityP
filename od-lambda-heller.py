import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

# data import
raw_data = pd.read_csv('spectroturbidimetry.csv', sep=',')

# temporary results list
results_list = []

# Using .unique() to take every sample name (PLA95_n1_N1, PLA95_n1_N2, and etc.)
all_samples = raw_data['SampleName'].unique()

for name in all_samples:
    # 1. Data filtration for each certain iteration
    sample_data = raw_data[raw_data['SampleName'] == name]

    # Skipping transparent iterations PLA95 and PLA90
    if name.startswith(('PLA95', 'PLA90')):
        continue

    # 2. Compatibilzation/refraction change effects filtration for further logarithmization
    valid_data = sample_data[sample_data['OD'] > 0]

    # Checking for data efficiency and skipping poor iterations
    if len(valid_data) < 3:
        print(f"Warning: For {name} positive ODs are not efficient!")
        continue

    # 3. Taking values
    wavelengths = valid_data['Wavelength'].values
    od_values = valid_data['OD'].values

    # 4. Logarithmization for further Heller's approximation
    X = np.log(wavelengths).reshape(-1, 1)  # reshaping wavelength array to library specific 2D format
    y = np.log(od_values)

    # 5. Using linear regression (with constant C)
    model = LinearRegression()  # if no constant, add fit_intercept=False
    model.fit(X, y)

    alpha = -model.coef_[0]
    r_squared = model.score(X, y)
    y_pred = model.predict(X)   # predicted y for the plot

    # 6. Plotting results
    fig, ax = plt.subplots(figsize=(6, 5), clear=True) # or figsize=(8, 6)
    sample_type = valid_data['SampleType'].iloc[0]
    # Making experimental log(OD) vs log(wavelength)
    ax.scatter(X, y, color='#5b9bd5', alpha=0.7, edgecolors='#333333', linewidths=0.7, s=40,
               label=f"Experimental Data ({sample_type})")
    # The model
    ax.plot(X, y_pred, color='red', linestyle='-', linewidth=2,
            label=f"Heller's fit ($\\alpha$ = {alpha:.2f}, $R^2$ = {r_squared:.3f})")
    # Labels
    ax.set_xlabel(r'$\ln(\text{Wavelength})$', fontsize=16)
    ax.set_ylabel(r'$\ln(\text{Optical Density})$', fontsize=16)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    # Saving
    ax.legend(loc='best', frameon=True, fontsize=12)
    plt.tight_layout()
    plt.savefig(f"fit_{name}_new.tiff", dpi=300) # plt.savefig(f"fit_{name}.tiff", dpi=300)
    plt.close(fig)

    # 6. Adding this iteration to the list
    results_list.append({
        'SampleType': sample_type,  # saving type name (e.g., PLA85)
        'SampleName': name,
        'Alpha': alpha,
        'R_squared': r_squared
    })

# Transforming results list into final DataFrame
summary_df = pd.DataFrame(results_list)
# Sorting by sample types (PLA85, PLA80, PLA75)
summary_df.sort_values(by='SampleType', inplace=True)
# Saving to CSV
summary_df.to_csv('summary_df.csv', index=False)
print("\n--- Summary DataFrame ---")
print(summary_df)

# Group results by samples (PLA85, PLA80, PLA75) and calculating means for SD and alpha
final_stats = summary_df.groupby('SampleType')['Alpha'].agg(['mean', 'std']).reset_index()
# Rename stats columns
final_stats.columns = ['SampleType', 'Alpha_Mean', 'Alpha_SD']
# Saving to CSV
final_stats.to_csv('final_stats.csv', index=False)
print("\n--- Final Statistics ---")
print(final_stats)

