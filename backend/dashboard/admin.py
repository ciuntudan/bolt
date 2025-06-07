from django.contrib import admin
from .models import (
    ProgressEntry, WorkoutTemplate, UserWorkout, 
    MealPlan, Achievement, UserStreak
)

@admin.register(ProgressEntry)
class ProgressEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight', 'strength_score')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'notes')

@admin.register(WorkoutTemplate)
class WorkoutTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_groups', 'difficulty_level', 'estimated_duration')
    list_filter = ('difficulty_level', 'muscle_groups')
    search_fields = ('name', 'description')

@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_template', 'scheduled_date', 'completed_date', 'is_completed')
    list_filter = ('user', 'is_completed', 'scheduled_date')
    search_fields = ('user__username', 'workout_template__name', 'notes')

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'meal_type', 'calories', 'protein', 'carbs', 'fat')
    list_filter = ('user', 'date', 'meal_type')
    search_fields = ('user__username', 'meal_name', 'foods')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'earned_date', 'is_new')
    list_filter = ('category', 'earned_date', 'is_new')
    search_fields = ('user__username', 'title', 'description')

@admin.register(UserStreak)
class UserStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'longest_streak', 'last_workout_date')
    list_filter = ('user', 'last_workout_date')
    search_fields = ('user__username',)