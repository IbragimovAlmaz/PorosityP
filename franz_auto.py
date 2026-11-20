import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

# 1. Calibration for Methylene Blue, OD=665
# Water background
water_background1 = 0.0357000008225441
water_background2 = 0.0362000018358231
water_background3 = 0.0357000008225441
# Calibration curves
calibration1 = np.array([1.05190002918243, 0.578599989414215, 0.322200000286102, 0.178399994969368, 0.103200003504753, 0.0706999972462654, 0.0505999997258186, 0.0432999990880489])
calibration2 = np.array([1.06340003013611, 0.589299976825714, 0.322899997234345, 0.181600004434586, 0.108300000429153, 0.0706000030040741, 0.0533000007271767, 0.0427000001072884])
calibration3 = np.array([1.07819998264313, 0.597500026226044, 0.324600011110306, 0.180500000715256, 0.107500001788139, 0.0707999989390373, 0.0511999987065792, 0.0439999997615814])
# Concentrations in μg/ml, reshape for further regression
X_concentrations = np.array([10, 5, 2.5, 1.25, 0.625, 0.3125, 0.15625, 0.078125]).reshape(-1, 1)

# Making calculation
cal1_corrected = np.clip(calibration1 - water_background1, 0, None)
cal2_corrected = np.clip(calibration2 - water_background2, 0, None)
cal3_corrected = np.clip(calibration3 - water_background3, 0, None)
# Calculating mean ODs for each concentration (which is Y)
calibration_matrix = np.vstack([cal1_corrected, cal2_corrected, cal3_corrected])
y_mean_od = np.mean(calibration_matrix, axis=0)
# Calculating force zero interception in linear regression (y = a * x)
# fit_intercept=False disables constant (Const), forcing zero interception
calib_model = LinearRegression(fit_intercept=False)
calib_model.fit(X_concentrations, y_mean_od)
# Getting final coefficient 'a' and R-squared
a_coeff = calib_model.coef_[0]
r2_calib = calib_model.score(X_concentrations, y_mean_od)
print("=== Calibration results ===")
print(f"Coefficient (a): {a_coeff:.7f}")
print(f"R-squared (R²): {r2_calib:.5f}")

# Plotting regression
# Calculating Y for the regression line
y_pred_calib = calib_model.predict(X_concentrations)
fig, ax = plt.subplots(figsize=(7, 5), clear=True) # or figsize=(8, 6)
# Scatter of experimental values
ax.scatter(X_concentrations, y_mean_od, color='#5b9bd5', alpha=0.8,
           edgecolors='#333333', linewidths=0.7, s=40,
           label="Experimental Data (Mean OD)")
# The model
ax.plot(X_concentrations, y_pred_calib, color='red', linestyle='-', linewidth=2,
        label=f"Linear Fit ($y = a \\cdot x$, $a$ = {a_coeff:.5f}, $R^2$ = {r2_calib:.4f})")
# Labels
ax.set_title("Calibration Curve for Methylene Blue Dye ($\\lambda$ = 665 nm)", fontsize=12, fontweight='bold')
ax.set_xlabel('Concentration ($\\mu$g/mL)', fontsize=10)
ax.set_ylabel('Optical Density (OD)', fontsize=10)
# Making grid and saving
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig("fit_MB_new.png", dpi=300)
plt.close(fig)
print("Calibration curve successfully saved as fit_MB.png!")



# Enter iteration's file path !!!
file_path = 'FranzPLA2.5mcm_n123.csv'

# Enter water background for this iteration !!!
water_background = 0.044599998742342

iterations = ['Iteration_1', 'Iteration_2', 'Iteration_3']
# Importing csv data here
df = pd.read_csv(file_path, index_col='hours')

# 2. Calculating concentrations based on experimental ODs
# Background correction
for col in iterations:
    df[col] = (df[col] - water_background).clip(lower=0)
# Making empty DataFrame to save concentrations further
df_conc = pd.DataFrame(index=df.index)
# Using Beer-Bouger-Lambert Law: A=ε*c*l, or here it is: OD=a*C, C=OD/a
for col in iterations:
    df_conc[f'Conc_{col}'] = df[col] / a_coeff
print("--- Calculated concentrations (μg/mL) without Pohry-Casper yet ---")
print(df_conc)

# 2. Calculating cumulative mass with Pohry-Casper correction (Franz cells)
V_receptor = 5.0  # ml
V_aliquot = 0.25  # ml
# Recalculating OD in current concentrations (C = OD / a) -> μg/ml
df_current_conc = pd.DataFrame(index=df.index)
for col in iterations:
    df_current_conc[f'Conc_{col}'] = df[col] / a_coeff
# Making new DataFrame for total accumulated MASS (μg)
df_cumul_mass = pd.DataFrame(index=df.index)
for col in iterations:
    curr_conc_col = f'Conc_{col}'
    # 1. Current mass in a Franz cell
    mass_in_receptor = df_current_conc[curr_conc_col] * V_receptor
    # 2. Taken mass in current aliquot
    mass_sampled = df_current_conc[curr_conc_col] * V_aliquot
    # 3. Sum of every previous aliquot (shifting 1 step down)
    prev_sampled_mass_loss = mass_sampled.cumsum().shift(1).fillna(0)
    # 4. Final cumulative mass
    df_cumul_mass[f'Cumul_Mass_{col}'] = mass_in_receptor + prev_sampled_mass_loss

# Marking numbered days/hours as hours
df_cumul_mass.index.name = 'hours'
# Saving to CSV
df_cumul_mass.to_csv(f'final_{file_path}', index=True)
print("--- Cumulative mass of the release (μg) ---")
print(df_cumul_mass)

