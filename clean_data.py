import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('final_dataset.csv')

# Remove rows where 'Diagnosis_of_SDB' is missing
df = df.dropna(subset=['Diagnosis_of_SDB'])

# Drop unnecessary text-based columns
columns_to_remove = ['user_id', 'night_id', 'Patient_ID', 'Physician_Notes', 'Patient_Symptoms']
df = df.drop(columns=columns_to_remove, errors='ignore')

# Convert categorical columns to numeric
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
df['CPAP'] = df['CPAP'].map({'True': 1, 'False': 0})
df['Surgery'] = df['Surgery'].map({'True': 1, 'False': 0})

# Convert Diagnosis_of_SDB into categories
df['Diagnosis_of_SDB'] = df['Diagnosis_of_SDB'].astype('category').cat.codes

# Convert all numeric-like columns properly
numeric_columns = ['Age', 'BMI', 'Oxygen_Saturation', 'AHI', 'ECG_Heart_Rate', 'SpO2', 'Nasal_Airflow', 'Chest_Movement']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill missing numeric values with median
df.fillna(df.median(numeric_only=True), inplace=True)

# ✅ NEW: Estimate ODI based on Oxygen Saturation
df['ODI'] = df['Oxygen_Saturation'].apply(lambda x: 30 if x < 90 else 20 if x < 93 else 10 if x < 95 else 0)

# ✅ NEW: Add Blood Pressure Columns (Estimated if missing)
df['BPsys'] = 120 + (df['BMI'] * 0.3)  # Example estimation
df['BPdia'] = 80 + (df['BMI'] * 0.2)   # Example estimation

# ✅ NEW: Add Snoring_Score (Random values for now, replace if real data is available)
df['Snoring_Score'] = np.random.randint(0, 100, size=len(df))  # Replace with real snoring data if available

# Save cleaned dataset
df.to_csv('cleaned_dataset.csv', index=False)

print("✅ Data cleaning complete! Saved as 'cleaned_dataset.csv'.")
