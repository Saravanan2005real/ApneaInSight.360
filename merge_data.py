import pandas as pd

# Load existing dataset
existing_df = pd.read_csv('data/patients.csv')  # Change this to your current dataset filename

# Load new dataset
new_df = pd.read_csv('data/sdb_dataset.csv')  # Change this if filename differs

# Merge datasets (remove duplicates)
merged_df = pd.concat([existing_df, new_df]).drop_duplicates()

# Save merged dataset
merged_df.to_csv('final_dataset.csv', index=False)

print("✅ Merging completed! New dataset saved as 'final_dataset.csv'.")
