import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

# --- Synthetic Data Generation ---
def generate_synthetic_data(n_samples=5000):
    np.random.seed(42)
    # Features
    age = np.random.randint(16, 65, n_samples)
    gender = np.random.choice(['male', 'female', 'other'], n_samples)
    experience = np.random.randint(0, 10, n_samples)  # years
    goal = np.random.choice(['strength', 'hypertrophy', 'endurance', 'weight_loss'], n_samples)
    days_per_week = np.random.randint(2, 7, n_samples)
    equipment = np.random.choice(['minimal', 'dumbbells', 'barbell', 'full_gym'], n_samples)
    injuries = np.random.choice(['none', 'shoulder', 'knee', 'back'], n_samples)

    # Target: split type
    split_type = []
    for d, g in zip(days_per_week, goal):
        if d <= 3:
            split_type.append('full_body')
        elif d == 4:
            split_type.append('upper_lower' if g in ['strength'] else 'push_pull_legs')
        else:
            split_type.append('body_part' if g == 'hypertrophy' else 'push_pull_legs')

    # Target: structure (sets, reps, rest)
    sets = []
    reps = []
    rest = []
    for g, exp in zip(goal, experience):
        if g == 'strength':
            sets.append(5 + (exp > 2))
            reps.append(4)
            rest.append(180)
        elif g == 'hypertrophy':
            sets.append(4 + (exp > 2))
            reps.append(10)
            rest.append(90)
        elif g == 'endurance':
            sets.append(3)
            reps.append(18)
            rest.append(60)
        else:
            sets.append(3)
            reps.append(12)
            rest.append(60)

    df = pd.DataFrame({
        'age': age,
        'gender': gender,
        'experience': experience,
        'goal': goal,
        'days_per_week': days_per_week,
        'equipment': equipment,
        'injuries': injuries,
        'split_type': split_type,
        'sets': sets,
        'reps': reps,
        'rest': rest
    })
    return df

# --- Model Training ---
def train_and_save_models():
    df = generate_synthetic_data()
    X = df[['age', 'gender', 'experience', 'goal', 'days_per_week', 'equipment', 'injuries']]
    y_split = df['split_type']
    y_sets = df['sets']
    y_reps = df['reps']
    y_rest = df['rest']

    # Encode categorical features
    X_enc = X.copy()
    encoders = {}
    for col in ['gender', 'goal', 'equipment', 'injuries']:
        le = LabelEncoder()
        X_enc[col] = le.fit_transform(X[col])
        encoders[col] = le

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_enc)

    # Split type classifier
    split_le = LabelEncoder()
    y_split_enc = split_le.fit_transform(y_split)
    split_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    split_clf.fit(X_scaled, y_split_enc)

    # Structure regressors
    sets_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    sets_reg.fit(X_scaled, y_sets)
    reps_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reps_reg.fit(X_scaled, y_reps)
    rest_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    rest_reg.fit(X_scaled, y_rest)

    # Save models and encoders
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(scaler, os.path.join(model_dir, 'workout_scaler.joblib'))
    joblib.dump(encoders, os.path.join(model_dir, 'workout_encoders.joblib'))
    joblib.dump(split_le, os.path.join(model_dir, 'split_label_encoder.joblib'))
    joblib.dump(split_clf, os.path.join(model_dir, 'split_classifier.joblib'))
    joblib.dump(sets_reg, os.path.join(model_dir, 'sets_regressor.joblib'))
    joblib.dump(reps_reg, os.path.join(model_dir, 'reps_regressor.joblib'))
    joblib.dump(rest_reg, os.path.join(model_dir, 'rest_regressor.joblib'))
    print('Workout ML models trained and saved!')

if __name__ == '__main__':
    train_and_save_models() 