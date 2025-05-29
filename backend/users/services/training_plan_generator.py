from typing import List, Dict, Any
import random
from datetime import datetime
from ..models import TrainingPlan, TrainingWeek, TrainingDay, Exercise

class TrainingPlanGenerator:
    def __init__(self):
        self.exercise_templates = {
            'strength': {
                'chest': [
                    {'name': 'Bench Press', 'sets': 4, 'reps': '6-8', 'notes': 'Focus on controlled movement'},
                    {'name': 'Incline Dumbbell Press', 'sets': 3, 'reps': '8-12', 'notes': 'Keep elbows at 45 degrees'},
                    {'name': 'Push-Ups', 'sets': 3, 'reps': '12-15', 'notes': 'Full range of motion'},
                    {'name': 'Dips', 'sets': 3, 'reps': '8-10', 'notes': 'Control the descent'}
                ],
                'back': [
                    {'name': 'Deadlift', 'sets': 4, 'reps': '5-6', 'notes': 'Maintain neutral spine'},
                    {'name': 'Pull-Ups', 'sets': 3, 'reps': '8-12', 'notes': 'Full hang at bottom'},
                    {'name': 'Barbell Rows', 'sets': 3, 'reps': '8-12', 'notes': 'Squeeze shoulder blades'},
                    {'name': 'Lat Pulldowns', 'sets': 3, 'reps': '10-12', 'notes': 'Wide grip'}
                ],
                'legs': [
                    {'name': 'Squats', 'sets': 4, 'reps': '6-8', 'notes': 'Break parallel'},
                    {'name': 'Romanian Deadlifts', 'sets': 3, 'reps': '8-12', 'notes': 'Feel hamstring stretch'},
                    {'name': 'Leg Press', 'sets': 3, 'reps': '10-12', 'notes': 'Control the eccentric'},
                    {'name': 'Bulgarian Split Squats', 'sets': 3, 'reps': '8-10', 'notes': 'Keep front knee stable'}
                ],
                'shoulders': [
                    {'name': 'Military Press', 'sets': 4, 'reps': '6-8', 'notes': 'Full lockout'},
                    {'name': 'Lateral Raises', 'sets': 3, 'reps': '12-15', 'notes': 'Control the movement'},
                    {'name': 'Face Pulls', 'sets': 3, 'reps': '12-15', 'notes': 'Focus on rear delts'},
                    {'name': 'Arnold Press', 'sets': 3, 'reps': '10-12', 'notes': 'Full rotation'}
                ],
                'arms': [
                    {'name': 'Barbell Curls', 'sets': 3, 'reps': '8-12', 'notes': 'No swinging'},
                    {'name': 'Tricep Pushdowns', 'sets': 3, 'reps': '10-12', 'notes': 'Keep elbows tucked'},
                    {'name': 'Hammer Curls', 'sets': 3, 'reps': '10-12', 'notes': 'Neutral grip'},
                    {'name': 'Skull Crushers', 'sets': 3, 'reps': '10-12', 'notes': 'Keep elbows in'}
                ]
            },
            'hypertrophy': {
                'chest': [
                    {'name': 'Bench Press', 'sets': 4, 'reps': '8-12', 'notes': 'Focus on muscle contraction'},
                    {'name': 'Incline Dumbbell Press', 'sets': 4, 'reps': '10-15', 'notes': 'Squeeze at the top'},
                    {'name': 'Cable Flyes', 'sets': 3, 'reps': '12-15', 'notes': 'Keep tension throughout'},
                    {'name': 'Machine Press', 'sets': 3, 'reps': '12-15', 'notes': 'Slow negatives'}
                ],
                'back': [
                    {'name': 'Lat Pulldowns', 'sets': 4, 'reps': '10-15', 'notes': 'Full stretch at top'},
                    {'name': 'Cable Rows', 'sets': 4, 'reps': '12-15', 'notes': 'Squeeze shoulder blades'},
                    {'name': 'Machine Pulldowns', 'sets': 3, 'reps': '12-15', 'notes': 'Focus on lats'},
                    {'name': 'Face Pulls', 'sets': 3, 'reps': '15-20', 'notes': 'High reps for rear delts'}
                ],
                'legs': [
                    {'name': 'Leg Press', 'sets': 4, 'reps': '12-15', 'notes': 'Full range of motion'},
                    {'name': 'Hack Squats', 'sets': 4, 'reps': '10-12', 'notes': 'Control the descent'},
                    {'name': 'Leg Extensions', 'sets': 3, 'reps': '15-20', 'notes': 'Hold peak contraction'},
                    {'name': 'Leg Curls', 'sets': 3, 'reps': '12-15', 'notes': 'Focus on hamstrings'}
                ]
            },
            'endurance': {
                'full_body': [
                    {'name': 'Mountain Climbers', 'sets': 3, 'reps': '30 seconds', 'notes': 'Keep core tight'},
                    {'name': 'Burpees', 'sets': 3, 'reps': '45 seconds', 'notes': 'Explosive movement'},
                    {'name': 'Jump Rope', 'sets': 3, 'reps': '60 seconds', 'notes': 'Stay light on feet'},
                    {'name': 'Bodyweight Squats', 'sets': 3, 'reps': '30 reps', 'notes': 'Quick pace'}
                ],
                'hiit': [
                    {'name': 'Sprint', 'sets': 8, 'reps': '30 seconds', 'notes': '30s work, 30s rest'},
                    {'name': 'Jump Squats', 'sets': 8, 'reps': '20 reps', 'notes': 'Explosive jumps'},
                    {'name': 'Push-Ups', 'sets': 8, 'reps': '15 reps', 'notes': 'Quick but controlled'},
                    {'name': 'High Knees', 'sets': 8, 'reps': '30 seconds', 'notes': 'Drive knees high'}
                ]
            }
        }

    def _generate_workout_split(self, difficulty: str) -> List[str]:
        """Generate a workout split based on difficulty."""
        if difficulty == 'beginner':
            return ['full_body'] * 3
        elif difficulty == 'intermediate':
            return ['push', 'pull', 'legs'] * 2
        else:  # advanced
            return ['chest', 'back', 'legs', 'shoulders', 'arms', 'legs']

    def _select_exercises(self, muscle_group: str, goal: str, difficulty: str) -> List[Dict[str, Any]]:
        """Select appropriate exercises for a given muscle group and difficulty."""
        exercises = self.exercise_templates.get(goal, {}).get(muscle_group, [])
        num_exercises = {
            'beginner': 3,
            'intermediate': 4,
            'advanced': 5
        }.get(difficulty, 3)
        
        return random.sample(exercises, min(num_exercises, len(exercises)))

    def _calculate_volume(self, difficulty: str, goal: str) -> Dict[str, range]:
        """Calculate appropriate volume based on difficulty and goal."""
        base_sets = {
            'beginner': (2, 3),
            'intermediate': (3, 4),
            'advanced': (4, 5)
        }.get(difficulty, (2, 3))

        base_reps = {
            'strength': (4, 8),
            'hypertrophy': (8, 12),
            'endurance': (12, 15)
        }.get(goal, (8, 12))

        return {'sets': base_sets, 'reps': base_reps}

    def generate_plan(self, user_data: Dict[str, Any]) -> TrainingPlan:
        """Generate a complete training plan based on user data."""
        goal = user_data.get('goal', 'strength')
        difficulty = user_data.get('difficulty', 'intermediate')
        duration_weeks = user_data.get('duration_weeks', 8)
        days_per_week = user_data.get('days_per_week', 4)
        focus_areas = user_data.get('focus_areas', ['chest', 'back', 'legs', 'shoulders', 'arms'])
        include_cardio = user_data.get('include_cardio', True)
        preferred_workout_duration = user_data.get('preferred_workout_duration', 60)
        user = user_data.get('user')

        if not user:
            raise ValueError("User is required to generate a training plan")

        # Create the training plan
        plan = TrainingPlan.objects.create(
            user=user,
            name=f"{goal.title()} Training Plan",
            description=f"AI-generated {duration_weeks}-week {difficulty} {goal} training plan",
            goal=goal,
            difficulty=difficulty,
            duration_weeks=duration_weeks,
            created_at=datetime.now()
        )

        # Generate workout split based on days per week
        workout_split = self._generate_advanced_split(days_per_week, goal, focus_areas)

        # Create weeks and days
        for week_num in range(1, duration_weeks + 1):
            week = TrainingWeek.objects.create(
                training_plan=plan,
                week_number=week_num,
                name=f"Week {week_num}",
                description=self._get_week_description(week_num, goal, difficulty)
            )

            # Determine if this is a deload week
            is_deload = week_num % 4 == 0 and difficulty in ['intermediate', 'advanced', 'elite']

            # Create training days
            rest_days = self._calculate_rest_days(days_per_week)
            for day_num in range(1, 8):  # 1-7 for each day of the week
                if day_num not in rest_days:
                    day_index = len([d for d in range(1, day_num) if d not in rest_days])
                    workout_type = workout_split[day_index % len(workout_split)]
                    
                    day = TrainingDay.objects.create(
                        training_week=week,
                        day_of_week=day_num,
                        name=self._get_workout_name(workout_type, goal),
                        description=self._get_workout_description(workout_type, goal, is_deload),
                        duration_minutes=preferred_workout_duration
                    )

                    # Add exercises
                    exercises = self._generate_exercises_for_day(
                        workout_type,
                        goal,
                        difficulty,
                        is_deload,
                        include_cardio
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

        return plan

    def _generate_advanced_split(self, days_per_week: int, goal: str, focus_areas: List[str]) -> List[str]:
        """Generate an advanced workout split based on training days and goal."""
        if goal == 'powerlifting':
            return ['squat', 'bench', 'deadlift'] * 2

        if goal == 'crossfit':
            return ['metcon', 'strength', 'skills'] * 2

        if days_per_week <= 3:
            return ['full_body'] * 3

        if days_per_week == 4:
            if 'chest' in focus_areas and 'back' in focus_areas:
                return ['upper', 'lower', 'push', 'pull']
            return ['chest_back', 'legs', 'shoulders_arms', 'full_body']

        if days_per_week == 5:
            return ['push', 'pull', 'legs', 'upper', 'lower']

        return ['push', 'pull', 'legs'] * 2

    def _calculate_rest_days(self, training_days: int) -> List[int]:
        """Calculate optimal rest days based on training frequency."""
        if training_days == 3:
            return [1, 3, 5, 7]  # Monday, Wednesday, Friday
        if training_days == 4:
            return [1, 3, 5, 7]  # Monday, Wednesday, Friday, Sunday
        if training_days == 5:
            return [1, 7]  # Saturday, Sunday
        return [7]  # Sunday only for 6 days

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
        if goal == 'powerlifting':
            return f"{workout_type.title()} Focus Day"
        if goal == 'crossfit':
            return f"{workout_type.title()} WOD"
        return f"{workout_type.replace('_', ' ').title()} Workout"

    def _get_workout_description(self, workout_type: str, goal: str, is_deload: bool) -> str:
        """Generate a detailed description for the workout."""
        base_desc = f"Focus on {workout_type.replace('_', ' ')} training"
        if is_deload:
            return f"Deload session: {base_desc} with reduced weight and volume"
        if goal == 'powerlifting':
            return f"Heavy {base_desc} with emphasis on competition movements"
        if goal == 'crossfit':
            return f"High-intensity {base_desc} combining strength and conditioning"
        return base_desc

    def _generate_exercises_for_day(
        self,
        workout_type: str,
        goal: str,
        difficulty: str,
        is_deload: bool,
        include_cardio: bool
    ) -> List[Dict[str, Any]]:
        """Generate a list of exercises for a workout day."""
        exercises = self.exercise_templates.get(goal, {}).get(workout_type, [])
        
        # Adjust volume based on deload
        if is_deload:
            for exercise in exercises:
                exercise['sets'] = max(2, exercise['sets'] - 1)
                exercise['notes'] = f"Deload: {exercise['notes']}"

        # Add cardio if requested
        if include_cardio and workout_type not in ['cardio', 'metcon']:
            cardio = {
                'name': 'HIIT Cardio',
                'sets': 1,
                'reps': '15-20 minutes',
                'notes': 'Alternate between 30s high intensity and 30s rest'
            }
            exercises.append(cardio)

        return exercises

    def adjust_plan(self, plan: TrainingPlan, feedback: Dict[str, Any]) -> TrainingPlan:
        """Adjust the training plan based on user feedback."""
        # Implementation for adjusting the plan based on user feedback
        # This could include modifying exercises, sets, reps, etc.
        pass 