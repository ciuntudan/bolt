from typing import List, Dict, Any
import random
import joblib
import os

# --- ML Model Loading ---
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

_scaler = joblib.load(os.path.join(MODEL_DIR, 'workout_scaler.joblib'))
_encoders = joblib.load(os.path.join(MODEL_DIR, 'workout_encoders.joblib'))
_split_le = joblib.load(os.path.join(MODEL_DIR, 'split_label_encoder.joblib'))
_split_clf = joblib.load(os.path.join(MODEL_DIR, 'split_classifier.joblib'))
_sets_reg = joblib.load(os.path.join(MODEL_DIR, 'sets_regressor.joblib'))
_reps_reg = joblib.load(os.path.join(MODEL_DIR, 'reps_regressor.joblib'))
_rest_reg = joblib.load(os.path.join(MODEL_DIR, 'rest_regressor.joblib'))

def determine_split_type(days_per_week: int, goal: str) -> str:
    """Determine the most appropriate training split based on frequency and goal."""
    if days_per_week <= 3:
        return 'full_body'
    elif days_per_week == 4:
        return 'upper_lower' if goal in ['strength', 'powerlifting'] else 'push_pull_legs'
    else:
        return 'body_part' if goal == 'hypertrophy' else 'push_pull_legs'

def get_exercise_pool(equipment: List[str], injuries: List[str], 
                     excluded_exercises: List[str]) -> Dict[str, List[str]]:
    """Get available exercises based on equipment and injuries."""
    # Expanded exercise pool
    exercises = {
        'push': [
            'Bench Press', 'Overhead Press', 'Incline Bench Press', 'Decline Bench Press',
            'Dips', 'Push-ups', 'Lateral Raises', 'Tricep Extensions', 'Arnold Press',
            'Close-Grip Bench Press', 'Machine Chest Press', 'Cable Flyes', 'Front Raises',
            'Diamond Push-ups', 'Pec Deck', 'Seated Dumbbell Press', 'Landmine Press',
            'Chest Dips', 'Push-up Variations', 'Plate Press', 'Svend Press'
        ],
        'pull': [
            'Pull-ups', 'Chin-ups', 'Bent Over Rows', 'Lat Pulldowns', 'Seated Cable Row',
            'Face Pulls', 'Bicep Curls', 'Hammer Curls', 'Reverse Flyes', 'T-Bar Row',
            'Inverted Rows', 'Single-Arm Dumbbell Row', 'Preacher Curl', 'EZ Bar Curl',
            'Cable Curl', 'Shrugs', 'Rear Delt Fly', 'Trap Bar Row', 'Wide-Grip Pulldown',
            'Concentration Curl', 'Zottman Curl'
        ],
        'legs': [
            'Squats', 'Front Squats', 'Deadlifts', 'Romanian Deadlifts', 'Leg Press',
            'Lunges', 'Calf Raises', 'Leg Extensions', 'Leg Curls', 'Bulgarian Split Squat',
            'Glute Bridge', 'Hip Thrust', 'Step-Ups', 'Sumo Deadlift', 'Hack Squat',
            'Goblet Squat', 'Seated Calf Raise', 'Standing Calf Raise', 'Good Mornings',
            'Box Squat'
        ],
        'core': [
            'Planks', 'Ab Wheel Rollouts', 'Russian Twists', 'Hanging Leg Raises',
            'Cable Woodchoppers', 'Sit-ups', 'Crunches', 'Mountain Climbers',
            'V-Ups', 'Toe Touches', 'Bicycle Crunches', 'Flutter Kicks',
            'Side Plank', 'Reverse Crunch', 'Cable Crunch', 'Leg Raises'
        ]
    }
    
    # Filter based on equipment
    if 'barbell' not in equipment:
        exercises = {k: [e for e in v if 'Press' not in e and 'Deadlift' not in e]
                    for k, v in exercises.items()}
    
    # Filter based on injuries
    if 'shoulder' in injuries:
        exercises['push'] = [e for e in exercises['push'] 
                           if 'Overhead' not in e and 'Lateral' not in e]
    if 'knee' in injuries:
        exercises['legs'] = [e for e in exercises['legs'] 
                           if 'Squat' not in e and 'Lunge' not in e]
    if 'back' in injuries:
        exercises = {k: [e for e in v if 'Deadlift' not in e] 
                    for k, v in exercises.items()}
    
    # Remove excluded exercises
    exercises = {k: [e for e in v if e not in excluded_exercises]
                for k, v in exercises.items()}
    
    return exercises

def generate_workout_structure(goal: str, training_style: str, 
                             duration: int) -> Dict[str, Any]:
    """Generate workout structure based on goal and training style."""
    structures = {
        'strength': {
            'sets': 5,
            'reps': '3-5',
            'rest': 180,
            'exercises_per_group': 4
        },
        'hypertrophy': {
            'sets': 4,
            'reps': '8-12',
            'rest': 90,
            'exercises_per_group': 5
        },
        'endurance': {
            'sets': 3,
            'reps': '15-20',
            'rest': 60,
            'exercises_per_group': 6
        }
    }
    
    base_structure = structures.get(goal, structures['hypertrophy'])
    
    # Modify structure based on training style
    if training_style == 'supersets':
        base_structure['rest'] *= 0.7
        base_structure['exercises_per_group'] += 1
    elif training_style == 'circuit':
        base_structure['rest'] *= 0.5
        base_structure['exercises_per_group'] += 2
    elif training_style == 'german_volume':
        base_structure['sets'] = 10
        base_structure['reps'] = '10'
        base_structure['exercises_per_group'] = 2
    
    return base_structure

def generate_workout(muscle_groups: List[str], exercise_pool: Dict[str, List[str]], 
                    structure: Dict[str, Any], experience_years: int) -> Dict[str, Any]:
    """Generate a single workout based on parameters."""
    exercises = []
    total_duration = 0
    
    for group in muscle_groups:
        available_exercises = exercise_pool.get(group, [])
        # For core, use 3-4 exercises; for others, use structure['exercises_per_group'] (default 4-6)
        if group == 'core':
            num_exercises = min(max(3, structure.get('exercises_per_group', 4)), len(available_exercises))
        else:
            num_exercises = min(max(4, structure.get('exercises_per_group', 4)), len(available_exercises))
        
        selected_exercises = random.sample(available_exercises, num_exercises)
        
        for exercise in selected_exercises:
            exercise_data = {
                'name': exercise,
                'sets': structure['sets'],
                'reps': structure['reps'],
                'notes': ''
            }
            
            # Adjust based on experience
            if experience_years > 2:
                exercise_data['sets'] += 1
            if experience_years > 5:
                exercise_data['notes'] = 'Consider adding intensity techniques'
            
            exercises.append(exercise_data)
            total_duration += (structure['sets'] * 
                             (structure.get('rest', 60) + 45))  
    
    return {
        'exercises': exercises,
        'duration': total_duration // 60 
    }

def generate_workouts(days_per_week: int, goal: str, training_style: str,
                     equipment: List[str], intensity_multiplier: float = 1.0,
                     preferred_duration: int = 60, injuries: List[str] = None,
                     experience_years: int = 0, preferred_exercises: List[str] = None,
                     excluded_exercises: List[str] = None) -> List[Dict[str, Any]]:
    """Generate a complete set of workouts for the week."""
    injuries = injuries or []
    preferred_exercises = preferred_exercises or []
    excluded_exercises = excluded_exercises or []
    
    # Determine split type and get exercise pool
    split_type = determine_split_type(days_per_week, goal)
    exercise_pool = get_exercise_pool(equipment, injuries, excluded_exercises)
    
    # Get workout structure
    structure = generate_workout_structure(goal, training_style, preferred_duration)
    
    # Adjust intensity
    structure['sets'] = int(structure['sets'] * intensity_multiplier)
    
    # Define workout splits
    splits = {
        'full_body': [['push', 'pull', 'legs']] * days_per_week,
        'upper_lower': [['push', 'pull'], ['legs', 'core']] * (days_per_week // 2),
        'push_pull_legs': [['push'], ['pull'], ['legs']] * (days_per_week // 3),
        'body_part': [['push'], ['pull'], ['legs'], ['push'], ['pull'], ['legs']][:days_per_week]
    }
    
    # Generate workouts
    workouts = []
    for day_num, muscle_groups in enumerate(splits[split_type], 1):
        workout = generate_workout(
            muscle_groups, exercise_pool, structure, experience_years
        )
        
        workout.update({
            'name': f"Day {day_num}: {' + '.join(muscle_groups).title()}",
            'description': f"Focus on {', '.join(muscle_groups)} exercises"
        })
        
        workouts.append(workout)
    
    return workouts

def generate_cardio_workout(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a cardio workout based on preferences."""
    cardio_type = random.choice(preferences.get('type', ['running']))
    duration = preferences.get('duration', 20)
    
    # Define different cardio formats
    formats = {
        'steady_state': {
            'description': f"{duration} minutes steady state {cardio_type}",
            'intensity': 'moderate',
            'notes': 'Maintain a consistent pace throughout'
        },
        'intervals': {
            'description': f"{duration} minutes {cardio_type} intervals",
            'intensity': 'high',
            'notes': '1 min high intensity, 1 min recovery'
        },
        'pyramid': {
            'description': f"{duration} minutes {cardio_type} pyramid",
            'intensity': 'variable',
            'notes': 'Gradually increase then decrease intensity'
        }
    }
    
    # Select random format
    format_type = random.choice(list(formats.keys()))
    workout = formats[format_type]
    
    return {
        'name': f"{format_type.replace('_', ' ').title()} {cardio_type.title()}",
        'exercise': cardio_type,
        'duration': duration,
        **workout
    }

def generate_cardio_days(frequency: int, total_days: int, 
                        preferences: Dict[str, Any]) -> List[int]:
    """Generate optimal days for cardio sessions."""
    if frequency >= total_days:
        return list(range(1, total_days + 1))
    
    # Space out cardio days evenly
    step = total_days // frequency
    cardio_days = list(range(2, total_days + 1, step))[:frequency]
    
    return cardio_days

def generate_week_description(goal: str, is_deload: bool) -> str:
    """Generate a description for the training week based on the goal."""
    if is_deload:
        return "Deload week: Lower intensity and volume to promote recovery."
    
    descriptions = {
        'strength': "Focus on compound movements with heavy weights and low reps.",
        'hypertrophy': "Moderate weights with higher volume to stimulate muscle growth.",
        'endurance': "Higher reps with shorter rest periods to build muscular endurance.",
        'weight_loss': "Circuit-style training with a mix of resistance and cardio.",
        'powerlifting': "Heavy compound lifts focusing on the big three: squat, bench, deadlift.",
        'crossfit': "High-intensity functional movements combining strength and conditioning.",
        'athletic': "Explosive movements and sport-specific training for performance.",
        'rehabilitation': "Controlled movements focusing on form and gradual progression."
    }
    return descriptions.get(goal, "Custom training week based on your goals.")

def ml_predict_split_and_structure(user_profile: dict) -> dict:
    """
    Predict split type and structure (sets, reps, rest) using ML models.
    user_profile: dict with keys: age, gender, experience, goal, days_per_week, equipment, injuries
    """
    X = {
        'age': user_profile['age'],
        'gender': user_profile['gender'],
        'experience': user_profile['experience'],
        'goal': user_profile['goal'],
        'days_per_week': user_profile['days_per_week'],
        'equipment': user_profile['equipment'],
        'injuries': user_profile['injuries'],
    }
    X_enc = X.copy()
    for col in ['gender', 'goal', 'equipment', 'injuries']:
        le = _encoders[col]
        X_enc[col] = le.transform([X[col]])[0]
    X_df = [[X_enc['age'], X_enc['gender'], X_enc['experience'], X_enc['goal'], X_enc['days_per_week'], X_enc['equipment'], X_enc['injuries']]]
    X_scaled = _scaler.transform(X_df)
    split_pred = _split_le.inverse_transform(_split_clf.predict(X_scaled))[0]
    sets_pred = int(round(_sets_reg.predict(X_scaled)[0]))
    reps_pred = int(round(_reps_reg.predict(X_scaled)[0]))
    rest_pred = int(round(_rest_reg.predict(X_scaled)[0]))
    return {
        'split_type': split_pred,
        'sets': sets_pred,
        'reps': reps_pred,
        'rest': rest_pred
    }

def generate_workouts_ml(user_profile: dict, intensity_multiplier: float = 1.0, preferred_duration: int = 60, preferred_exercises: list = None, excluded_exercises: list = None) -> list:
    """
    Generate workouts using ML-predicted split and structure.
    user_profile: dict with keys: age, gender, experience, goal, days_per_week, equipment, injuries
    """
    preferred_exercises = preferred_exercises or []
    excluded_exercises = excluded_exercises or []
    ml_pred = ml_predict_split_and_structure(user_profile)
    split_type = ml_pred['split_type']
    # Use more exercises per group for ML as well
    structure = {
        'sets': int(ml_pred['sets'] * intensity_multiplier),
        'reps': ml_pred['reps'],
        'rest': ml_pred['rest'],
        'exercises_per_group': 5  # default to 5 for more volume
    }
    # Use the rest of the original logic, but with ML-predicted split_type and structure
    days_per_week = user_profile['days_per_week']
    equipment = [user_profile['equipment']]
    injuries = [user_profile['injuries']] if user_profile['injuries'] != 'none' else []
    exercise_pool = get_exercise_pool(equipment, injuries, excluded_exercises)
    splits = {
        'full_body': [['push', 'pull', 'legs']] * days_per_week,
        'upper_lower': [['push', 'pull'], ['legs', 'core']] * (days_per_week // 2),
        'push_pull_legs': [['push'], ['pull'], ['legs']] * (days_per_week // 3),
        'body_part': [['push'], ['pull'], ['legs'], ['push'], ['pull'], ['legs']][:days_per_week]
    }
    workouts = []
    for day_num, muscle_groups in enumerate(splits[split_type], 1):
        workout = generate_workout(
            muscle_groups, exercise_pool, structure, user_profile['experience']
        )
        workout.update({
            'name': f"Day {day_num}: {' + '.join(muscle_groups).title()}",
            'description': f"Focus on {', '.join(muscle_groups)} exercises"
        })
        workouts.append(workout)
    return workouts 