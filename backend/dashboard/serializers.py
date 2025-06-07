from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ProgressEntry, WorkoutTemplate, UserWorkout, 
    MealPlan, Achievement, UserStreak
)
from users.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'weight', 'target_weight', 'height', 
            'age', 'gender', 'fitness_level', 'avatar',
            'workout_frequency', 'workout_duration', 'activity_level',
            'stress_level', 'preferred_workout_time', 'allergies',
            'medical_conditions', 'medications', 'injuries',
            'updated_at'
        ]

class ProgressEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressEntry
        fields = '__all__'

class WorkoutTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate
        fields = '__all__'

class UserWorkoutSerializer(serializers.ModelSerializer):
    workout_template = WorkoutTemplateSerializer()
    
    class Meta:
        model = UserWorkout
        fields = '__all__'

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class UserStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStreak
        fields = '__all__'

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard overview stats"""
    current_weight = serializers.FloatField()
    target_weight = serializers.FloatField()
    weight_change = serializers.FloatField()
    strength_score = serializers.FloatField()
    strength_change = serializers.FloatField()
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