from typing import List, Dict, Any
import random
from datetime import datetime
from ..models import TrainingPlan, TrainingWeek, TrainingDay, Exercise

class TrainingPlanGenerator:
    def __init__(self):
        # Comprehensive exercise database organized by muscle groups and equipment
        self.exercise_database = {
            'chest': {
                'barbell': [
                    {'name': 'Barbell Bench Press', 'sets': 4, 'reps': '6-8', 'notes': 'Keep feet flat on floor'},
                    {'name': 'Incline Barbell Press', 'sets': 3, 'reps': '8-10', 'notes': '30-45 degree incline'},
                    {'name': 'Decline Barbell Press', 'sets': 3, 'reps': '8-12', 'notes': 'Focus on lower chest'},
                ],
                'dumbbell': [
                    {'name': 'Dumbbell Bench Press', 'sets': 4, 'reps': '8-12', 'notes': 'Full range of motion'},
                    {'name': 'Incline Dumbbell Press', 'sets': 3, 'reps': '8-12', 'notes': 'Squeeze at the top'},
                    {'name': 'Dumbbell Flyes', 'sets': 3, 'reps': '10-15', 'notes': 'Control the stretch'},
                    {'name': 'Chest Flyes', 'sets': 3, 'reps': '12-15', 'notes': 'Feel the stretch'},
                ],
                'cables': [
                    {'name': 'Cable Flyes', 'sets': 3, 'reps': '12-15', 'notes': 'Keep tension throughout'},
                    {'name': 'Cable Crossovers', 'sets': 3, 'reps': '12-15', 'notes': 'Squeeze at midline'},
                    {'name': 'Cable Chest Press', 'sets': 3, 'reps': '10-12', 'notes': 'Stable core'},
                ],
                'machines': [
                    {'name': 'Chest Press Machine', 'sets': 3, 'reps': '10-12', 'notes': 'Adjust seat height'},
                    {'name': 'Pec Deck', 'sets': 3, 'reps': '12-15', 'notes': 'Focus on squeeze'},
                ],
                'bodyweight': [
                    {'name': 'Push-Ups', 'sets': 3, 'reps': '12-20', 'notes': 'Full range of motion'},
                    {'name': 'Incline Push-Ups', 'sets': 3, 'reps': '10-15', 'notes': 'Hands elevated'},
                    {'name': 'Decline Push-Ups', 'sets': 3, 'reps': '8-12', 'notes': 'Feet elevated'},
                    {'name': 'Diamond Push-Ups', 'sets': 3, 'reps': '8-12', 'notes': 'Focus on triceps'},
                    {'name': 'Dips', 'sets': 3, 'reps': '8-15', 'notes': 'Control the descent'},
                ]
            },
            'back': {
                'barbell': [
                    {'name': 'Deadlift', 'sets': 4, 'reps': '5-6', 'notes': 'Maintain neutral spine'},
                    {'name': 'Bent-Over Barbell Rows', 'sets': 4, 'reps': '8-10', 'notes': 'Squeeze shoulder blades'},
                    {'name': 'Barbell Rows', 'sets': 3, 'reps': '8-12', 'notes': 'Pull to lower chest'},
                ],
                'dumbbell': [
                    {'name': 'Dumbbell Rows', 'sets': 3, 'reps': '8-12', 'notes': 'One arm at a time'},
                    {'name': 'Dumbbell Deadlifts', 'sets': 3, 'reps': '8-12', 'notes': 'Keep back straight'},
                    {'name': 'Reverse Flyes', 'sets': 3, 'reps': '12-15', 'notes': 'Focus on rear delts'},
                ],
                'cables': [
                    {'name': 'Cable Rows', 'sets': 4, 'reps': '10-12', 'notes': 'Pull to lower chest'},
                    {'name': 'Lat Pulldowns', 'sets': 4, 'reps': '10-12', 'notes': 'Wide grip'},
                    {'name': 'Close-Grip Pulldowns', 'sets': 3, 'reps': '10-12', 'notes': 'Focus on lats'},
                    {'name': 'Face Pulls', 'sets': 3, 'reps': '15-20', 'notes': 'Target rear delts'},
                ],
                'bodyweight': [
                    {'name': 'Pull-Ups', 'sets': 3, 'reps': '5-12', 'notes': 'Full hang at bottom'},
                    {'name': 'Chin-Ups', 'sets': 3, 'reps': '6-12', 'notes': 'Underhand grip'},
                    {'name': 'Inverted Rows', 'sets': 3, 'reps': '8-15', 'notes': 'Body parallel to floor'},
                ]
            },
            'legs': {
                'barbell': [
                    {'name': 'Back Squats', 'sets': 4, 'reps': '6-8', 'notes': 'Break parallel'},
                    {'name': 'Front Squats', 'sets': 3, 'reps': '8-10', 'notes': 'Keep chest up'},
                    {'name': 'Romanian Deadlifts', 'sets': 3, 'reps': '8-12', 'notes': 'Feel hamstring stretch'},
                    {'name': 'Stiff Leg Deadlifts', 'sets': 3, 'reps': '10-12', 'notes': 'Keep legs straight'},
                ],
                'dumbbell': [
                    {'name': 'Dumbbell Squats', 'sets': 3, 'reps': '10-15', 'notes': 'Hold dumbbells at sides'},
                    {'name': 'Dumbbell Lunges', 'sets': 3, 'reps': '10-12 each leg', 'notes': 'Step forward'},
                    {'name': 'Bulgarian Split Squats', 'sets': 3, 'reps': '8-12 each leg', 'notes': 'Rear foot elevated'},
                    {'name': 'Dumbbell RDLs', 'sets': 3, 'reps': '10-12', 'notes': 'Feel hamstring stretch'},
                ],
                'machines': [
                    {'name': 'Leg Press', 'sets': 4, 'reps': '12-15', 'notes': 'Full range of motion'},
                    {'name': 'Leg Extensions', 'sets': 3, 'reps': '12-15', 'notes': 'Squeeze at top'},
                    {'name': 'Leg Curls', 'sets': 3, 'reps': '12-15', 'notes': 'Control the negative'},
                    {'name': 'Calf Raises', 'sets': 4, 'reps': '15-20', 'notes': 'Full stretch at bottom'},
                ],
                'bodyweight': [
                    {'name': 'Bodyweight Squats', 'sets': 3, 'reps': '15-25', 'notes': 'Full depth'},
                    {'name': 'Jump Squats', 'sets': 3, 'reps': '10-15', 'notes': 'Explosive movement'},
                    {'name': 'Lunges', 'sets': 3, 'reps': '12-15 each leg', 'notes': 'Alternate legs'},
                    {'name': 'Single Leg Squats', 'sets': 3, 'reps': '5-10 each leg', 'notes': 'Pistol squats'},
                ]
            },
            'shoulders': {
                'barbell': [
                    {'name': 'Military Press', 'sets': 4, 'reps': '6-8', 'notes': 'Full lockout overhead'},
                    {'name': 'Behind Neck Press', 'sets': 3, 'reps': '8-10', 'notes': 'If mobile enough'},
                ],
                'dumbbell': [
                    {'name': 'Dumbbell Shoulder Press', 'sets': 4, 'reps': '8-12', 'notes': 'Press straight up'},
                    {'name': 'Lateral Raises', 'sets': 3, 'reps': '12-15', 'notes': 'Control the movement'},
                    {'name': 'Front Raises', 'sets': 3, 'reps': '12-15', 'notes': 'One arm at a time'},
                    {'name': 'Rear Delt Flyes', 'sets': 3, 'reps': '15-20', 'notes': 'Bent over position'},
                    {'name': 'Arnold Press', 'sets': 3, 'reps': '10-12', 'notes': 'Rotate palms'},
                ],
                'cables': [
                    {'name': 'Cable Lateral Raises', 'sets': 3, 'reps': '12-15', 'notes': 'Constant tension'},
                    {'name': 'Cable Rear Delt Flyes', 'sets': 3, 'reps': '15-20', 'notes': 'Cross-body movement'},
                    {'name': 'Cable Front Raises', 'sets': 3, 'reps': '12-15', 'notes': 'Keep core tight'},
                ],
                'bodyweight': [
                    {'name': 'Pike Push-Ups', 'sets': 3, 'reps': '8-15', 'notes': 'Feet elevated'},
                    {'name': 'Handstand Push-Ups', 'sets': 3, 'reps': '3-8', 'notes': 'Against wall'},
                ]
            },
            'arms': {
                'barbell': [
                    {'name': 'Barbell Curls', 'sets': 3, 'reps': '8-12', 'notes': 'No swinging'},
                    {'name': 'Close-Grip Bench Press', 'sets': 3, 'reps': '8-12', 'notes': 'Elbows tucked'},
                    {'name': 'EZ Bar Curls', 'sets': 3, 'reps': '10-12', 'notes': 'Easier on wrists'},
                ],
                'dumbbell': [
                    {'name': 'Dumbbell Curls', 'sets': 3, 'reps': '10-12', 'notes': 'Alternate arms'},
                    {'name': 'Hammer Curls', 'sets': 3, 'reps': '10-12', 'notes': 'Neutral grip'},
                    {'name': 'Overhead Tricep Extension', 'sets': 3, 'reps': '10-12', 'notes': 'Keep elbows in'},
                    {'name': 'Tricep Kickbacks', 'sets': 3, 'reps': '12-15', 'notes': 'Squeeze at extension'},
                ],
                'cables': [
                    {'name': 'Cable Curls', 'sets': 3, 'reps': '12-15', 'notes': 'Constant tension'},
                    {'name': 'Tricep Pushdowns', 'sets': 3, 'reps': '12-15', 'notes': 'Keep elbows at sides'},
                    {'name': 'Overhead Cable Extension', 'sets': 3, 'reps': '12-15', 'notes': 'Stretch triceps'},
                ],
                'bodyweight': [
                    {'name': 'Tricep Dips', 'sets': 3, 'reps': '8-15', 'notes': 'On bench or parallel bars'},
                    {'name': 'Diamond Push-Ups', 'sets': 3, 'reps': '8-12', 'notes': 'Focus on triceps'},
                ]
            }
        }

        # Workout split templates
        self.split_templates = {
            'traditional': {
                3: ['push', 'pull', 'legs'],
                4: ['push', 'pull', 'legs', 'push'],
                5: ['push', 'pull', 'legs', 'push', 'pull'],
                6: ['push', 'pull', 'legs', 'push', 'pull', 'legs']
            },
            'upper_lower': {
                3: ['upper', 'lower', 'upper'],
                4: ['upper', 'lower', 'upper', 'lower'],
                5: ['upper', 'lower', 'upper', 'lower', 'upper'],
                6: ['upper', 'lower', 'upper', 'lower', 'upper', 'lower']
            },
            'body_part': {
                4: ['chest', 'back', 'legs', 'shoulders'],
                5: ['chest', 'back', 'legs', 'shoulders', 'arms'],
                6: ['chest', 'back', 'legs', 'shoulders', 'arms', 'legs']
            }
        }

    def generate_plan(self, user_data: Dict[str, Any]) -> TrainingPlan:
        """Generate a complete training plan based on user data."""
        goal = user_data.get('goal', 'strength')
        difficulty = user_data.get('difficulty', 'intermediate')
        duration_weeks = user_data.get('duration_weeks', 8)
        days_per_week = user_data.get('days_per_week', 4)
        training_style = user_data.get('training_style', 'traditional')
        equipment_available = user_data.get('equipment_available', ['barbell', 'dumbbell', 'bodyweight'])
        preferred_workout_duration = user_data.get('preferred_workout_duration', 60)
        include_deload_weeks = user_data.get('include_deload_weeks', False)
        experience_years = user_data.get('experience_years', 0)
        injuries_limitations = user_data.get('injuries_limitations', [])
        preferred_exercises = user_data.get('preferred_exercises', [])
        excluded_exercises = user_data.get('excluded_exercises', [])
        cardio_preferences = user_data.get('cardio_preferences', {})
        user = user_data.get('user')

        if not user:
            raise ValueError("User is required to generate a training plan")

        # Create the training plan with all preferences
        plan = TrainingPlan.objects.create(
            user=user,
            name=f"{goal.title()} Training Plan",
            description=f"AI-generated {duration_weeks}-week {difficulty} {goal} training plan",
            goal=goal,
            difficulty=difficulty,
            duration_weeks=duration_weeks,
            training_style=training_style,
            equipment_available=equipment_available,
            include_deload_weeks=include_deload_weeks,
            experience_years=experience_years,
            injuries_limitations=injuries_limitations,
            preferred_exercises=preferred_exercises,
            excluded_exercises=excluded_exercises,
            cardio_preferences=cardio_preferences,
            created_at=datetime.now()
        )

        # Generate workout split
        workout_split = self._generate_workout_split(days_per_week, training_style, goal)

        # Create weeks and days
        for week_num in range(1, duration_weeks + 1):
            week = TrainingWeek.objects.create(
                training_plan=plan,
                week_number=week_num,
                name=f"Week {week_num}",
                description=self._get_week_description(week_num, goal, difficulty)
            )

            # Determine if this is a deload week
            is_deload = include_deload_weeks and week_num % 4 == 0

            # Create training days
            rest_days = self._calculate_rest_days(days_per_week)
            workout_day_index = 0
            
            for day_num in range(1, 8):  # 1-7 for each day of the week
                if day_num not in rest_days:
                    workout_type = workout_split[workout_day_index % len(workout_split)]
                    
                    day = TrainingDay.objects.create(
                        training_week=week,
                        day_of_week=day_num,
                        name=self._get_workout_name(workout_type, goal),
                        description=self._get_workout_description(workout_type, goal, is_deload),
                        duration_minutes=preferred_workout_duration
                    )

                    # Generate exercises for this day
                    exercises = self._generate_exercises_for_day(
                        workout_type, goal, difficulty, equipment_available,
                        preferred_exercises, excluded_exercises, is_deload
                    )
                    
                    for i, exercise in enumerate(exercises, 1):
                        Exercise.objects.create(
                            training_day=day,
                            name=exercise['name'],
                            sets=exercise['sets'],
                            reps=exercise['reps'],
                            notes=exercise['notes'],
                            order=i
                        )
                    
                    workout_day_index += 1

        return plan

    def _generate_workout_split(self, days_per_week: int, training_style: str, goal: str) -> List[str]:
        """Generate workout split based on preferences."""
        if goal == 'powerlifting':
            return ['squat_focus', 'bench_focus', 'deadlift_focus'] * (days_per_week // 3 + 1)
        
        if goal == 'crossfit':
            return ['metcon', 'strength', 'skills'] * (days_per_week // 3 + 1)
        
        # Use appropriate split template
        if training_style == 'traditional' and days_per_week in self.split_templates['traditional']:
            return self.split_templates['traditional'][days_per_week]
        elif training_style in ['supersets', 'circuit'] and days_per_week in self.split_templates['upper_lower']:
            return self.split_templates['upper_lower'][days_per_week]
        elif days_per_week >= 4 and days_per_week in self.split_templates['body_part']:
            return self.split_templates['body_part'][days_per_week]
        else:
            # Default fallback
            if days_per_week <= 3:
                return ['full_body'] * days_per_week
            else:
                return ['push', 'pull', 'legs'] * (days_per_week // 3 + 1)

    def _generate_exercises_for_day(self, workout_type: str, goal: str, difficulty: str, 
                                   equipment_available: List[str], preferred_exercises: List[str],
                                   excluded_exercises: List[str], is_deload: bool) -> List[Dict[str, Any]]:
        """Generate exercises for a specific workout day."""
        exercises = []
        
        # Define muscle groups for each workout type
        muscle_groups = self._get_muscle_groups_for_workout(workout_type)
        
        # Number of exercises based on difficulty and goal
        num_exercises = self._get_exercise_count(difficulty, goal, workout_type)
        
        for muscle_group in muscle_groups:
            if muscle_group in self.exercise_database:
                # Get exercises for available equipment
                available_exercises = []
                for equipment in equipment_available:
                    if equipment in self.exercise_database[muscle_group]:
                        available_exercises.extend(self.exercise_database[muscle_group][equipment])
                
                # Filter based on preferences
                if preferred_exercises:
                    available_exercises = [ex for ex in available_exercises 
                                         if any(pref.lower() in ex['name'].lower() for pref in preferred_exercises)]
                
                if excluded_exercises:
                    available_exercises = [ex for ex in available_exercises 
                                         if not any(excl.lower() in ex['name'].lower() for excl in excluded_exercises)]
                
                # Select exercises for this muscle group
                if available_exercises:
                    exercises_per_group = max(1, num_exercises // len(muscle_groups))
                    selected = random.sample(available_exercises, min(exercises_per_group, len(available_exercises)))
                    
                    for exercise in selected:
                        # Adjust for deload
                        if is_deload:
                            exercise = exercise.copy()
                            exercise['sets'] = max(2, exercise['sets'] - 1)
                            exercise['notes'] = f"Deload: {exercise['notes']}"
                        
                        # Adjust sets/reps based on goal
                        exercise = self._adjust_exercise_for_goal(exercise, goal, difficulty)
                        exercises.append(exercise)
        
        return exercises[:num_exercises]  # Limit to target number

    def _get_muscle_groups_for_workout(self, workout_type: str) -> List[str]:
        """Get muscle groups for a workout type."""
        muscle_group_map = {
            'push': ['chest', 'shoulders', 'arms'],
            'pull': ['back', 'arms'],
            'legs': ['legs'],
            'upper': ['chest', 'back', 'shoulders', 'arms'],
            'lower': ['legs'],
            'full_body': ['chest', 'back', 'legs', 'shoulders'],
            'chest': ['chest'],
            'back': ['back'],
            'shoulders': ['shoulders'],
            'arms': ['arms'],
            'squat_focus': ['legs'],
            'bench_focus': ['chest', 'shoulders'],
            'deadlift_focus': ['back', 'legs']
        }
        return muscle_group_map.get(workout_type, ['chest', 'back', 'legs'])

    def _get_exercise_count(self, difficulty: str, goal: str, workout_type: str) -> int:
        """Get number of exercises based on difficulty and goal."""
        base_counts = {
            'beginner': 4,
            'intermediate': 6,
            'advanced': 8,
            'elite': 10
        }
        
        count = base_counts.get(difficulty, 6)
        
        # Adjust for workout type
        if workout_type in ['legs', 'full_body']:
            count += 2
        elif workout_type in ['arms']:
            count = max(4, count - 2)
            
        return count

    def _adjust_exercise_for_goal(self, exercise: Dict[str, Any], goal: str, difficulty: str) -> Dict[str, Any]:
        """Adjust exercise sets/reps based on goal and difficulty."""
        exercise = exercise.copy()
        
        if goal == 'strength':
            if difficulty in ['advanced', 'elite']:
                exercise['sets'] = min(5, exercise['sets'] + 1)
                exercise['reps'] = '3-6'
            else:
                exercise['reps'] = '5-8'
        elif goal == 'hypertrophy':
            exercise['reps'] = '8-12'
            if difficulty in ['advanced', 'elite']:
                exercise['sets'] = min(5, exercise['sets'] + 1)
        elif goal == 'endurance':
            exercise['reps'] = '12-20'
            exercise['sets'] = max(2, exercise['sets'] - 1)
        elif goal == 'weight_loss':
            exercise['reps'] = '10-15'
            exercise['notes'] = f"{exercise['notes']} - Higher intensity"
            
        return exercise

    def _calculate_rest_days(self, training_days: int) -> List[int]:
        """Calculate optimal rest days based on training frequency."""
        if training_days == 1:
            return [2, 3, 4, 5, 6, 7]
        elif training_days == 2:
            return [2, 4, 6, 7]
        elif training_days == 3:
            return [2, 4, 6, 7]
        elif training_days == 4:
            return [3, 6, 7]
        elif training_days == 5:
            return [6, 7]
        elif training_days == 6:
            return [7]
        else:
            return []

    def _get_week_description(self, week_num: int, goal: str, difficulty: str) -> str:
        """Generate a detailed description for the training week."""
        phase = (week_num - 1) % 4
        if difficulty in ['advanced', 'elite']:
            phases = {
                0: 'Accumulation - Focus on volume and technique',
                1: 'Intensification - Increase weights, decrease reps',
                2: 'Peak - Heavy weights, lower volume',
                3: 'Deload - Recovery and technique work'
            }
        else:
            phases = {
                0: 'Foundation - Build basic strength and form',
                1: 'Progressive overload - Gradually increase weights',
                2: 'Challenge - Push your limits',
                3: 'Active recovery - Maintain gains while recovering'
            }
        return f"Week {week_num}: {phases[phase]}"

    def _get_workout_name(self, workout_type: str, goal: str) -> str:
        """Generate a descriptive name for the workout."""
        workout_names = {
            'push': 'Push Day (Chest, Shoulders, Triceps)',
            'pull': 'Pull Day (Back, Biceps)',
            'legs': 'Leg Day',
            'upper': 'Upper Body',
            'lower': 'Lower Body',
            'full_body': 'Full Body Workout',
            'chest': 'Chest Workout',
            'back': 'Back Workout',
            'shoulders': 'Shoulder Workout',
            'arms': 'Arms Workout',
            'squat_focus': 'Squat Focus',
            'bench_focus': 'Bench Focus',
            'deadlift_focus': 'Deadlift Focus'
        }
        return workout_names.get(workout_type, workout_type.replace('_', ' ').title())

    def _get_workout_description(self, workout_type: str, goal: str, is_deload: bool) -> str:
        """Generate a detailed description for the workout."""
        base_descriptions = {
            'push': 'Focus on pushing movements: chest, shoulders, and triceps',
            'pull': 'Focus on pulling movements: back and biceps',
            'legs': 'Complete lower body training: quads, hamstrings, glutes, and calves',
            'upper': 'Complete upper body training: chest, back, shoulders, and arms',
            'lower': 'Lower body focus: legs and glutes',
            'full_body': 'Total body workout hitting all major muscle groups',
            'chest': 'Chest development with supporting muscle work',
            'back': 'Back development and posterior chain strengthening',
            'shoulders': 'Shoulder development and stability work',
            'arms': 'Biceps and triceps focused training'
        }
        
        base_desc = base_descriptions.get(workout_type, f"Focus on {workout_type.replace('_', ' ')} training")
        
        if is_deload:
            return f"Deload session: {base_desc} with reduced intensity"
        
        return base_desc

    def adjust_plan(self, plan: TrainingPlan, feedback: Dict[str, Any]) -> TrainingPlan:
        """Adjust the training plan based on user feedback."""
        # Implementation for adjusting the plan based on user feedback
        # This could include modifying exercises, sets, reps, etc.
        pass

    def regenerate_existing_plan(self, existing_plan: TrainingPlan, user_data: Dict[str, Any]) -> TrainingPlan:
        """Regenerate weeks and exercises for an existing training plan."""
        # Extract data from user_data
        goal = user_data.get('goal', 'strength')
        difficulty = user_data.get('difficulty', 'intermediate')
        duration_weeks = user_data.get('duration_weeks', 8)
        days_per_week = user_data.get('days_per_week', 4)
        training_style = user_data.get('training_style', 'traditional')
        equipment_available = user_data.get('equipment_available', ['barbell', 'dumbbell', 'bodyweight'])
        preferred_workout_duration = user_data.get('preferred_workout_duration', 60)
        include_deload_weeks = user_data.get('include_deload_weeks', False)
        injuries_limitations = user_data.get('injuries_limitations', [])
        preferred_exercises = user_data.get('preferred_exercises', [])
        excluded_exercises = user_data.get('excluded_exercises', [])

        # Generate workout split
        workout_split = self._generate_workout_split(days_per_week, training_style, goal)

        # Create weeks and days for the existing plan
        for week_num in range(1, duration_weeks + 1):
            week = TrainingWeek.objects.create(
                training_plan=existing_plan,
                week_number=week_num,
                name=f"Week {week_num}",
                description=self._get_week_description(week_num, goal, difficulty)
            )

            # Determine if this is a deload week
            is_deload = include_deload_weeks and week_num % 4 == 0

            # Create training days
            rest_days = self._calculate_rest_days(days_per_week)
            workout_day_index = 0
            
            for day_num in range(1, 8):  # 1-7 for each day of the week
                if day_num not in rest_days:
                    workout_type = workout_split[workout_day_index % len(workout_split)]
                    
                    day = TrainingDay.objects.create(
                        training_week=week,
                        day_of_week=day_num,
                        name=self._get_workout_name(workout_type, goal),
                        description=self._get_workout_description(workout_type, goal, is_deload),
                        duration_minutes=preferred_workout_duration
                    )

                    # Generate exercises for this day
                    exercises = self._generate_exercises_for_day(
                        workout_type, goal, difficulty, equipment_available,
                        preferred_exercises, excluded_exercises, is_deload
                    )
                    
                    for i, exercise in enumerate(exercises, 1):
                        Exercise.objects.create(
                            training_day=day,
                            name=exercise['name'],
                            sets=exercise['sets'],
                            reps=exercise['reps'],
                            notes=exercise['notes'],
                            order=i
                        )
                    
                    workout_day_index += 1

        return existing_plan 