from typing import List, Dict, Any
import random

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
    # Base exercise pool
    exercises = {
        'push': [
            'Bench Press', 'Overhead Press', 'Incline Bench Press',
            'Dips', 'Push-ups', 'Lateral Raises', 'Tricep Extensions'
        ],
        'pull': [
            'Pull-ups', 'Bent Over Rows', 'Lat Pulldowns',
            'Face Pulls', 'Bicep Curls', 'Hammer Curls'
        ],
        'legs': [
            'Squats', 'Deadlifts', 'Romanian Deadlifts',
            'Leg Press', 'Lunges', 'Calf Raises'
        ],
        'core': [
            'Planks', 'Ab Wheel Rollouts', 'Russian Twists',
            'Hanging Leg Raises', 'Cable Woodchoppers'
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
            'exercises_per_group': 2
        },
        'hypertrophy': {
            'sets': 4,
            'reps': '8-12',
            'rest': 90,
            'exercises_per_group': 3
        },
        'endurance': {
            'sets': 3,
            'reps': '15-20',
            'rest': 60,
            'exercises_per_group': 4
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
        base_structure['exercises_per_group'] = 1
    
    return base_structure

def generate_workout(muscle_groups: List[str], exercise_pool: Dict[str, List[str]], 
                    structure: Dict[str, Any], experience_years: int) -> Dict[str, Any]:
    """Generate a single workout based on parameters."""
    exercises = []
    total_duration = 0
    
    for group in muscle_groups:
        available_exercises = exercise_pool.get(group, [])
        num_exercises = min(structure['exercises_per_group'], len(available_exercises))
        
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