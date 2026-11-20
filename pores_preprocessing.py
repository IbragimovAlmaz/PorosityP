import os
import re
import pandas as pd

# 1. Base directory should be named as 'porogen_content', extracted from Zenodo 10.5281/zenodo.22864555
# if the script is present right in this directory, keep it as '.'
BASE_DIR = './porogen_content'

all_results_data = []

print("=== STARTING THE DATASET PREPROCESSING ===")

# Going through the porogen_content folders
# Please, keep in mind that PLA70 was manually processed
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        # Keeping only Results1.csv, Results2.csv, Results3.csv files
        # Summary and other files are ignored automatically
        if file.startswith("Results") and file.endswith(".csv"):
            file_path = os.path.join(root, file)

            # Constructing file paths
            # Path example: ./porogen_content/PLA70_1/top/Results1.csv
            relative_path = os.path.relpath(file_path, BASE_DIR)
            path_parts = relative_path.split(os.sep)

            # Checkpoint: is the file present in the correct folder (path)?
            if len(path_parts) >= 3:
                folder_composite = path_parts[0]  # Example: 'PLA70_1'
                side = path_parts[1]  # Example: 'top' or 'bottom'
                file_name = path_parts[2]  # Example: 'Results1.csv'

                # Taking composition type and full repeat number (f) from the file name
                # Extracting sample repeat number right after the '_' (Example: 'PLA70_1' -> 'PLA70', '1')
                match_folder = re.match(r"(.+)_(\d+)$", folder_composite)
                if match_folder:
                    composite_base = match_folder.group(1)  # 'PLA70'
                    full_repeat = match_folder.group(2)  # '1'
                else:
                    composite_base = folder_composite
                    full_repeat = "unknown"

                # Extracting the number of tech repeat (t) from the final file name (Example: 'Results1.csv' -> '1')
                match_file = re.search(r"Results(\d+)\.csv", file_name)
                tech_repeat = match_file.group(1) if match_file else "unknown"

                # Constructing the final names for new columns
                # Example: 'PLA70_top'
                composite_label = f"{composite_base}_{side}"
                # Example: 't1f1' (means technical repeat 1, full repeat 1)
                iteration_label = f"t{tech_repeat}f{full_repeat}"

                try:
                    # Reading the original csv from Fiji (raw data are not changed!)
                    df = pd.read_csv(file_path)

                    # Adding new columns to the beginning (Fiji-data goes right)
                    df.insert(0, 'Iteration', iteration_label)
                    df.insert(0, 'Composites', composite_label)

                    all_results_data.append(df)
                    print(
                        f"Successfully reading: {folder_composite}/{side}/{file_name} -> {composite_label} | {iteration_label}")

                except Exception as e:
                    print(f"Error, file location: {relative_path}: {e}")

# 2. Combining all data to the united file
if all_results_data:
    final_dataset = pd.concat(all_results_data, ignore_index=True)

    # Saving the final file one level up, outside from the raw data directory
    output_path = os.path.join(os.path.dirname(BASE_DIR) if BASE_DIR != '.' else '.', "combined_porogen_data.csv")
    final_dataset.to_csv(output_path, index=False)

    print("\n" + "=" * 60)
    print("SUCCESSFULLY CONSTRUCTED THE FINAL DATASET!")
    print(f"Final file was saved in: {output_path}")
    print(f"Overall pores (rows) united: {len(final_dataset)}")
    print("=" * 60)
else:
    print("\nError: files 'Results*.csv' were not found in the directory.")
