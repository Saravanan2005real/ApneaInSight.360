import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load cleaned dataset
df = pd.read_csv('cleaned_dataset.csv')

# ✅ CREATE MISSING FEATURES
df['BMI_Age'] = df['BMI'] * df['Age']
df['Oxygen_AHI'] = df['Oxygen_Saturation'] / (df['AHI'] + 1)  # Avoid division by zero
df['Heart_BMI'] = df['ECG_Heart_Rate'] / (df['BMI'] + 1)

# Select same features as in training
features = ['Age', 'BMI', 'Oxygen_Saturation', 'ODI', 'AHI',  
            'ECG_Heart_Rate', 'BMI_Age', 'Oxygen_AHI', 'Heart_BMI', 'Snoring_Score']
X = df[features]
y = df['Diagnosis_of_SDB']

# Train a simple RandomForest model
model = RandomForestClassifier(n_estimators=500, max_depth=10, random_state=42)
model.fit(X, y)

# Print feature importance
importances = model.feature_importances_
importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n🔥 Feature Importance 🔥")
print(importance_df)
