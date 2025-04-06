import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('final_dataset.csv')

# Convert categorical columns to strings to prevent conversion errors
df = df.astype(str)

# Check class balance
print("\n🔍 Diagnosis Class Distribution:")
print(df['Diagnosis_of_SDB'].value_counts(normalize=True) * 100)

# Convert numeric columns back (ignore categorical ones)
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except ValueError:
        print(f"⚠️ Column '{col}' is non-numeric and will be ignored in variance & correlation checks.")

# Check for low-variance features
low_variance_features = df.var(numeric_only=True)[df.var(numeric_only=True) < 0.01].index.tolist()
print("\n⚠️ Features with very low variance (remove these):", low_variance_features)

# Check for duplicate rows
duplicate_count = df.duplicated().sum()
print(f"\n📌 Duplicate rows in dataset: {duplicate_count}")

# Check for highly correlated features
correlation_matrix = df.corr(numeric_only=True)
high_correlation_pairs = [(i, j, correlation_matrix.loc[i, j])
                          for i in correlation_matrix.columns
                          for j in correlation_matrix.columns
                          if i != j and abs(correlation_matrix.loc[i, j]) > 0.9]

print("\n🔗 Highly Correlated Features (Consider removing one from each pair):")
for i, j, corr in high_correlation_pairs:
    print(f"{i} ↔ {j} (Correlation: {corr:.2f})")
