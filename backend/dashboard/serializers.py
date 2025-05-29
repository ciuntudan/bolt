from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, ProgressEntry, WorkoutTemplate, Exercise, 
    WorkoutExercise, UserWorkout, MealPlan, Achievement, UserStreak
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'current_weight', 'target_weight', 'height', 
            'age', 'gender', 'fitness_level', 'goal', 'created_at', 'updated_at'
        ]

class ProgressEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressEntry
        fields = [
            'id', 'date', 'weight', 'strength_score', 
            'body_fat_percentage', 'muscle_mass', 'notes', 'created_at'
        ]

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'muscle_group', 'equipment_needed', 
            'instructions', 'difficulty_level'
        ]

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    
    class Meta:
        model = WorkoutExercise
        fields = [
            'id', 'exercise', 'sets', 'reps_min', 'reps_max', 
            'weight_suggestion', 'rest_time', 'order'
        ]

class WorkoutTemplateSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkoutTemplate
        fields = [
            'id', 'name', 'description', 'muscle_groups', 
            'difficulty_level', 'estimated_duration', 'exercises'
        ]

class UserWorkoutSerializer(serializers.ModelSerializer):
    workout_template = WorkoutTemplateSerializer(read_only=True)
    
    class Meta:
        model = UserWorkout
        fields = [
            'id', 'workout_template', 'scheduled_date', 'completed_date',
            'duration_minutes', 'notes', 'is_completed'
        ]

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = [
            'id', 'date', 'meal_type', 'meal_name', 'foods', 
            'calories', 'protein', 'carbs', 'fat', 
            'scheduled_time', 'is_consumed'
        ]

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            'id', 'title', 'description', 'icon', 'category', 
            'earned_date', 'is_new'
        ]

class UserStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStreak
        fields = ['current_streak', 'longest_streak', 'last_workout_date']

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard overview stats"""
    current_weight = serializers.FloatField()
    target_weight = serializers.FloatField()
    weight_change_percentage = serializers.FloatField()
    strength_score = serializers.IntegerField()
    strength_change_percentage = serializers.FloatField()
    current_streak = serializers.IntegerField()
    total_achievements = serializers.IntegerField()
    new_achievements = serializers.IntegerField()

class DashboardDataSerializer(serializers.Serializer):
    """Main dashboard data serializer"""
    stats = DashboardStatsSerializer()
    progress_data = ProgressEntrySerializer(many=True)
    today_workout = UserWorkoutSerializer(allow_null=True)
    today_meals = MealPlanSerializer(many=True)
    weekly_nutrition = serializers.ListField()
    goals_progress = serializers.DictField()
    recent_achievements = AchievementSerializer(many=True)