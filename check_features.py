import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load cleaned dataset
df = pd.read_csv('cleaned_dataset.csv')

# Select same features as in training
features = ['Age', 'BMI', 'Oxygen_Saturation', 'AHI', 'ECG_Heart_Rate', 'Snoring']
X = df[features]
y = df['Diagnosis_of_SDB']

# Train a simple RandomForest model
model = RandomForestClassifier(n_estimators=500, max_depth=15, random_state=42)
model.fit(X, y)

# Print feature importance
importances = model.feature_importances_
importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n🔥 Feature Importance 🔥")
print(importance_df)
