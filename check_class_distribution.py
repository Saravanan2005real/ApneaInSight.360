import pandas as pd

# Load cleaned dataset
df = pd.read_csv('cleaned_dataset.csv')

# Check class distribution
print("\n🔍 Diagnosis Class Distribution:")
print(df['Diagnosis_of_SDB'].value_counts(normalize=True) * 100)
