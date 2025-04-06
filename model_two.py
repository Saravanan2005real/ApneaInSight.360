import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline

# Load the dataset
df = pd.read_csv('data/nutrition.csv')

# Encode categorical columns
label_encoder = LabelEncoder()
df['Severity'] = label_encoder.fit_transform(df['Severity'])
df['Weight Category'] = label_encoder.fit_transform(df['Weight Category'])

# Encode target column 'Personalized Nutrition & Sleep Advice' as categorical label
y = df['Personalized Nutrition & Sleep Advice']

# Prepare features (X) - Using available features
X = df[['AHI', 'BMI', 'Severity', 'Weight Category']]

# Handle missing values
X = X.fillna(X.mean())

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Create preprocessing pipeline
preprocessor = Pipeline([
    ('scaler', StandardScaler())
])

# Fit and transform the training data
X_train_scaled = preprocessor.fit_transform(X_train)
X_test_scaled = preprocessor.transform(X_test)

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

# Initialize and train the model with hyperparameter tuning
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

model = GradientBoostingClassifier(random_state=42)
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_resampled, y_train_resampled)

# Get the best model
best_model = grid_search.best_estimator_

# Test the model
y_pred = best_model.predict(X_test_scaled)

# Calculate and print the accuracy and classification report
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.2f}')
print('\nClassification Report:')
print(classification_report(y_test, y_pred))

# Save the trained model and preprocessor
with open('model.pkl', 'wb') as model_file:
    pickle.dump(best_model, model_file)

with open('preprocessor.pkl', 'wb') as preprocessor_file:
    pickle.dump(preprocessor, preprocessor_file)

def get_personalized_advice(ahi, bmi, severity, weight_category):
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'AHI': [ahi],
        'BMI': [bmi],
        'Severity': [severity],
        'Weight Category': [weight_category]
    })
    
    # Load the preprocessor and model
    with open('preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Preprocess and predict
    input_scaled = preprocessor.transform(input_data)
    predicted_advice = model.predict(input_scaled)
    
    return predicted_advice[0]

# Example usage
advice = get_personalized_advice(
    ahi=15,
    bmi=25,
    severity=2,  # Moderate
    weight_category=2  # Overweight
)
print(f"Personalized Nutrition & Sleep Advice: {advice}")