import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import random
from typing import Dict, List, Tuple, Optional, Union


class UserProfile:
    """
    Stores and manages user profile information for personalization
    """

    def __init__(self,
                 user_id: str,
                 age: int,
                 gender: str,
                 height: float,  # in cm
                 weight: float,  # in kg
                 goal: str,  # 'weight_loss', 'muscle_gain', 'maintenance'
                 activity_level: str,
                 # 'sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active'
                 dietary_restrictions: List[str] = None,
                 allergies: List[str] = None,
                 fitness_experience: str = 'beginner',  # 'beginner', 'intermediate', 'advanced'
                 preferred_workout_days: int = 3,
                 workout_duration: int = 45,  # in minutes
                 available_equipment: List[str] = None,
                 health_conditions: List[str] = None,
                 favorite_foods: List[str] = None,
                 disliked_foods: List[str] = None):

        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.goal = goal
        self.activity_level = activity_level
        self.dietary_restrictions = dietary_restrictions or []
        self.allergies = allergies or []
        self.fitness_experience = fitness_experience
        self.preferred_workout_days = preferred_workout_days
        self.workout_duration = workout_duration
        self.available_equipment = available_equipment or ['bodyweight']
        self.health_conditions = health_conditions or []
        self.favorite_foods = favorite_foods or []
        self.disliked_foods = disliked_foods or []

        # Calculate BMI and BMR
        self.bmi = self._calculate_bmi()
        self.bmr = self._calculate_bmr()
        self.tdee = self._calculate_tdee()
        self.target_calories = self._calculate_target_calories()
        self.macros = self._calculate_macros()

    def _calculate_bmi(self) -> float:
        """Calculate Body Mass Index"""
        return round(self.weight / ((self.height / 100) ** 2), 2)

    def _calculate_bmr(self) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation"""
        if self.gender.lower() == 'male':
            return round((10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5, 2)
        else:  # female
            return round((10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161, 2)

    def _calculate_tdee(self) -> float:
        """Calculate Total Daily Energy Expenditure"""
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }

        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        return round(self.bmr * multiplier, 2)

    def _calculate_target_calories(self) -> float:
        """Calculate target calories based on goals"""
        if self.goal == 'weight_loss':
            # 20% caloric deficit
            return round(self.tdee * 0.8, 2)
        elif self.goal == 'muscle_gain':
            # 10% caloric surplus
            return round(self.tdee * 1.1, 2)
        else:  # maintenance
            return self.tdee

    def _calculate_macros(self) -> Dict[str, float]:
        """Calculate macronutrient targets based on goal"""
        if self.goal == 'weight_loss':
            protein_pct = 0.40  # Higher protein for weight loss
            fat_pct = 0.30
            carb_pct = 0.30
        elif self.goal == 'muscle_gain':
            protein_pct = 0.30
            fat_pct = 0.25
            carb_pct = 0.45  # Higher carbs for muscle gain
        else:  # maintenance
            protein_pct = 0.30
            fat_pct = 0.30
            carb_pct = 0.40

        # Calculate grams
        protein_cals = self.target_calories * protein_pct
        fat_cals = self.target_calories * fat_pct
        carb_cals = self.target_calories * carb_pct

        # Convert to grams
        protein_g = round(protein_cals / 4, 2)  # 4 calories per gram of protein
        fat_g = round(fat_cals / 9, 2)  # 9 calories per gram of fat
        carb_g = round(carb_cals / 4, 2)  # 4 calories per gram of carb

        return {
            'protein': protein_g,
            'fat': fat_g,
            'carbs': carb_g
        }

    def to_dict(self) -> Dict:
        """Convert user profile to dictionary"""
        return {
            'user_id': self.user_id,
            'age': self.age,
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'bmi': self.bmi,
            'bmr': self.bmr,
            'tdee': self.tdee,
            'goal': self.goal,
            'activity_level': self.activity_level,
            'dietary_restrictions': self.dietary_restrictions,
            'allergies': self.allergies,
            'fitness_experience': self.fitness_experience,
            'preferred_workout_days': self.preferred_workout_days,
            'workout_duration': self.workout_duration,
            'available_equipment': self.available_equipment,
            'health_conditions': self.health_conditions,
            'target_calories': self.target_calories,
            'macros': self.macros
        }


class FoodDatabase:
    """
    A database of foods with nutritional information
    """

    def __init__(self, food_data_path: Optional[str] = None):
        # Load from path if provided, otherwise use sample data
        if food_data_path:
            self.foods = self._load_food_data(food_data_path)
        else:
            self.foods = self._create_sample_food_data()

    def _load_food_data(self, filepath: str) -> pd.DataFrame:
        """Load food data from CSV or JSON file"""
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith('.json'):
            return pd.DataFrame(json.load(open(filepath)))
        else:
            raise ValueError("Unsupported file format. Please provide CSV or JSON.")

    def _create_sample_food_data(self) -> pd.DataFrame:
        """Create a small sample food database"""
        foods = [
            # Proteins
            {"name": "Chicken Breast", "category": "protein", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6,
             "serving_size": "100g", "tags": ["high_protein", "low_carb"]},
            {"name": "Salmon", "category": "protein", "calories": 208, "protein": 20, "carbs": 0, "fat": 13,
             "serving_size": "100g", "tags": ["high_protein", "healthy_fat", "omega3"]},
            {"name": "Tofu", "category": "protein", "calories": 144, "protein": 17, "carbs": 3, "fat": 8,
             "serving_size": "100g", "tags": ["vegetarian", "vegan", "plant_based"]},
            {"name": "Greek Yogurt", "category": "protein", "calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4,
             "serving_size": "100g", "tags": ["high_protein", "probiotic", "breakfast"]},
            {"name": "Eggs", "category": "protein", "calories": 143, "protein": 13, "carbs": 1, "fat": 9.5,
             "serving_size": "2 eggs", "tags": ["high_protein", "breakfast"]},
            {"name": "Lean Beef", "category": "protein", "calories": 250, "protein": 26, "carbs": 0, "fat": 17,
             "serving_size": "100g", "tags": ["high_protein", "iron_rich"]},
            {"name": "Turkey Breast", "category": "protein", "calories": 157, "protein": 24, "carbs": 0, "fat": 7,
             "serving_size": "100g", "tags": ["high_protein", "low_fat"]},
            {"name": "Lentils", "category": "protein", "calories": 116, "protein": 9, "carbs": 20, "fat": 0.4,
             "serving_size": "100g", "tags": ["vegetarian", "vegan", "plant_based", "fiber"]},

            # Carbohydrates
            {"name": "Brown Rice", "category": "carb", "calories": 112, "protein": 2.6, "carbs": 23, "fat": 0.9,
             "serving_size": "100g", "tags": ["whole_grain", "gluten_free"]},
            {"name": "Sweet Potato", "category": "carb", "calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1,
             "serving_size": "100g", "tags": ["complex_carbs", "vitamin_a"]},
            {"name": "Quinoa", "category": "carb", "calories": 120, "protein": 4.4, "carbs": 21.3, "fat": 1.9,
             "serving_size": "100g", "tags": ["whole_grain", "complete_protein", "gluten_free"]},
            {"name": "Oats", "category": "carb", "calories": 389, "protein": 16.9, "carbs": 66.3, "fat": 6.9,
             "serving_size": "100g", "tags": ["whole_grain", "fiber", "breakfast"]},
            {"name": "Whole Wheat Bread", "category": "carb", "calories": 265, "protein": 13.2, "carbs": 43.1,
             "fat": 4.2, "serving_size": "100g", "tags": ["whole_grain", "fiber"]},
            {"name": "Banana", "category": "carb", "calories": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3,
             "serving_size": "1 medium", "tags": ["fruit", "potassium", "quick_energy"]},
            {"name": "Pasta (whole grain)", "category": "carb", "calories": 131, "protein": 5.3, "carbs": 27.2,
             "fat": 0.9, "serving_size": "100g", "tags": ["whole_grain", "complex_carbs"]},

            # Fats
            {"name": "Avocado", "category": "fat", "calories": 160, "protein": 2, "carbs": 8.5, "fat": 14.7,
             "serving_size": "1/2 avocado", "tags": ["healthy_fat", "monounsaturated"]},
            {"name": "Olive Oil", "category": "fat", "calories": 119, "protein": 0, "carbs": 0, "fat": 13.5,
             "serving_size": "1 tbsp", "tags": ["healthy_fat", "monounsaturated"]},
            {"name": "Almonds", "category": "fat", "calories": 164, "protein": 6, "carbs": 6, "fat": 14,
             "serving_size": "28g", "tags": ["healthy_fat", "fiber", "snack"]},
            {"name": "Chia Seeds", "category": "fat", "calories": 58, "protein": 2, "carbs": 4, "fat": 3.7,
             "serving_size": "1 tbsp", "tags": ["healthy_fat", "omega3", "fiber"]},

            # Vegetables
            {"name": "Broccoli", "category": "vegetable", "calories": 34, "protein": 2.8, "carbs": 6.6, "fat": 0.4,
             "serving_size": "100g", "tags": ["cruciferous", "fiber", "vitamin_c"]},
            {"name": "Spinach", "category": "vegetable", "calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4,
             "serving_size": "100g", "tags": ["leafy_green", "iron", "vitamin_k"]},
            {"name": "Bell Pepper", "category": "vegetable", "calories": 31, "protein": 1, "carbs": 6, "fat": 0.3,
             "serving_size": "100g", "tags": ["vitamin_c", "antioxidants"]},
            {"name": "Carrots", "category": "vegetable", "calories": 41, "protein": 0.9, "carbs": 9.6, "fat": 0.2,
             "serving_size": "100g", "tags": ["vitamin_a", "fiber"]}
        ]
        return pd.DataFrame(foods)

    def get_foods_by_category(self, category: str) -> pd.DataFrame:
        """Retrieve foods by category"""
        return self.foods[self.foods['category'] == category]

    def get_foods_by_tag(self, tag: str) -> pd.DataFrame:
        """Retrieve foods containing a specific tag"""
        return self.foods[self.foods['tags'].apply(lambda x: tag in x)]

    def filter_by_restrictions(self, restrictions: List[str]) -> pd.DataFrame:
        """Filter out foods with certain tags based on dietary restrictions"""
        filtered_foods = self.foods.copy()
        restriction_tag_map = {
            'vegetarian': ['vegetarian', 'vegan', 'plant_based'],
            'vegan': ['vegan', 'plant_based'],
            'gluten_free': ['gluten_free'],
            'dairy_free': ['dairy_free', 'vegan', 'plant_based'],
            'nut_free': ['nut_free']
        }

        for restriction in restrictions:
            if restriction in restriction_tag_map:
                allowed_tags = restriction_tag_map[restriction]
                # For each restriction, keep only foods that have at least one of the allowed tags
                filtered_foods = filtered_foods[filtered_foods['tags'].apply(
                    lambda x: any(tag in x for tag in allowed_tags)
                )]

        return filtered_foods

    def get_food_item(self, food_name: str) -> Dict:
        """Get a specific food item by name"""
        food = self.foods[self.foods['name'] == food_name]
        if food.empty:
            return None
        return food.iloc[0].to_dict()


class ExerciseDatabase:
    """
    A database of exercises with categorization and difficulty levels
    """

    def __init__(self, exercise_data_path: Optional[str] = None):
        # Load from path if provided, otherwise use sample data
        if exercise_data_path:
            self.exercises = self._load_exercise_data(exercise_data_path)
        else:
            self.exercises = self._create_sample_exercise_data()

    def _load_exercise_data(self, filepath: str) -> pd.DataFrame:
        """Load exercise data from CSV or JSON file"""
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith('.json'):
            return pd.DataFrame(json.load(open(filepath)))
        else:
            raise ValueError("Unsupported file format. Please provide CSV or JSON.")

    def _create_sample_exercise_data(self) -> pd.DataFrame:
        """Create a small sample exercise database"""
        exercises = [
            # Strength Training - Upper Body
            {"name": "Push-up", "category": "strength", "muscle_group": "chest", "difficulty": "beginner",
             "equipment": ["bodyweight"], "description": "Standard push-up targeting chest, shoulders, and triceps.",
             "instructions": "Place hands slightly wider than shoulder-width apart. Lower body until chest nearly touches the floor. Push back up to starting position."},
            {"name": "Dumbbell Bench Press", "category": "strength", "muscle_group": "chest",
             "difficulty": "intermediate", "equipment": ["dumbbells", "bench"],
             "description": "Chest press with dumbbells for balanced chest development.",
             "instructions": "Lie on bench with dumbbells at chest level. Press weights upward until arms are extended. Lower weights back to starting position."},
            {"name": "Pull-up", "category": "strength", "muscle_group": "back", "difficulty": "intermediate",
             "equipment": ["pull-up bar"], "description": "Upper body pulling exercise for back and biceps.",
             "instructions": "Grip pull-up bar with hands wider than shoulder width. Pull body up until chin is over the bar. Lower back to starting position with control."},
            {"name": "Dumbbell Row", "category": "strength", "muscle_group": "back", "difficulty": "beginner",
             "equipment": ["dumbbells", "bench"],
             "description": "Unilateral back exercise targeting lats and middle back.",
             "instructions": "Place one knee and hand on bench. Hold dumbbell with free hand. Pull dumbbell to hip, keeping elbow close to body. Lower with control."},
            {"name": "Overhead Press", "category": "strength", "muscle_group": "shoulders",
             "difficulty": "intermediate", "equipment": ["dumbbells", "barbell"],
             "description": "Vertical pressing movement for shoulder development.",
             "instructions": "Hold weights at shoulder level. Press weights overhead until arms are fully extended. Lower weights back to shoulder level."},
            {"name": "Bicep Curl", "category": "strength", "muscle_group": "arms", "difficulty": "beginner",
             "equipment": ["dumbbells", "barbell"], "description": "Isolation exercise for biceps.",
             "instructions": "Hold weights with arms extended at sides. Curl weights towards shoulders while keeping elbows fixed. Lower with control."},
            {"name": "Tricep Dip", "category": "strength", "muscle_group": "arms", "difficulty": "intermediate",
             "equipment": ["bench", "dip bars"], "description": "Bodyweight exercise targeting triceps.",
             "instructions": "Support body with hands on bench or dip bars. Lower body by bending elbows. Push back up to starting position."},

            # Strength Training - Lower Body
            {"name": "Bodyweight Squat", "category": "strength", "muscle_group": "legs", "difficulty": "beginner",
             "equipment": ["bodyweight"],
             "description": "Fundamental lower body exercise targeting quads, hamstrings, and glutes.",
             "instructions": "Stand with feet shoulder-width apart. Bend knees and lower hips as if sitting in a chair. Return to standing position."},
            {"name": "Barbell Squat", "category": "strength", "muscle_group": "legs", "difficulty": "intermediate",
             "equipment": ["barbell", "squat rack"], "description": "Compound lower body movement with external load.",
             "instructions": "Place barbell across upper back. Squat by bending knees and lowering hips. Return to standing position."},
            {"name": "Deadlift", "category": "strength", "muscle_group": "legs", "difficulty": "intermediate",
             "equipment": ["barbell"],
             "description": "Posterior chain exercise targeting hamstrings, glutes, and lower back.",
             "instructions": "Stand with feet hip-width apart, barbell over mid-foot. Bend at hips and knees to grip bar. Lift bar by extending hips and knees. Return bar to floor with control."},
            {"name": "Lunge", "category": "strength", "muscle_group": "legs", "difficulty": "beginner",
             "equipment": ["bodyweight", "dumbbells"],
             "description": "Unilateral leg exercise for balanced lower body development.",
             "instructions": "Step forward with one leg. Lower body until both knees are bent at 90 degrees. Push off front foot to return to starting position."},
            {"name": "Glute Bridge", "category": "strength", "muscle_group": "legs", "difficulty": "beginner",
             "equipment": ["bodyweight", "barbell"],
             "description": "Hip extension exercise targeting glutes and hamstrings.",
             "instructions": "Lie on back with knees bent, feet flat on floor. Lift hips toward ceiling by squeezing glutes. Lower hips with control."},

            # Core Training
            {"name": "Plank", "category": "core", "muscle_group": "core", "difficulty": "beginner",
             "equipment": ["bodyweight"],
             "description": "Isometric core exercise for overall core strength and stability.",
             "instructions": "Support body on forearms and toes. Maintain straight line from head to heels. Hold position."},
            {"name": "Russian Twist", "category": "core", "muscle_group": "core", "difficulty": "intermediate",
             "equipment": ["bodyweight", "medicine ball"],
             "description": "Rotational core exercise targeting obliques.",
             "instructions": "Sit with knees bent, feet elevated. Lean back slightly. Rotate torso side to side, touching hands or weight to floor beside hips."},
            {"name": "Mountain Climber", "category": "core", "muscle_group": "core", "difficulty": "beginner",
             "equipment": ["bodyweight"], "description": "Dynamic core exercise with cardiovascular benefits.",
             "instructions": "Start in push-up position. Rapidly alternate bringing knees toward chest, keeping hips level."},

            # Cardiovascular Training
            {"name": "Running", "category": "cardio", "muscle_group": "full body", "difficulty": "adjustable",
             "equipment": ["none"], "description": "Basic cardiovascular exercise for endurance and calorie burning.",
             "instructions": "Run at consistent pace, maintaining upright posture and rhythmic breathing."},
            {"name": "Cycling", "category": "cardio", "muscle_group": "lower body", "difficulty": "adjustable",
             "equipment": ["bicycle", "stationary bike"],
             "description": "Low-impact cardiovascular exercise focusing on lower body.",
             "instructions": "Maintain comfortable cadence, adjusting resistance as needed for workout intensity."},
            {"name": "Jumping Jacks", "category": "cardio", "muscle_group": "full body", "difficulty": "beginner",
             "equipment": ["bodyweight"], "description": "Classic calisthenic exercise for heart rate elevation.",
             "instructions": "Start standing with arms at sides. Jump while spreading legs and raising arms overhead. Jump back to starting position."},
            {"name": "Burpee", "category": "cardio", "muscle_group": "full body", "difficulty": "advanced",
             "equipment": ["bodyweight"],
             "description": "High-intensity full body exercise combining strength and cardio.",
             "instructions": "From standing, drop into squat position and place hands on floor. Jump feet back to plank position. Perform push-up. Jump feet forward to squat position. Jump explosively with arms overhead."},
            {"name": "Jump Rope", "category": "cardio", "muscle_group": "full body", "difficulty": "beginner",
             "equipment": ["jump rope"], "description": "Coordination-based cardiovascular exercise.",
             "instructions": "Swing rope over head and jump as it passes under feet. Maintain light, continuous jumps using balls of feet."},

            # Flexibility & Mobility
            {"name": "Hamstring Stretch", "category": "flexibility", "muscle_group": "legs", "difficulty": "beginner",
             "equipment": ["none"], "description": "Static stretch for hamstring flexibility.",
             "instructions": "Sit with one leg extended, other leg bent. Reach toward toes of extended leg. Hold stretch for 20-30 seconds."},
            {"name": "Shoulder Stretch", "category": "flexibility", "muscle_group": "shoulders",
             "difficulty": "beginner", "equipment": ["none"], "description": "Basic stretch for shoulder mobility.",
             "instructions": "Bring one arm across chest. Use opposite arm to gently pull elbow toward chest. Hold for 20-30 seconds."},
            {"name": "Hip Flexor Stretch", "category": "flexibility", "muscle_group": "hips", "difficulty": "beginner",
             "equipment": ["none"], "description": "Static stretch for hip mobility and flexibility.",
             "instructions": "Kneel with one knee on floor, other foot flat in front. Push hips forward slightly until stretch is felt in front of hip. Hold for 20-30 seconds."},
            {"name": "Sun Salutation", "category": "flexibility", "muscle_group": "full body",
             "difficulty": "intermediate", "equipment": ["yoga mat"],
             "description": "Yoga sequence for full-body mobility and flexibility.",
             "instructions": "Flow through sequence of poses including mountain pose, forward fold, plank, upward dog, downward dog, and back to standing."}
        ]
        return pd.DataFrame(exercises)

    def get_exercises_by_category(self, category: str) -> pd.DataFrame:
        """Retrieve exercises by category"""
        return self.exercises[self.exercises['category'] == category]

    def get_exercises_by_muscle_group(self, muscle_group: str) -> pd.DataFrame:
        """Retrieve exercises by muscle group"""
        return self.exercises[self.exercises['muscle_group'] == muscle_group]

    def get_exercises_by_difficulty(self, difficulty: str) -> pd.DataFrame:
        """Retrieve exercises by difficulty level"""
        return self.exercises[self.exercises['difficulty'] == difficulty]

    def get_exercises_by_equipment(self, equipment: List[str]) -> pd.DataFrame:
        """Retrieve exercises that can be performed with available equipment"""
        # Return exercises where at least one of the required equipment items is in the user's available equipment
        return self.exercises[self.exercises['equipment'].apply(
            lambda x: any(item in equipment for item in x)
        )]

    def get_exercise(self, exercise_name: str) -> Dict:
        """Get a specific exercise by name"""
        exercise = self.exercises[self.exercises['name'] == exercise_name]
        if exercise.empty:
            return None
        return exercise.iloc[0].to_dict()


class MealPlanner:
    """
    Generates personalized meal plans based on user profile and preferences
    """

    def __init__(self, food_database: FoodDatabase):
        self.food_db = food_database

    def generate_daily_meals(self,
                             user_profile: UserProfile,
                             meal_count: int = 3,
                             snack_count: int = 2) -> Dict:
        """
        Generate a full day's meal plan based on user profile

        Args:
            user_profile: UserProfile object with user data
            meal_count: Number of main meals to include
            snack_count: Number of snacks to include

        Returns:
            Dictionary with meal plan details
        """
        # Filter foods based on dietary restrictions
        available_foods = self.food_db.foods
        if user_profile.dietary_restrictions:
            available_foods = self.food_db.filter_by_restrictions(user_profile.dietary_restrictions)

        # Remove foods with allergens
        if user_profile.allergies:
            # This is a simplified version - in a real system, you'd have a more robust
            # way to identify allergens in foods
            for allergen in user_profile.allergies:
                available_foods = available_foods[~available_foods['name'].str.contains(allergen, case=False)]

        # Calculate calories per meal and snack
        calories_per_main_meal = user_profile.target_calories * 0.8 / meal_count
        calories_per_snack = user_profile.target_calories * 0.2 / snack_count

        # Dictionary to hold the meal plan
        meal_plan = {
            'daily_target': {
                'calories': user_profile.target_calories,
                'protein': user_profile.macros['protein'],
                'carbs': user_profile.macros['carbs'],
                'fat': user_profile.macros['fat']
            },
            'meals': [],
            'snacks': [],
            'total_nutrition': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }
        }

        # Generate main meals
        meal_names = ['Breakfast', 'Lunch', 'Dinner', 'Pre-workout Meal', 'Post-workout Meal']
        for i in range(meal_count):
            meal = self._generate_meal(
                available_foods,
                target_calories=calories_per_main_meal,
                protein_ratio=0.35,  # Higher protein ratio for main meals
                meal_type=meal_names[i] if i < len(meal_names) else f"Meal {i + 1}"
            )

            # Add to meal plan and update totals
            meal_plan['meals'].append(meal)
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                meal_plan['total_nutrition'][nutrient] += meal['nutrition'][nutrient]

        # Generate snacks
        for i in range(snack_count):
            snack = self._generate_meal(
                available_foods,
                target_calories=calories_per_snack,
                protein_ratio=0.25,  # Moderate protein for snacks
                meal_type=f"Snack {i + 1}"
            )

            # Add to meal plan and update totals
            meal_plan['snacks'].append(snack)
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                meal_plan['total_nutrition'][nutrient] += snack['nutrition'][nutrient]

        # Round the totals for cleaner display
        for nutrient in meal_plan['total_nutrition']:
            meal_plan['total_nutrition'][nutrient] = round(meal_plan['total_nutrition'][nutrient], 1)

        return meal_plan

    def _generate_meal(self,
                       available_foods: pd.DataFrame,
                       target_calories: float,
                       protein_ratio: float = 0.3,
                       meal_type: str = "Meal") -> Dict:
        """
        Generate a single meal or snack

        Args:
            available_foods: DataFrame of foods to select from
            target_calories: Target calories for this meal
            protein_ratio: Desired ratio of protein in the meal
            meal_type: Type of meal (breakfast, lunch, etc.)

        Returns:
            Dictionary with meal information
        """
        # Define food selections based on meal type
        if meal_type == "Breakfast":
            protein_foods = available_foods[
                available_foods['tags'].apply(lambda x: 'breakfast' in x or 'high_protein' in x)]
            carb_foods = available_foods[
                available_foods['tags'].apply(lambda x: 'breakfast' in x or 'whole_grain' in x)]
        elif "Snack" in meal_type:
            protein_foods = available_foods[
                available_foods['tags'].apply(lambda x: 'snack' in x or 'high_protein' in x)]
            carb_foods = available_foods[available_foods['tags'].apply(lambda x: 'snack' in x or 'quick_energy' in x)]
        elif "Post-workout" in meal_type:
            protein_foods = available_foods[available_foods['category'] == 'protein']
            carb_foods = available_foods[
                available_foods['tags'].apply(lambda x: 'quick_energy' in x or 'complex_carbs' in x)]
        else:  # Default for lunch, dinner, etc.
            protein_foods = available_foods[available_foods['category'] == 'protein']
            carb_foods = available_foods[available_foods['category'] == 'carb']

        # Always include some healthy fats and vegetables
        fat_foods = available_foods[available_foods['category'] == 'fat']
        vegetable_foods = available_foods[available_foods['category'] == 'vegetable']

        # Handle empty dataframes (e.g., due to dietary restrictions)
        if protein_foods.empty:
            protein_foods = available_foods[available_foods['protein'] > 5]  # Fallback to any protein-rich food
        if carb_foods.empty:
            carb_foods = available_foods[available_foods['carbs'] > 5]  # Fallback to any carb-rich food
        if fat_foods.empty:
            fat_foods = available_foods[available_foods['fat'] > 3]  # Fallback to any fat-containing food
        if vegetable_foods.empty and 'Snack' not in meal_type:  # Only require veggies for main meals
            vegetable_foods = available_foods.sample(min(3, len(available_foods)))  # Just pick something

        # Initialize meal
        meal = {
            'type': meal_type,
            'foods': [],
            'nutrition': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }
        }

        # Calculate protein target
        protein_target = (target_calories * protein_ratio) / 4  # 4 calories per gram of protein

        # Add a protein source
        if not protein_foods.empty:
            protein_item = protein_foods.sample(1).iloc[0]
            serving_multiplier = (protein_target / protein_item[
                'protein']) * 0.8  # Aim for 80% of protein from main protein source
            serving_multiplier = max(0.5, min(2.0, serving_multiplier))  # Keep servings reasonable

            meal['foods'].append({
                'name': protein_item['name'],
                'servings': round(serving_multiplier, 1),
                'serving_size': protein_item['serving_size'],
                'nutrition': {
                    'calories': round(protein_item['calories'] * serving_multiplier, 1),
                    'protein': round(protein_item['protein'] * serving_multiplier, 1),
                    'carbs': round(protein_item['carbs'] * serving_multiplier, 1),
                    'fat': round(protein_item['fat'] * serving_multiplier, 1)
                }
            })

            # Update meal nutrition
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                meal['nutrition'][nutrient] += meal['foods'][-1]['nutrition'][nutrient]

        # Calculate remaining calories
        remaining_calories = target_calories - meal['nutrition']['calories']

        # Add a carb source if appropriate
        if remaining_calories > 100 and not carb_foods.empty:
            carb_item = carb_foods.sample(1).iloc[0]
            # Target around 40-50% of remaining calories from carbs
            carb_target_calories = remaining_calories * 0.45
            serving_multiplier = carb_target_calories / carb_item['calories']
            serving_multiplier = max(0.5, min(2.0, serving_multiplier))  # Keep servings reasonable

            meal['foods'].append({
                'name': carb_item['name'],
                'servings': round(serving_multiplier, 1),
                'serving_size': carb_item['serving_size'],
                'nutrition': {
                    'calories': round(carb_item['calories'] * serving_multiplier, 1),
                    'protein': round(carb_item['protein'] * serving_multiplier, 1),
                    'carbs': round(carb_item['carbs'] * serving_multiplier, 1),
                    'fat': round(carb_item['fat'] * serving_multiplier, 1)
                }
            })

            # Update meal nutrition
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                meal['nutrition'][nutrient] += meal['foods'][-1]['nutrition'][nutrient]

        # Recalculate remaining calories
        remaining_calories = target_calories - meal['nutrition']['calories']

        # Add a healthy fat source
        if remaining_calories > 50 and not fat_foods.empty:
            fat_item = fat_foods.sample(1).iloc[0]
            # Target around 20-30% of remaining calories from fat
            fat_target_calories = remaining_calories * 0.25
            serving_multiplier = fat_target_calories / fat_item['calories']
            serving_multiplier = max(0.25, min(1.5, serving_multiplier))  # Keep servings reasonable

            meal['foods'].append({
                'name': fat_item['name'],
                'servings': round(serving_multiplier, 1),
                'serving_size': fat_item['serving_size'],
                'nutrition': {
                    'calories': round(fat_item['calories'] * serving_multiplier, 1),
                    'protein': round(fat_item['protein'] * serving_multiplier, 1),
                    'carbs': round(fat_item['carbs'] * serving_multiplier, 1),
                    'fat': round(fat_item['fat'] * serving_multiplier, 1)
                }
            })

            # Update meal nutrition
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                meal['nutrition'][nutrient] += meal['foods'][-1]['nutrition'][nutrient]

        # Add vegetables for main meals
        if 'Snack' not in meal_type and not vegetable_foods.empty:
            veggie = vegetable_foods.sample(1).iloc[0]
            # Standard serving of vegetables
            serving_multiplier = 1.0

            meal['foods'].append({
                'name': veggie['name'],
                'servings': serving_multiplier,
                'serving_size': veggie['serving_size'],
                'nutrition': {
                    'calories': round(veggie['calories'] * serving_multiplier, 1),
                    'protein': round(veggie['protein'] * serving_multiplier, 1),
                    'carbs': round(veggie['carbs'] * serving_multiplier, 1),
                    'fat': round(veggie['fat'] * serving_multiplier, 1)
                }
            })

            # Update meal nutrition
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                meal['nutrition'][nutrient] += meal['foods'][-1]['nutrition'][nutrient]

        return meal

    def generate_weekly_plan(self, user_profile: UserProfile, days: int = 7) -> Dict:
        """
        Generate a complete weekly meal plan

        Args:
            user_profile: UserProfile object with user data
            days: Number of days to generate plan for

        Returns:
            Dictionary with weekly meal plan
        """
        weekly_plan = {
            'user_id': user_profile.user_id,
            'days': [],
            'weekly_nutrition_avg': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }
        }

        # Determine meal structure based on user's goals and preferences
        if user_profile.goal == 'weight_loss':
            meal_count = 3  # Fewer, more structured meals for weight loss
            snack_count = 1
        elif user_profile.goal == 'muscle_gain':
            meal_count = 5  # More frequent meals for muscle gain
            snack_count = 2
        else:  # maintenance
            meal_count = 3
            snack_count = 2

        # Generate each day's plan
        for day in range(1, days + 1):
            # Small day-to-day calorie variation for better adherence
            calorie_adjustment = random.uniform(0.95, 1.05)
            temp_profile = UserProfile(
                user_id=user_profile.user_id,
                age=user_profile.age,
                gender=user_profile.gender,
                height=user_profile.height,
                weight=user_profile.weight,
                goal=user_profile.goal,
                activity_level=user_profile.activity_level,
                dietary_restrictions=user_profile.dietary_restrictions,
                allergies=user_profile.allergies,
                fitness_experience=user_profile.fitness_experience
            )

            # Adjust the target calories with the random factor
            temp_profile.target_calories = user_profile.target_calories * calorie_adjustment

            # Generate the day's meals
            day_plan = self.generate_daily_meals(
                temp_profile,
                meal_count=meal_count,
                snack_count=snack_count
            )

            day_plan['day'] = day
            weekly_plan['days'].append(day_plan)

            # Add to weekly average
            for nutrient in weekly_plan['weekly_nutrition_avg']:
                weekly_plan['weekly_nutrition_avg'][nutrient] += day_plan['total_nutrition'][nutrient] / days

        # Round the averages
        for nutrient in weekly_plan['weekly_nutrition_avg']:
            weekly_plan['weekly_nutrition_avg'][nutrient] = round(weekly_plan['weekly_nutrition_avg'][nutrient], 1)

        return weekly_plan


class WorkoutPlanner:
    """
    Generates personalized workout plans based on user profile and preferences
    """

    def __init__(self, exercise_database: ExerciseDatabase):
        self.exercise_db = exercise_database

    def generate_workout_session(self,
                                 user_profile: UserProfile,
                                 focus: str = None,  # 'upper', 'lower', 'full', 'cardio', 'core', etc.
                                 duration_minutes: int = None) -> Dict:
        """
        Generate a single workout session

        Args:
            user_profile: UserProfile object with user data
            focus: Workout focus area
            duration_minutes: Target workout duration

        Returns:
            Dictionary with workout session details
        """
        # Use profile defaults if not specified
        if duration_minutes is None:
            duration_minutes = user_profile.workout_duration

        # Filter exercises by available equipment
        available_exercises = self.exercise_db.get_exercises_by_equipment(user_profile.available_equipment)

        # Filter by experience level
        if user_profile.fitness_experience == 'beginner':
            difficulty_levels = ['beginner']
        elif user_profile.fitness_experience == 'intermediate':
            difficulty_levels = ['beginner', 'intermediate']
        else:  # advanced
            difficulty_levels = ['beginner', 'intermediate', 'advanced']

        experience_appropriate = available_exercises[available_exercises['difficulty'].isin(difficulty_levels)]

        # Determine workout structure based on focus
        workout = {
            'title': f"{focus.title() if focus else 'Full Body'} Workout",
            'duration_minutes': duration_minutes,
            'warm_up': [],
            'main_exercises': [],
            'cool_down': [],
            'total_exercises': 0
        }

        # Add warm-up
        cardio_exercises = experience_appropriate[experience_appropriate['category'] == 'cardio']
        if not cardio_exercises.empty:
            warm_up_exercise = cardio_exercises.sample(1).iloc[0]
            workout['warm_up'].append({
                'name': warm_up_exercise['name'],
                'sets': 1,
                'time': '5 minutes',
                'intensity': 'Light to moderate',
                'description': warm_up_exercise['description'],
                'instructions': warm_up_exercise['instructions']
            })

        # Add mobility/flexibility warm-up
        flexibility_exercises = experience_appropriate[experience_appropriate['category'] == 'flexibility']
        if not flexibility_exercises.empty:
            mobility_exercise = flexibility_exercises.sample(1).iloc[0]
            workout['warm_up'].append({
                'name': mobility_exercise['name'],
                'sets': 1,
                'time': '3-5 minutes',
                'description': mobility_exercise['description'],
                'instructions': mobility_exercise['instructions']
            })

        # Select main exercises based on focus
        main_duration = duration_minutes - 10  # Subtract warm-up and cool-down time
        exercise_count = main_duration // 5  # Rough estimate - 5 mins per exercise including rest

        if focus == 'upper':
            muscle_groups = ['chest', 'back', 'shoulders', 'arms']
        elif focus == 'lower':
            muscle_groups = ['legs']
        elif focus == 'core':
            muscle_groups = ['core']
        elif focus == 'cardio':
            muscle_groups = ['full body']
            # For cardio, we'll have fewer exercises but longer duration
            exercise_count = max(2, exercise_count // 2)
        else:  # full body or None
            muscle_groups = ['chest', 'back', 'shoulders', 'arms', 'legs', 'core']

        # Select exercises for each target muscle group
        selected_exercises = []

        if focus == 'cardio':
            # For cardio focus, select mostly cardio exercises
            cardio_options = experience_appropriate[experience_appropriate['category'] == 'cardio']
            if not cardio_options.empty:
                selected_cardio = cardio_options.sample(min(exercise_count, len(cardio_options)))
                for _, exercise in selected_cardio.iterrows():
                    selected_exercises.append(exercise)
        else:
            # For strength/mixed workouts, select exercise for each target muscle group
            for muscle_group in muscle_groups:
                group_exercises = experience_appropriate[experience_appropriate['muscle_group'] == muscle_group]
                if not group_exercises.empty:
                    # Select 1-2 exercises per muscle group depending on focus
                    count = 2 if (focus == 'upper' and muscle_group in ['chest', 'back']) or \
                                 (focus == 'lower' and muscle_group == 'legs') or \
                                 (focus == 'core' and muscle_group == 'core') else 1

                    group_selections = group_exercises.sample(min(count, len(group_exercises)))
                    for _, exercise in group_selections.iterrows():
                        selected_exercises.append(exercise)

        # If we didn't get enough exercises, add some general ones
        while len(selected_exercises) < exercise_count:
            # Prioritize strength exercises for non-cardio focuses
            if focus != 'cardio' and not experience_appropriate[experience_appropriate['category'] == 'strength'].empty:
                additional = experience_appropriate[experience_appropriate['category'] == 'strength'].sample(1).iloc[0]
            else:
                # Otherwise just pick something available
                additional = experience_appropriate.sample(1).iloc[0]

            # Check if this exercise is already selected
            if additional['name'] not in [ex['name'] for ex in selected_exercises]:
                selected_exercises.append(additional)

        # Format exercises for the workout
        for exercise in selected_exercises:
            # Determine sets, reps, etc. based on category and experience
            if exercise['category'] == 'cardio':
                if focus == 'cardio':
                    time = '15-20 minutes'
                else:
                    time = '8-10 minutes'

                workout['main_exercises'].append({
                    'name': exercise['name'],
                    'sets': 1,
                    'time': time,
                    'intensity': 'Moderate to high',
                    'category': exercise['category'],
                    'muscle_group': exercise['muscle_group'],
                    'description': exercise['description'],
                    'instructions': exercise['instructions']
                })
            elif exercise['category'] == 'strength':
                # Set structure based on experience and goals
                if user_profile.fitness_experience == 'beginner':
                    sets = 2
                    if exercise['difficulty'] == 'beginner':
                        reps = '12-15'
                    else:
                        reps = '8-12'
                elif user_profile.fitness_experience == 'intermediate':
                    sets = 3
                    if user_profile.goal == 'muscle_gain':
                        reps = '8-12'
                    else:
                        reps = '10-15'
                else:  # advanced
                    sets = 4
                    if user_profile.goal == 'muscle_gain':
                        reps = '6-10'
                    else:
                        reps = '8-15'

                workout['main_exercises'].append({
                    'name': exercise['name'],
                    'sets': sets,
                    'reps': reps,
                    'rest': '60-90 seconds',
                    'category': exercise['category'],
                    'muscle_group': exercise['muscle_group'],
                    'description': exercise['description'],
                    'instructions': exercise['instructions']
                })
            elif exercise['category'] == 'core':
                if user_profile.fitness_experience == 'beginner':
                    sets = 2
                    if exercise['name'] == 'Plank':
                        reps = '20-30 seconds'
                    else:
                        reps = '10-12'
                else:  # intermediate or advanced
                    sets = 3
                    if exercise['name'] == 'Plank':
                        reps = '30-60 seconds'
                    else:
                        reps = '15-20'

                workout['main_exercises'].append({
                    'name': exercise['name'],
                    'sets': sets,
                    'reps': reps,
                    'rest': '45-60 seconds',
                    'category': exercise['category'],
                    'muscle_group': exercise['muscle_group'],
                    'description': exercise['description'],
                    'instructions': exercise['instructions']
                })

        # Add cool-down stretches
        cool_down_stretches = experience_appropriate[experience_appropriate['category'] == 'flexibility']
        if not cool_down_stretches.empty:
            stretch = cool_down_stretches.sample(1).iloc[0]
            workout['cool_down'].append({
                'name': stretch['name'],
                'sets': 1,
                'time': '5 minutes',
                'description': stretch['description'],
                'instructions': stretch['instructions']
            })

        # Update total count
        workout['total_exercises'] = len(workout['main_exercises'])

        return workout

    def generate_weekly_plan(self, user_profile: UserProfile, days: int = None) -> Dict:
        """
        Generate a complete weekly workout plan

        Args:
            user_profile: UserProfile object with user data
            days: Number of workout days (defaults to user preference)

        Returns:
            Dictionary with weekly workout plan
        """
        if days is None:
            days = user_profile.preferred_workout_days

        weekly_plan = {
            'user_id': user_profile.user_id,
            'days_per_week': days,
            'workouts': [],
            'rest_days': 7 - days
        }

        # Determine workout split based on days per week and goals
        if days <= 2:
            # 1-2 days: Full body workouts
            split = ['full'] * days
        elif days == 3:
            if user_profile.goal == 'weight_loss':
                # Weight loss: mix of strength and cardio
                split = ['full', 'cardio', 'full']
            else:
                # Others: push/pull/legs or similar
                split = ['upper', 'lower', 'full']
        elif days == 4:
            if user_profile.goal == 'weight_loss':
                # Weight loss: mix of strength and cardio
                split = ['upper', 'cardio', 'lower', 'cardio']
            else:
                # Others: upper/lower split
                split = ['upper', 'lower', 'upper', 'lower']
        else:  # 5+ days
            if user_profile.goal == 'muscle_gain':
                # Muscle gain: body part split
                split = ['upper', 'lower', 'core', 'upper', 'lower']
                if days > 5:
                    split.extend(['cardio'] * (days - 5))
            else:
                # Others: mix of strength, cardio and recovery
                split = ['upper', 'lower', 'cardio', 'upper', 'lower']
                if days > 5:
                    split.extend(['cardio'] * (days - 5))

        # Generate each workout
        for i, focus in enumerate(split):
            workout = self.generate_workout_session(
                user_profile=user_profile,
                focus=focus,
                duration_minutes=user_profile.workout_duration
            )

            # Add day number
            workout['day'] = i + 1
            weekly_plan['workouts'].append(workout)

        return weekly_plan


class FitnessAI:
    """
    Main AI class that orchestrates personalized fitness recommendations
    """

    def __init__(self, food_db_path: str = None, exercise_db_path: str = None):
        # Initialize databases
        self.food_database = FoodDatabase(food_db_path)
        self.exercise_database = ExerciseDatabase(exercise_db_path)

        # Initialize planners
        self.meal_planner = MealPlanner(self.food_database)
        self.workout_planner = WorkoutPlanner(self.exercise_database)

        # User session storage
        self.user_profiles = {}

    def create_user_profile(self, user_data: Dict) -> UserProfile:
        """
        Create and store a user profile

        Args:
            user_data: Dictionary with user information

        Returns:
            UserProfile object
        """
        profile = UserProfile(
            user_id=user_data.get('user_id', str(len(self.user_profiles) + 1)),
            age=user_data.get('age'),
            gender=user_data.get('gender'),
            height=user_data.get('height'),
            weight=user_data.get('weight'),
            goal=user_data.get('goal', 'maintenance'),
            activity_level=user_data.get('activity_level', 'lightly_active'),
            dietary_restrictions=user_data.get('dietary_restrictions', []),
            allergies=user_data.get('allergies', []),
            fitness_experience=user_data.get('fitness_experience', 'beginner'),
            preferred_workout_days=user_data.get('preferred_workout_days', 3),
            workout_duration=user_data.get('workout_duration', 45),
            available_equipment=user_data.get('available_equipment', ['bodyweight']),
            health_conditions=user_data.get('health_conditions', []),
            favorite_foods=user_data.get('favorite_foods', []),
            disliked_foods=user_data.get('disliked_foods', [])
        )

        # Store the profile
        self.user_profiles[profile.user_id] = profile
        return profile

    def get_user_profile(self, user_id: str) -> UserProfile:
        """Get a user profile by ID"""
        return self.user_profiles.get(user_id)

    def update_user_profile(self, user_id: str, updates: Dict) -> UserProfile:
        """
        Update an existing user profile

        Args:
            user_id: ID of user to update
            updates: Dictionary of fields to update

        Returns:
            Updated UserProfile object
        """
        if user_id not in self.user_profiles:
            raise ValueError(f"User ID {user_id} not found")

        # Get existing profile data
        profile = self.user_profiles[user_id]
        profile_dict = profile.to_dict()

        # Update with new values
        for key, value in updates.items():
            if hasattr(profile, key):
                profile_dict[key] = value

        # Create new profile with updated data
        updated_profile = self.create_user_profile(profile_dict)
        return updated_profile

    def generate_meal_plan(self, user_id: str, days: int = 7) -> Dict:
        """Generate a meal plan for a user"""
        profile = self.get_user_profile(user_id)
        if not profile:
            raise ValueError(f"User ID {user_id} not found")

        return self.meal_planner.generate_weekly_plan(profile, days)

    def generate_workout_plan(self, user_id: str, days: int = None) -> Dict:
        """Generate a workout plan for a user"""
        profile = self.get_user_profile(user_id)
        if not profile:
            raise ValueError(f"User ID {user_id} not found")

        return self.workout_planner.generate_weekly_plan(profile, days)

    def generate_complete_fitness_plan(self, user_id: str, meal_days: int = 7, workout_days: int = None) -> Dict:
        """
        Generate a complete fitness plan including both meals and workouts

        Args:
            user_id: User ID
            meal_days: Number of days for meal plan
            workout_days: Number of days for workout plan (defaults to user preference)

        Returns:
            Complete fitness plan dictionary
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            raise ValueError(f"User ID {user_id} not found")

        meal_plan = self.meal_planner.generate_weekly_plan(profile, meal_days)
        workout_plan = self.workout_planner.generate_weekly_plan(profile, workout_days)

        return {
            'user_id': user_id,
            'user_profile': profile.to_dict(),
            'meal_plan': meal_plan,
            'workout_plan': workout_plan,
            'generation_date': datetime.now().strftime('%Y-%m-%d'),
            'plan_start_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'plan_end_date': (datetime.now() + timedelta(days=meal_days)).strftime('%Y-%m-%d')
        }

    # Web API implementation using Flask


from flask import Flask, request, jsonify, render_template


def create_fitness_api():
    app = Flask(__name__)
    fitness_ai = FitnessAI()

    @app.route('/')
    def home():
        """Render the home page"""
        return render_template('index.html')

    @app.route('/api/user', methods=['POST'])
    def create_user():
        """Create a new user profile"""
        user_data = request.json
        try:
            profile = fitness_ai.create_user_profile(user_data)
            return jsonify({
                'success': True,
                'message': 'User profile created successfully',
                'user_id': profile.user_id,
                'profile': profile.to_dict()
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400

    @app.route('/api/user/<user_id>', methods=['GET'])
    def get_user(user_id):
        """Get a user profile"""
        profile = fitness_ai.get_user_profile(user_id)
        if profile:
            return jsonify({
                'success': True,
                'profile': profile.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'message': f'User ID {user_id} not found'
            }), 404

    @app.route('/api/user/<user_id>', methods=['PUT'])
    def update_user(user_id):
        """Update a user profile"""
        updates = request.json
        try:
            profile = fitness_ai.update_user_profile(user_id, updates)
            return jsonify({
                'success': True,
                'message': 'User profile updated successfully',
                'profile': profile.to_dict()
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400

    @app.route('/api/meal-plan/<user_id>', methods=['GET'])
    def get_meal_plan(user_id):
        """Generate a meal plan for a user"""
        days = request.args.get('days', default=7, type=int)

        try:
            meal_plan = fitness_ai.generate_meal_plan(user_id, days)
            return jsonify({
                'success': True,
                'meal_plan': meal_plan
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400

    @app.route('/api/workout-plan/<user_id>', methods=['GET'])
    def get_workout_plan(user_id):
        """Generate a workout plan for a user"""
        days = request.args.get('days', default=None, type=int)

        try:
            workout_plan = fitness_ai.generate_workout_plan(user_id, days)
            return jsonify({
                'success': True,
                'workout_plan': workout_plan
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400

    @app.route('/api/fitness-plan/<user_id>', methods=['GET'])
    def get_fitness_plan(user_id):
        """Generate a complete fitness plan for a user"""
        meal_days = request.args.get('meal_days', default=7, type=int)
        workout_days = request.args.get('workout_days', default=None, type=int)

        try:
            fitness_plan = fitness_ai.generate_complete_fitness_plan(user_id, meal_days, workout_days)
            return jsonify({
                'success': True,
                'fitness_plan': fitness_plan
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400

    return app