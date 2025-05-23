from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    """Extended user profile with fitness data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_weight = models.FloatField(help_text="Weight in kgs")
    target_weight = models.FloatField(help_text="Target weight in kgs")
    height = models.FloatField(help_text="Height in cm")
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    fitness_level = models.CharField(
        max_length=20, 
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    goal = models.CharField(
        max_length=20,
        choices=[
            ('weight_loss', 'Weight Loss'),
            ('muscle_gain', 'Muscle Gain'),
            ('maintenance', 'Maintenance')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ProgressEntry(models.Model):
    """Track user's progress over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_entries')
    date = models.DateField()
    weight = models.FloatField(help_text="Weight in kgs")
    strength_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Strength score from 0-100"
    )
    body_fat_percentage = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class WorkoutTemplate(models.Model):
    """Template for workouts"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    muscle_groups = models.CharField(max_length=200, help_text="Comma-separated muscle groups")
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    """Individual exercises"""
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=50)
    equipment_needed = models.CharField(max_length=100, blank=True)
    instructions = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )

    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    """Exercises within a workout template"""
    workout = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps_min = models.IntegerField()
    reps_max = models.IntegerField()
    weight_suggestion = models.FloatField(null=True, blank=True, help_text="Suggested weight in kgs")
    rest_time = models.IntegerField(help_text="Rest time in seconds")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.workout.name} - {self.exercise.name}"

class UserWorkout(models.Model):
    """User's scheduled/completed workouts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    workout_template = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    completed_date = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'scheduled_date')

    def __str__(self):
        return f"{self.user.username} - {self.workout_template.name} - {self.scheduled_date}"

class MealPlan(models.Model):
    """User's meal plans"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    date = models.DateField()
    meal_type = models.CharField(
        max_length=20,
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('snack', 'Snack')
        ]
    )
    meal_name = models.CharField(max_length=100)
    foods = models.JSONField(help_text="List of foods in the meal")
    calories = models.IntegerField()
    protein = models.FloatField(help_text="Protein in grams")
    carbs = models.FloatField(help_text="Carbohydrates in grams")
    fat = models.FloatField(help_text="Fat in grams")
    scheduled_time = models.TimeField()
    is_consumed = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'scheduled_time']

    def __str__(self):
        return f"{self.user.username} - {self.meal_name} - {self.date}"

class Achievement(models.Model):
    """User achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    category = models.CharField(
        max_length=20,
        choices=[
            ('workout', 'Workout'),
            ('nutrition', 'Nutrition'),
            ('progress', 'Progress'),
            ('consistency', 'Consistency')
        ]
    )
    earned_date = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)

    class Meta:
        ordering = ['-earned_date']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class UserStreak(models.Model):
    """Track user's workout streaks"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_workout_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"