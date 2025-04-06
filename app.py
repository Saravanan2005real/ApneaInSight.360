from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os
import librosa
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from chatbot import get_chatbot_response

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize LabelEncoder
label_encoder = LabelEncoder()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load models
model_sleep = joblib.load('trained_sleep_model.pkl')
with open('model.pkl', 'rb') as f:
    model_advice = joblib.load(f)
with open('preprocessor.pkl', 'rb') as f:
    preprocessor = joblib.load(f)
with open("snore_model.pkl", "rb") as f:
    snore_model = joblib.load(f)

def extract_features(file_path):
    """Extract audio features for snoring analysis."""
    try:
        y, sr = librosa.load(file_path, sr=22050)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        mel = librosa.feature.melspectrogram(y=y, sr=sr)
        features = np.hstack([np.mean(mfccs, axis=1), np.mean(chroma, axis=1), np.mean(mel, axis=1)])
        return features
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def calculate_sleep_quality(ahi, snoring_score, oxygen_saturation, pulse):
    """Calculate overall sleep quality score based on multiple factors."""
    # Normalize values
    ahi_score = max(0, 100 - (ahi * 2))  # Convert AHI to score (0-100)
    snoring_score_norm = max(0, 100 - (snoring_score * 10))  # Convert snoring score (0-100)
    oxygen_score = (oxygen_saturation - 80) * 5  # Convert oxygen saturation to score (0-100)
    pulse_score = max(0, 100 - abs(pulse - 60) * 2)  # Convert pulse to score (0-100)
    
    # Weighted average
    weights = {'ahi': 0.4, 'snoring': 0.3, 'oxygen': 0.2, 'pulse': 0.1}
    total_score = (
        ahi_score * weights['ahi'] +
        snoring_score_norm * weights['snoring'] +
        oxygen_score * weights['oxygen'] +
        pulse_score * weights['pulse']
    )
    
    # Convert to quality level
    if total_score >= 90:
        return "Good"
    elif total_score >= 80:
        return "Very Mild"
    elif total_score >= 70:
        return "Mild"
    elif total_score >= 60:
        return "Moderate"
    elif total_score >= 50:
        return "Moderately Poor"
    elif total_score >= 40:
        return "Poor"
    elif total_score >= 30:
        return "Very Poor"
    else:
        return "Extremely Poor"

def predict_ahi(bmi, oxygen_saturation, snore_score, age, pulse_rate):
    """Predict AHI based on key factors with improved accuracy."""
    # Base AHI calculation based on BMI (primary factor)
    base_ahi = 0
    
    # BMI impact (strong correlation)
    if bmi >= 40:
        base_ahi = 35  # Severe obesity
    elif bmi >= 35:
        base_ahi = 25  # Moderate obesity
    elif bmi >= 30:
        base_ahi = 15  # Mild obesity
    elif bmi >= 25:
        base_ahi = 8   # Overweight
    else:
        base_ahi = 3   # Normal weight

    # Oxygen saturation impact (inverse relationship)
    oxygen_factor = 0
    if oxygen_saturation < 90:
        oxygen_factor = 12  # Severe desaturation
    elif oxygen_saturation < 93:
        oxygen_factor = 8   # Moderate desaturation
    elif oxygen_saturation < 95:
        oxygen_factor = 4   # Mild desaturation
    else:
        oxygen_factor = 0   # Normal saturation

    # Snoring impact (weighted less than BMI and oxygen)
    snoring_factor = snore_score * 1.5  # Reduced impact

    # Age impact (older age increases risk)
    age_factor = 0
    if age >= 60:
        age_factor = 4
    elif age >= 50:
        age_factor = 2
    elif age >= 40:
        age_factor = 1
    else:
        age_factor = 0

    # Pulse rate impact (minimal impact)
    pulse_factor = 0
    if pulse_rate >= 90:
        pulse_factor = 2
    elif pulse_rate >= 80:
        pulse_factor = 1
    else:
        pulse_factor = 0

    # Calculate final AHI with weighted factors
    final_ahi = (
        base_ahi * 0.5 +           # BMI is most important (50%)
        oxygen_factor * 0.3 +      # Oxygen saturation (30%)
        snoring_factor * 0.1 +     # Snoring (10%)
        age_factor * 0.05 +        # Age (5%)
        pulse_factor * 0.05        # Pulse rate (5%)
    )
    
    # Apply non-linear scaling to prevent extreme values
    final_ahi = final_ahi * (1 - 0.1 * (final_ahi / 100))  # Diminishing returns
    
    # Ensure AHI is within reasonable range (0-100)
    final_ahi = max(0, min(100, final_ahi))
    
    # Round to one decimal place
    return round(final_ahi, 1)

def get_severity_level(ahi):
    """Get severity level based on AHI score."""
    if ahi >= 30:
        return "Severe"
    elif ahi >= 15:
        return "Moderate"
    elif ahi >= 5:
        return "Mild"
    else:
        return "Normal"

def get_weight_category(bmi):
    """Get weight category based on BMI."""
    if bmi >= 40:
        return "Severe Obesity"
    elif bmi >= 35:
        return "Moderate Obesity"
    elif bmi >= 30:
        return "Mild Obesity"
    elif bmi >= 25:
        return "Overweight"
    else:
        return "Normal Weight"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Required fields check
        required_fields = ['age', 'gender', 'weight', 'height', 'oxygen_saturation', 'pulse', 'BPsys', 'BPdia']
        for field in required_fields:
            if field not in request.form or request.form[field].strip() == '':
                raise ValueError(f"Missing input: {field}")

        # Collect user input
        age = float(request.form.get('age'))
        gender = request.form.get('gender')
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height')) / 100  # Convert cm to meters
        oxygen_saturation = float(request.form.get('oxygen_saturation'))
        pulse_rate = float(request.form.get('pulse'))
        BPsys = float(request.form.get('BPsys'))
        BPdia = float(request.form.get('BPdia'))

        # Calculate BMI
        bmi = round(weight / (height ** 2), 2)

        # Process Snoring Sound File (Detect Snoring Severity)
        snore_score = 0  # Default if no file
        if 'snoringSound' in request.files and request.files['snoringSound'].filename != '':
            audio_file = request.files['snoringSound']
            filename = secure_filename(audio_file.filename)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(audio_path)

            # Extract features from audio and predict snoring severity
            features = extract_features(audio_path)
            if features is not None:
                features = features.reshape(1, -1)
                snore_score = snore_model.predict(features)[0]
            else:
                snore_score = 0

        # Predict AHI using the new function
        predicted_ahi = predict_ahi(bmi, oxygen_saturation, snore_score, age, pulse_rate)

        # Get severity level and weight category
        severity = get_severity_level(predicted_ahi)
        weight_category = get_weight_category(bmi)

        # Calculate overall sleep quality
        sleep_quality = calculate_sleep_quality(predicted_ahi, snore_score, oxygen_saturation, pulse_rate)
        
        # Calculate sleep quality percentage
        sleep_quality_map = {
            "Extremely Poor": 20,
            "Very Poor": 40,
            "Poor": 50,
            "Moderately Poor": 60,
            "Moderate": 70,
            "Mild": 80,
            "Very Mild": 90,
            "Good": 100
        }
        sleep_quality_percentage = sleep_quality_map.get(sleep_quality, 50)

        # Generate doctor's recommendation based on severity
        if predicted_ahi >= 30:
            doctor_recommendation = "🚨 URGENT: Immediate specialist consultation required. Severe sleep apnea detected with high risk of complications."
        elif predicted_ahi >= 20:
            doctor_recommendation = "⚠️ Critical: Severe condition detected. Medical intervention is necessary. Consider CPAP therapy."
        elif predicted_ahi >= 15:
            doctor_recommendation = "⚠️ Severe: Strongly recommended to consult a sleep specialist. Lifestyle changes and medical treatment may be needed."
        elif predicted_ahi >= 10:
            doctor_recommendation = "🔶 High Risk: Lifestyle changes & medical guidance suggested. Consider weight management and sleep position therapy."
        elif predicted_ahi >= 5:
            doctor_recommendation = "🟡 Moderate Risk: Medical consultation advised. Focus on sleep hygiene and weight management."
        elif predicted_ahi >= 3:
            doctor_recommendation = "🟢 Mild: Consider lifestyle changes & monitor symptoms. Maintain healthy sleep habits."
        else:
            doctor_recommendation = "✅ No sleep apnea detected. Continue maintaining healthy sleep habits."

        # Prepare data for nutrition & sleep advice model
        advice_data = pd.DataFrame({
            'AHI': [predicted_ahi],
            'BMI': [bmi],
            'Severity': [label_encoder.fit_transform([severity])[0]],
            'Weight Category': [label_encoder.fit_transform([weight_category])[0]]
        })
        
        # Preprocess and predict
        advice_data_scaled = preprocessor.transform(advice_data)
        personalized_advice = model_advice.predict(advice_data_scaled)[0]

        return render_template('result.html', 
                             prediction=severity,
                             ahi_score=predicted_ahi,
                             bmi=round(bmi, 1),
                             weight_category=weight_category,
                             sleep_quality=sleep_quality,
                             sleep_quality_percentage=sleep_quality_percentage,
                             recommendation=doctor_recommendation,
                             nutrition_advice=personalized_advice,
                             snore_score=round(snore_score, 1),
                             oxygen_saturation=oxygen_saturation,
                             pulse_rate=pulse_rate,
                             bp_sys=BPsys,
                             bp_dia=BPdia,
                             age=age)

    except Exception as e:
        print("Error occurred:", e)
        return render_template('prediction.html', error=f"Error: {str(e)}")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        response = get_chatbot_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
