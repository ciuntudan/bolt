from django.contrib import admin
from .models import (
    UserProfile, ProgressEntry, WorkoutTemplate, Exercise, 
    WorkoutExercise, UserWorkout, MealPlan, Achievement, UserStreak
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_weight', 'target_weight', 'goal', 'fitness_level']
    list_filter = ['goal', 'fitness_level', 'gender']
    search_fields = ['user__username', 'user__email']

@admin.register(ProgressEntry)
class ProgressEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight', 'strength_score']
    list_filter = ['date']
    search_fields = ['user__username']
    ordering = ['-date']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'muscle_group', 'difficulty_level']
    list_filter = ['muscle_group', 'difficulty_level']
    search_fields = ['name', 'muscle_group']

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

@admin.register(WorkoutTemplate)
class WorkoutTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty_level', 'estimated_duration']
    list_filter = ['difficulty_level']
    search_fields = ['name', 'muscle_groups']
    inlines = [WorkoutExerciseInline]

@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout_template', 'scheduled_date', 'is_completed']
    list_filter = ['is_completed', 'scheduled_date']
    search_fields = ['user__username', 'workout_template__name']
    ordering = ['-scheduled_date']

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'meal_type', 'meal_name', 'calories']
    list_filter = ['meal_type', 'date', 'is_consumed']
    search_fields = ['user__username', 'meal_name']
    ordering = ['-date', 'scheduled_time']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'category', 'earned_date', 'is_new']
    list_filter = ['category', 'is_new', 'earned_date']
    search_fields = ['user__username', 'title']
    ordering = ['-earned_date']

@admin.register(UserStreak)
class UserStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_workout_date']
    search_fields = ['user__username']
    ordering = ['-current_streak']