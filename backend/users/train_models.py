import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def create_synthetic_data(n_samples=10000):
    """Create synthetic data for training the meal plan models with realistic distributions"""
    np.random.seed(42)
    
    # Generate user 
    weights = np.random.normal(75, 15, n_samples)  
    heights = np.random.normal(170, 10, n_samples) 
    ages = np.random.randint(18, 70, n_samples)  
    body_fat_pcts = np.random.normal(20, 5, n_samples)  
    blood_pressure_systolic = np.random.normal(120, 10, n_samples)
    blood_pressure_diastolic = np.random.normal(80, 8, n_samples)
    resting_heart_rates = np.random.normal(70, 8, n_samples)
    hours_sleep = np.random.normal(7, 1, n_samples)
    
    # Categorical features
    genders = np.random.choice(['male', 'female'], n_samples)
    activity_levels = np.random.choice(
        ['sedentary', 'light', 'moderate', 'active', 'very_active'],
        n_samples,
        p=[0.2, 0.3, 0.3, 0.15, 0.05]
    )
    goals = np.random.choice(
        ['weight_loss', 'maintenance', 'muscle_gain'],
        n_samples,
        p=[0.4, 0.3, 0.3]
    )
    fitness_levels = np.random.choice(
        ['beginner', 'intermediate', 'advanced'],
        n_samples,
        p=[0.3, 0.5, 0.2]
    )
    
 
    is_vegetarian = np.random.choice([True, False], n_samples, p=[0.1, 0.9])
    is_vegan = np.random.choice([True, False], n_samples, p=[0.05, 0.95])
    is_gluten_free = np.random.choice([True, False], n_samples, p=[0.08, 0.92])
    is_dairy_free = np.random.choice([True, False], n_samples, p=[0.12, 0.88])
    
    # Meal types
    meal_types = np.random.choice(['breakfast', 'lunch', 'dinner', 'snack'], n_samples)
    
    # Create feature matrix
    X = np.column_stack([
        weights, heights, ages, body_fat_pcts,
        blood_pressure_systolic, blood_pressure_diastolic,
        resting_heart_rates, hours_sleep,
        (genders == 'male').astype(int),  
        np.eye(5)[(np.array([['sedentary', 'light', 'moderate', 'active', 'very_active'].index(x) for x in activity_levels]))], 
        np.eye(3)[(np.array([['weight_loss', 'maintenance', 'muscle_gain'].index(x) for x in goals]))], 
        np.eye(3)[(np.array([['beginner', 'intermediate', 'advanced'].index(x) for x in fitness_levels]))],  
        is_vegetarian.astype(int), is_vegan.astype(int),
        is_gluten_free.astype(int), is_dairy_free.astype(int),
        np.eye(4)[(np.array([['breakfast', 'lunch', 'dinner', 'snack'].index(x) for x in meal_types]))] 
    ])
    
   
    y_calories = generate_calorie_targets(X)
    y_macros = generate_macro_ratios(X)
    y_meal_timing = generate_meal_timing(X)
    y_meal_composition = generate_meal_composition(X)
    
    return {
        'X': X,
        'y_calories': y_calories,
        'y_macros': y_macros,
        'y_meal_timing': y_meal_timing,
        'y_meal_composition': y_meal_composition
    }

def train_models():
    """Train the ML models for meal plan generation"""
    print("Generating synthetic training data...")
    data = create_synthetic_data(n_samples=10000)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data['X'])
    
    # Train calorie prediction model
    print("Training calorie prediction model...")
    calorie_model = RandomForestRegressor(n_estimators=100, random_state=42)
    calorie_model.fit(X_scaled, data['y_calories'])
    
    # Train macro ratio prediction model 
    print("Training macro ratio prediction model...")
    X_macro = np.hstack([X_scaled, data['y_calories'].reshape(-1, 1)]) 
    macro_model = RandomForestRegressor(n_estimators=100, random_state=42)
    macro_model.fit(X_macro, data['y_macros'])
    
    # Train meal timing model
    print("Training meal timing model...")
    meal_timing_model = RandomForestRegressor(n_estimators=100, random_state=42)
    meal_timing_model.fit(X_scaled, data['y_meal_timing'])
    
    # Train meal composition model
    print("Training meal composition model...")
    meal_composition_model = RandomForestRegressor(n_estimators=100, random_state=42)
    meal_composition_model.fit(X_scaled, data['y_meal_composition'])
    
    # Save models and scaler
    print("Saving models and scaler...")
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(scaler, os.path.join(model_dir, 'feature_scaler.joblib'))
    joblib.dump(calorie_model, os.path.join(model_dir, 'calorie_model.joblib'))
    joblib.dump(macro_model, os.path.join(model_dir, 'macro_model.joblib'))
    joblib.dump(meal_timing_model, os.path.join(model_dir, 'meal_timing_model.joblib'))
    joblib.dump(meal_composition_model, os.path.join(model_dir, 'meal_composition_model.joblib'))
    
    print("Successfully trained and saved all models")

def generate_calorie_targets(X):
    """Generate realistic calorie targets based on user features"""
    n_samples = X.shape[0]
    base_calories = np.zeros(n_samples)
    
    for i in range(n_samples):
        # Extract features
        weight = X[i, 0]
        height = X[i, 1]
        age = X[i, 2]
        is_male = X[i, 8]  
        activity_level_idx = np.argmax(X[i, 9:14])  
        goal_idx = np.argmax(X[i, 14:17])  
        
        # Calculate BMR using Mifflin-St Jeor Equation
        if is_male:
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Apply activity multiplier
        activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]  
        tdee = bmr * activity_multipliers[activity_level_idx]
        
        # Apply goal adjustment
        goal_adjustments = [-500, 0, 300]  
        base_calories[i] = tdee + goal_adjustments[goal_idx]
    
    return base_calories

def generate_macro_ratios(X):
    """Generate realistic macro ratios based on user features"""
    n_samples = X.shape[0]
    macro_ratios = np.zeros((n_samples, 3))  
    
    for i in range(n_samples):
        # Extract goal
        goal_idx = np.argmax(X[i, 14:17])  
        
        # Base ratios for each goal
        if goal_idx == 0:  
            protein_pct = np.random.normal(0.35, 0.05)  
            fat_pct = np.random.normal(0.35, 0.05)
            carb_pct = 1 - protein_pct - fat_pct
        elif goal_idx == 2:  
            protein_pct = np.random.normal(0.30, 0.05)
            carb_pct = np.random.normal(0.45, 0.05)
            fat_pct = 1 - protein_pct - carb_pct
        else:  
            protein_pct = np.random.normal(0.25, 0.05)
            carb_pct = np.random.normal(0.45, 0.05)
            fat_pct = 1 - protein_pct - carb_pct
        
        # Clip and normalize
        ratios = np.array([protein_pct, carb_pct, fat_pct])
        ratios = np.clip(ratios, 0.15, 0.5)
        ratios = ratios / ratios.sum()
        
        macro_ratios[i] = ratios
    
    return macro_ratios

def generate_meal_timing(X):
    """Generate realistic meal timing ratios based on user features"""
    n_samples = X.shape[0]
    meal_ratios = np.zeros((n_samples, 6))  
    
    for i in range(n_samples):
        # Extract meal type
        meal_type_idx = np.argmax(X[i, -4:]) 
        goal_idx = np.argmax(X[i, 14:17])  
        
        if meal_type_idx == 0: 
            ratios = np.array([0.3, 0.3, 0.2, 0, 0.1, 0.1]) 
        elif meal_type_idx == 1: 
            ratios = np.array([0.3, 0.3, 0.15, 0.25, 0, 0])  
        elif meal_type_idx == 2:  
            ratios = np.array([0.35, 0.25, 0.15, 0.25, 0, 0]) 
        else:  
            ratios = np.array([0.3, 0.3, 0.2, 0, 0.2, 0])  
        
        # Adjust based on goal
        if goal_idx == 0:  
            ratios[0] *= 1.2  
            ratios[3] *= 1.3  
        elif goal_idx == 2:  
            ratios[0] *= 1.3  
            ratios[1] *= 1.2  
        
        # Add random variation
        ratios += np.random.normal(0, 0.05, size=6)
        
        # Clip and normalize
        ratios = np.clip(ratios, 0.05, 0.5)
        ratios = ratios / ratios.sum()
        
        meal_ratios[i] = ratios
    
    return meal_ratios

def generate_meal_composition(X):
    """Generate synthetic meal composition ratios for each meal (proteins, carbs, fats, vegetables, fruits, dairy)"""
    n_samples = X.shape[0]
    composition = np.zeros((n_samples, 6))
    for i in range(n_samples):
        meal_type_idx = np.argmax(X[i, -4:])
        # Default templates (should match get_default_meal_composition in generator)
        if meal_type_idx == 0:  # breakfast
            ratios = np.array([0.3, 0.3, 0.2, 0, 0.1, 0.1])
        elif meal_type_idx == 1:  # lunch
            ratios = np.array([0.3, 0.3, 0.15, 0.25, 0, 0])
        elif meal_type_idx == 2:  # dinner
            ratios = np.array([0.35, 0.25, 0.15, 0.25, 0, 0])
        else:  # snack
            ratios = np.array([0.3, 0.3, 0.2, 0, 0.2, 0])
        # Add some noise
        ratios += np.random.normal(0, 0.02, 6)
        ratios = np.clip(ratios, 0, 1)
        ratios = ratios / ratios.sum()
        composition[i] = ratios
    return composition

if __name__ == '__main__':
    train_models() 