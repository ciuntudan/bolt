#!/usr/bin/env python
import os
import sys
import django
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanSquaredError as MSE
import joblib
import warnings
warnings.filterwarnings('ignore')

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def create_enhanced_dataset():
    """Create a comprehensive dataset for meal planning"""
    np.random.seed(42)
    
    # Generate more diverse and realistic data
    n_samples = 50000
    
    # Basic user characteristics
    ages = np.random.normal(35, 12, n_samples).clip(18, 80)
    heights = np.random.normal(170, 10, n_samples).clip(140, 220)  # cm
    weights = np.random.normal(70, 15, n_samples).clip(40, 150)   # kg
    
    # Gender (0=female, 1=male)
    genders = np.random.choice([0, 1], n_samples, p=[0.5, 0.5])
    
    # Activity levels (0-4: sedentary to very_active)
    activity_levels = np.random.choice([0, 1, 2, 3, 4], n_samples, p=[0.15, 0.25, 0.35, 0.20, 0.05])
    
    # Goals (0=weight_loss, 1=maintenance, 2=muscle_gain)
    goals = np.random.choice([0, 1, 2], n_samples, p=[0.4, 0.4, 0.2])
    
    # Fitness levels (0=beginner, 1=intermediate, 2=advanced)
    fitness_levels = np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.5, 0.2])
    
    # Body fat percentage (realistic ranges)
    body_fat_male = np.random.normal(15, 5, n_samples).clip(8, 35)
    body_fat_female = np.random.normal(25, 7, n_samples).clip(15, 45)
    body_fat_pct = np.where(genders == 1, body_fat_male, body_fat_female)
    
    # Health metrics
    bp_systolic = np.random.normal(120, 15, n_samples).clip(90, 180)
    bp_diastolic = np.random.normal(80, 10, n_samples).clip(60, 120)
    resting_hr = np.random.normal(70, 12, n_samples).clip(50, 100)
    hours_sleep = np.random.normal(7.5, 1.2, n_samples).clip(4, 12)
    
    # Dietary preferences (binary)
    vegetarian = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    vegan = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
    gluten_free = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
    dairy_free = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    
    # Calculate BMR using Mifflin-St Jeor equation
    bmr = np.where(genders == 1,
                   10 * weights + 6.25 * heights - 5 * ages + 5,
                   10 * weights + 6.25 * heights - 5 * ages - 161)
    
    # Activity multipliers
    activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
    tdee = bmr * np.array([activity_multipliers[int(level)] for level in activity_levels])
    
    # Goal adjustments
    goal_adjustments = [-500, 0, 500]
    target_calories = tdee + np.array([goal_adjustments[int(goal)] for goal in goals])
    target_calories = np.maximum(target_calories, 1200)  # Minimum safe calories
    
    # Enhanced macro calculations based on multiple factors
    base_protein_ratio = np.where(goals == 2, 0.35,  # muscle gain
                                 np.where(goals == 0, 0.40,  # weight loss
                                         0.30))  # maintenance
    
    # Adjust protein based on fitness level and body composition
    protein_adjustment = fitness_levels * 0.02 + (body_fat_pct < 15).astype(int) * 0.03
    protein_ratio = np.clip(base_protein_ratio + protein_adjustment, 0.25, 0.45)
    
    # Fat ratio based on gender and goals
    base_fat_ratio = np.where(genders == 0, 0.28, 0.25)  # Slightly higher for females
    fat_adjustment = np.where(goals == 2, -0.05, 0)  # Lower fat for muscle gain
    fat_ratio = np.clip(base_fat_ratio + fat_adjustment, 0.15, 0.35)
    
    # Carb ratio fills the remainder
    carb_ratio = 1.0 - protein_ratio - fat_ratio
    
    # Convert to grams
    protein_g = (target_calories * protein_ratio) / 4
    carb_g = (target_calories * carb_ratio) / 4
    fat_g = (target_calories * fat_ratio) / 9
    
    # Meal timing preferences (enhanced)
    meals_per_day = np.random.choice([3, 4, 5, 6], n_samples, p=[0.2, 0.4, 0.3, 0.1])
    
    # Create comprehensive dataset
    data = {
        'weight': weights,
        'height': heights,
        'age': ages,
        'gender': genders,
        'activity_level': activity_levels,
        'goal': goals,
        'fitness_level': fitness_levels,
        'body_fat_pct': body_fat_pct,
        'bp_systolic': bp_systolic,
        'bp_diastolic': bp_diastolic,
        'resting_hr': resting_hr,
        'hours_sleep': hours_sleep,
        'vegetarian': vegetarian,
        'vegan': vegan,
        'gluten_free': gluten_free,
        'dairy_free': dairy_free,
        'meals_per_day': meals_per_day,
        'target_calories': target_calories,
        'protein_ratio': protein_ratio,
        'carb_ratio': carb_ratio,
        'fat_ratio': fat_ratio,
        'protein_g': protein_g,
        'carb_g': carb_g,
        'fat_g': fat_g
    }
    
    return pd.DataFrame(data)

def create_deep_learning_models():
    """Create and train deep learning models for meal planning"""
    print("Creating enhanced dataset...")
    df = create_enhanced_dataset()
    
    # Prepare features
    feature_columns = [
        'weight', 'height', 'age', 'gender', 'activity_level', 'goal',
        'fitness_level', 'body_fat_pct', 'bp_systolic', 'bp_diastolic',
        'resting_hr', 'hours_sleep', 'vegetarian', 'vegan',
        'gluten_free', 'dairy_free', 'meals_per_day'
    ]
    
    X = df[feature_columns].values
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Model 1: Calorie Prediction
    print("Training deep learning calorie prediction model...")
    y_calories = df['target_calories'].values
    
    X_train_cal, X_test_cal, y_train_cal, y_test_cal = train_test_split(
        X_scaled, y_calories, test_size=0.2, random_state=42
    )
    
    # Advanced neural network for calorie prediction
    calorie_model = keras.Sequential([
        layers.Dense(256, activation='relu', input_shape=(X_scaled.shape[1],)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.1),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='linear')
    ])
    
    # Create loss and metric objects
    mse_loss = MeanSquaredError()
    mse_metric = MSE()
    
    calorie_model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=mse_loss,
        metrics=[mse_metric]
    )
    
    # Train with callbacks
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=20, restore_best_weights=True
    )
    
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6
    )
    
    calorie_model.fit(
        X_train_cal, y_train_cal,
        validation_data=(X_test_cal, y_test_cal),
        epochs=200,
        batch_size=64,
        callbacks=[early_stopping, reduce_lr],
        verbose=0
    )
    
    # Model 2: Macro Distribution Prediction
    print("Training deep learning macro distribution model...")
    y_macros = df[['protein_ratio', 'carb_ratio', 'fat_ratio']].values
    
    X_train_macro, X_test_macro, y_train_macro, y_test_macro = train_test_split(
        X_scaled, y_macros, test_size=0.2, random_state=42
    )
    
    macro_model = keras.Sequential([
        layers.Dense(256, activation='relu', input_shape=(X_scaled.shape[1],)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.1),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax')  # Sum to 1 for ratios
    ])
    
    macro_model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=mse_loss,
        metrics=[mse_metric]
    )
    
    macro_model.fit(
        X_train_macro, y_train_macro,
        validation_data=(X_test_macro, y_test_macro),
        epochs=200,
        batch_size=64,
        callbacks=[early_stopping, reduce_lr],
        verbose=0
    )
    
    # Model 3: Meal Composition Prediction
    print("Training meal composition model...")
    
    # Generate meal data
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    meal_data = []
    
    for i in range(len(df)):
        for meal_type in meal_types:
            # Create meal-specific features
            meal_features = list(X_scaled[i]) + [meal_types.index(meal_type)]
            
            # Generate realistic meal composition based on meal type and user preferences
            if meal_type == 'breakfast':
                composition = [0.25, 0.35, 0.15, 0.05, 0.15, 0.05]  # protein, carbs, fats, vegetables, fruits, dairy
            elif meal_type == 'lunch':
                composition = [0.35, 0.30, 0.15, 0.20, 0.00, 0.00]
            elif meal_type == 'dinner':
                composition = [0.40, 0.25, 0.15, 0.20, 0.00, 0.00]
            else:  # snack
                composition = [0.30, 0.30, 0.20, 0.00, 0.20, 0.00]
            
            # Add some realistic variation
            noise = np.random.normal(0, 0.05, 6)
            composition = np.array(composition) + noise
            composition = np.clip(composition, 0, 1)
            composition = composition / composition.sum()  # Normalize
            
            meal_data.append(meal_features + list(composition))
    
    meal_df = pd.DataFrame(meal_data)
    X_meal = meal_df.iloc[:, :-6].values
    y_meal = meal_df.iloc[:, -6:].values
    
    X_train_meal, X_test_meal, y_train_meal, y_test_meal = train_test_split(
        X_meal, y_meal, test_size=0.2, random_state=42
    )
    
    meal_composition_model = keras.Sequential([
        layers.Dense(256, activation='relu', input_shape=(X_meal.shape[1],)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.1),
        layers.Dense(32, activation='relu'),
        layers.Dense(6, activation='softmax')  # 6 food groups
    ])
    
    meal_composition_model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=mse_loss,
        metrics=[mse_metric]
    )
    
    meal_composition_model.fit(
        X_train_meal, y_train_meal,
        validation_data=(X_test_meal, y_test_meal),
        epochs=150,
        batch_size=64,
        callbacks=[early_stopping, reduce_lr],
        verbose=0
    )
    
    # Save models
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    print("Saving enhanced models...")
    
    # Save TensorFlow models
    calorie_model.save(os.path.join(models_dir, 'deep_calorie_model.h5'))
    macro_model.save(os.path.join(models_dir, 'deep_macro_model.h5'))
    meal_composition_model.save(os.path.join(models_dir, 'deep_meal_composition_model.h5'))
    
    # Save scaler
    joblib.dump(scaler, os.path.join(models_dir, 'deep_scaler.joblib'))
    
    # Evaluate models
    print("\nModel Performance:")
    
    # Calorie model evaluation
    cal_pred = calorie_model.predict(X_test_cal, verbose=0)
    cal_mse = mean_squared_error(y_test_cal, cal_pred)
    cal_r2 = r2_score(y_test_cal, cal_pred)
    print(f"Calorie Model - MSE: {cal_mse:.2f}, R²: {cal_r2:.4f}")
    
    # Macro model evaluation
    macro_pred = macro_model.predict(X_test_macro, verbose=0)
    macro_mse = mean_squared_error(y_test_macro, macro_pred)
    macro_r2 = r2_score(y_test_macro, macro_pred)
    print(f"Macro Model - MSE: {macro_mse:.6f}, R²: {macro_r2:.4f}")
    
    # Meal composition model evaluation
    meal_pred = meal_composition_model.predict(X_test_meal, verbose=0)
    meal_mse = mean_squared_error(y_test_meal, meal_pred)
    meal_r2 = r2_score(y_test_meal, meal_pred)
    print(f"Meal Composition Model - MSE: {meal_mse:.6f}, R²: {meal_r2:.4f}")
    
    print("\nEnhanced deep learning models saved successfully!")

if __name__ == '__main__':
    create_deep_learning_models() 