from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import (
    UserProfile, WeightHistory, StrengthProgress, WorkoutLog,
    NutritionLog, UserGoal, UserTrainingPlan, UserTrainingDay, UserExercise,
    UserMealPlan, UserMealTime, UserMealItem, TrainingPlan, TrainingWeek, 
    TrainingDay, Exercise, TrainingProgress, TrainingAchievement
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'age', 'height', 'weight', 'gender', 'fitness_level']
        extra_kwargs = {
            'age': {'min_value': 13, 'max_value': 120},
            'height': {'min_value': 100, 'max_value': 250},
            'weight': {'min_value': 30, 'max_value': 300},
        }

    def to_representation(self, instance):
        """Handle default values for null fields"""
        data = super().to_representation(instance)
        
       
        if data['age'] is None:
            data['age'] = 18
        if data['height'] is None:
            data['height'] = 170.0
        if data['weight'] is None:
            data['weight'] = 70.0
        if data['gender'] is None:
            data['gender'] = 'other'
        if data['fitness_level'] is None:
            data['fitness_level'] = 'beginner'
        if data['avatar'] is None:
            data['avatar'] = None  
            
        return data

    def validate(self, data):
        """Additional validation for profile data"""
        if 'age' in data and (data['age'] < 13 or data['age'] > 120):
            raise serializers.ValidationError({'age': 'Age must be between 13 and 120'})
            
        if 'height' in data and (data['height'] < 100 or data['height'] > 250):
            raise serializers.ValidationError({'height': 'Height must be between 100 and 250 cm'})
            
        if 'weight' in data and (data['weight'] < 30 or data['weight'] > 300):
            raise serializers.ValidationError({'weight': 'Weight must be between 30 and 300 kg'})
            
        return data

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    # Profile fields
    age = serializers.IntegerField(required=True, min_value=13, max_value=120)
    height = serializers.FloatField(required=True, min_value=100, max_value=250)
    weight = serializers.FloatField(required=True, min_value=30, max_value=300)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True)
    fitness_level = serializers.ChoiceField(choices=UserProfile.FITNESS_LEVEL_CHOICES, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2',
            'age', 'height', 'weight', 'gender', 'fitness_level'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email already in use."})
            
        return attrs

    def create(self, validated_data):
        try:
            from django.db import transaction
            with transaction.atomic():
                # Extract profile data
                profile_data = {
                    'age': validated_data.pop('age'),
                    'height': validated_data.pop('height'),
                    'weight': validated_data.pop('weight'),
                    'gender': validated_data.pop('gender'),
                    'fitness_level': validated_data.pop('fitness_level'),
                }
                validated_data.pop('password2')
                
                # Create user
                password = validated_data.pop('password')
                user = User.objects.create_user(
                    **validated_data,
                    password=password
                )
                
                # The signal will have created the profile, now we just update it
                profile = UserProfile.objects.get(user=user)
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.save()
                
                return user
        except Exception as e:
            raise serializers.ValidationError(str(e))

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class WeightHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightHistory
        fields = ('id', 'weight', 'body_fat', 'muscle_mass', 'date', 'notes')
        read_only_fields = ('id', 'date')

class StrengthProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrengthProgress
        fields = ('id', 'exercise', 'weight', 'reps', 'sets', 'date', 'notes')
        read_only_fields = ('id', 'date')

class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = ('id', 'date', 'duration', 'intensity', 'calories_burned', 'notes')
        read_only_fields = ('id', 'date')

class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = ('id', 'date', 'calories', 'protein', 'carbs', 'fats', 'water', 'notes')
        read_only_fields = ('id', 'date')

class UserGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = UserGoal
        fields = ('id', 'goal_type', 'target_value', 'start_value', 'start_date',
                 'target_date', 'achieved', 'notes', 'progress_percentage')
        read_only_fields = ('id', 'start_date', 'progress_percentage')
    
    def get_progress_percentage(self, obj):
        if obj.goal_type == 'weight':
            latest_weight = WeightHistory.objects.filter(user=obj.user).order_by('-date').first()
            if latest_weight:
                total_change = obj.target_value - obj.start_value
                current_change = latest_weight.weight - obj.start_value
                if total_change != 0:
                    return min(100, max(0, (current_change / total_change) * 100))
        return 0

class ProgressSummarySerializer(serializers.Serializer):
    weight_change = serializers.FloatField()
    strength_increase = serializers.FloatField()
    workout_consistency = serializers.FloatField()
    goal_progress = serializers.FloatField()
    recent_achievements = serializers.ListField(child=serializers.DictField())
    body_metrics = serializers.ListField(child=serializers.DictField())
    strength_metrics = serializers.ListField(child=serializers.DictField())
    workout_metrics = serializers.ListField(child=serializers.DictField())
    nutrition_metrics = serializers.ListField(child=serializers.DictField())

class UserExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExercise
        fields = ['id', 'name', 'sets', 'reps', 'rest_time', 'notes', 'order']

class UserTrainingDaySerializer(serializers.ModelSerializer):
    exercises = UserExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = UserTrainingDay
        fields = ['id', 'day_of_week', 'name', 'notes', 'exercises']

class UserTrainingPlanSerializer(serializers.ModelSerializer):
    training_days = UserTrainingDaySerializer(many=True, read_only=True)

    class Meta:
        model = UserTrainingPlan
        fields = [
            'id', 'name', 'description', 'goal', 'difficulty',
            'duration_weeks', 'created_at', 'updated_at',
            'is_active', 'training_days'
        ]

class UserMealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMealItem
        fields = [
            'id', 'name', 'quantity', 'unit', 'calories',
            'protein', 'carbs', 'fats', 'notes', 'order'
        ]

class UserMealTimeSerializer(serializers.ModelSerializer):
    meal_items = UserMealItemSerializer(many=True, read_only=True)

    class Meta:
        model = UserMealTime
        fields = [
            'id', 'name', 'time', 'date', 'calories', 'protein',
            'carbs', 'fats', 'notes', 'order', 'meal_items'
        ]

class UserMealPlanSerializer(serializers.ModelSerializer):
    meal_times = UserMealTimeSerializer(many=True, read_only=True)

    class Meta:
        model = UserMealPlan
        fields = [
            'id', 'name', 'description', 'goal',
            'calories_target', 'protein_target', 'carbs_target',
            'fats_target', 'created_at', 'updated_at',
            'is_active', 'meal_times', 'start_date', 'end_date'
        ]

# Serializers for creating nested objects
class UserExerciseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExercise
        fields = ['name', 'sets', 'reps', 'rest_time', 'notes', 'order']

class UserTrainingDayCreateSerializer(serializers.ModelSerializer):
    exercises = UserExerciseCreateSerializer(many=True)

    class Meta:
        model = UserTrainingDay
        fields = ['day_of_week', 'name', 'notes', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        training_day = UserTrainingDay.objects.create(**validated_data)
        
        for exercise_data in exercises_data:
            UserExercise.objects.create(training_day=training_day, **exercise_data)
        
        return training_day

class UserTrainingPlanCreateSerializer(serializers.ModelSerializer):
    training_days = UserTrainingDayCreateSerializer(many=True)

    class Meta:
        model = UserTrainingPlan
        fields = [
            'name', 'description', 'goal', 'difficulty',
            'duration_weeks', 'is_active', 'training_days'
        ]

    def create(self, validated_data):
        training_days_data = validated_data.pop('training_days')
        training_plan = UserTrainingPlan.objects.create(**validated_data)
        
        for day_data in training_days_data:
            exercises_data = day_data.pop('exercises')
            training_day = UserTrainingDay.objects.create(training_plan=training_plan, **day_data)
            
            for exercise_data in exercises_data:
                UserExercise.objects.create(training_day=training_day, **exercise_data)
        
        return training_plan

class UserMealItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMealItem
        fields = ['name', 'quantity', 'unit', 'calories', 'protein', 'carbs', 'fats', 'notes', 'order']

class UserMealTimeCreateSerializer(serializers.ModelSerializer):
    meal_items = UserMealItemCreateSerializer(many=True)

    class Meta:
        model = UserMealTime
        fields = ['name', 'time', 'date', 'calories', 'protein', 'carbs', 'fats', 'notes', 'order', 'meal_items']

    def create(self, validated_data):
        meal_items_data = validated_data.pop('meal_items')
        meal_time = UserMealTime.objects.create(**validated_data)
        
        for item_data in meal_items_data:
            UserMealItem.objects.create(meal_time=meal_time, **item_data)
        
        return meal_time

class UserMealPlanCreateSerializer(serializers.ModelSerializer):
    meal_times = UserMealTimeCreateSerializer(many=True)

    class Meta:
        model = UserMealPlan
        fields = [
            'name', 'description', 'goal', 'calories_target',
            'protein_target', 'carbs_target', 'fats_target',
            'is_active', 'meal_times', 'start_date', 'end_date'
        ]

    def create(self, validated_data):
        meal_times_data = validated_data.pop('meal_times')
        meal_plan = UserMealPlan.objects.create(**validated_data)
        
        for time_data in meal_times_data:
            meal_items_data = time_data.pop('meal_items')
            meal_time = UserMealTime.objects.create(meal_plan=meal_plan, **time_data)
            
            for item_data in meal_items_data:
                UserMealItem.objects.create(meal_time=meal_time, **item_data)
        
        return meal_plan

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'sets', 'reps', 'weight', 'notes', 'order', 'completed']

class TrainingDaySerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = TrainingDay
        fields = [
            'id', 'day_of_week', 'name', 'description', 
            'duration_minutes', 'exercises', 'completed', 
            'completed_at'
        ]
        read_only_fields = ['completed', 'completed_at']

class TrainingWeekSerializer(serializers.ModelSerializer):
    workouts = TrainingDaySerializer(many=True, read_only=True)
    
    class Meta:
        model = TrainingWeek
        fields = ['id', 'week_number', 'name', 'description', 'workouts']

class TrainingPlanSerializer(serializers.ModelSerializer):
    weeks = TrainingWeekSerializer(many=True, read_only=True)
    
    class Meta:
        model = TrainingPlan
        fields = [
            'id', 'name', 'description', 'goal', 'difficulty',
            'duration_weeks', 'weeks', 'created_at', 'updated_at',
            'training_style', 'equipment_available', 'include_deload_weeks',
            'experience_years', 'injuries_limitations', 'preferred_exercises',
            'excluded_exercises', 'cardio_preferences'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_equipment_available(self, value):
        valid_equipment = [
            'barbell', 'dumbbell', 'cables', 'bodyweight',
            'machines', 'kettlebell', 'resistance_bands'
        ]
        if not all(item in valid_equipment for item in value):
            raise serializers.ValidationError("Invalid equipment type")
        return value

    def validate_injuries_limitations(self, value):
        valid_limitations = [
            'shoulder', 'knee', 'back', 'hip', 'wrist', 'ankle'
        ]
        if not all(item in valid_limitations for item in value):
            raise serializers.ValidationError("Invalid injury/limitation type")
        return value

    def validate_cardio_preferences(self, value):
        valid_types = ['running', 'cycling', 'rowing', 'swimming', 'hiit', 'walking']
        if 'type' in value and not all(t in valid_types for t in value['type']):
            raise serializers.ValidationError("Invalid cardio type")
        if 'duration' in value and not isinstance(value['duration'], int):
            raise serializers.ValidationError("Duration must be an integer")
        if 'frequency' in value and not isinstance(value['frequency'], int):
            raise serializers.ValidationError("Frequency must be an integer")
        return value

class TrainingProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgress
        fields = ['id', 'exercise', 'sets_completed', 'reps_completed', 'weight_used', 'notes', 'date']

class TrainingAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingAchievement
        fields = ['id', 'title', 'description', 'icon_type', 'color_theme', 'achieved_at']

# Serializer for creating a new training plan
class TrainingPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlan
        fields = ['goal', 'difficulty', 'duration_weeks']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['name'] = f"{validated_data['goal'].title()} Training Plan"
        validated_data['description'] = f"A {validated_data['duration_weeks']}-week {validated_data['difficulty']} level training plan for {validated_data['goal']}"
        return super().create(validated_data)