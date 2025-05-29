from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    FITNESS_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Required profile fields with defaults
    age = models.PositiveIntegerField(default=18)
    height = models.FloatField(help_text="Height in centimeters", default=170.0)
    weight = models.FloatField(help_text="Weight in kilograms", default=70.0)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='other')
    fitness_level = models.CharField(max_length=50, choices=FITNESS_LEVEL_CHOICES, default='beginner')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class WeightHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_history')
    weight = models.FloatField(help_text="Weight in kilograms")
    body_fat = models.FloatField(help_text="Body fat percentage", null=True, blank=True)
    muscle_mass = models.FloatField(help_text="Muscle mass in kilograms", null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Weight histories"

    def __str__(self):
        return f"{self.user.username}'s weight on {self.date}"

class StrengthProgress(models.Model):
    EXERCISE_CHOICES = [
        ('bench_press', 'Bench Press'),
        ('squat', 'Squat'),
        ('deadlift', 'Deadlift'),
        ('overhead_press', 'Overhead Press'),
        ('barbell_row', 'Barbell Row'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strength_progress')
    exercise = models.CharField(max_length=50, choices=EXERCISE_CHOICES)
    weight = models.FloatField(help_text="Weight in kilograms")
    reps = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Strength progress"

    def __str__(self):
        return f"{self.user.username}'s {self.exercise} on {self.date}"

class WorkoutLog(models.Model):
    INTENSITY_CHOICES = [
        (1, 'Very Light'),
        (2, 'Light'),
        (3, 'Moderate'),
        (4, 'Somewhat Hard'),
        (5, 'Hard'),
        (6, 'Harder'),
        (7, 'Very Hard'),
        (8, 'Extremely Hard'),
        (9, 'Almost Maximum'),
        (10, 'Maximum'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_logs')
    date = models.DateField(auto_now_add=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    intensity = models.PositiveIntegerField(choices=INTENSITY_CHOICES)
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s workout on {self.date}"

class NutritionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutrition_logs')
    date = models.DateField(auto_now_add=True)
    calories = models.PositiveIntegerField()
    protein = models.FloatField(help_text="Protein in grams")
    carbs = models.FloatField(help_text="Carbohydrates in grams")
    fats = models.FloatField(help_text="Fats in grams")
    water = models.FloatField(help_text="Water intake in liters")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s nutrition on {self.date}"

class UserGoal(models.Model):
    GOAL_TYPES = [
        ('weight', 'Weight Goal'),
        ('body_fat', 'Body Fat Percentage Goal'),
        ('muscle_mass', 'Muscle Mass Goal'),
        ('strength', 'Strength Goal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_type = models.CharField(max_length=50, choices=GOAL_TYPES)
    target_value = models.FloatField()
    start_value = models.FloatField()
    start_date = models.DateField(auto_now_add=True)
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.goal_type} goal"

class UserTrainingPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_training_plans')
    name = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.CharField(max_length=50)  
    difficulty = models.CharField(max_length=20)  
    duration_weeks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s {self.name} Training Plan"

class UserTrainingDay(models.Model):
    training_plan = models.ForeignKey(UserTrainingPlan, on_delete=models.CASCADE, related_name='training_days')
    day_of_week = models.IntegerField()  
    name = models.CharField(max_length=100)  
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['day_of_week']

    def __str__(self):
        return f"{self.training_plan.name} - Day {self.day_of_week}"

class UserExercise(models.Model):
    training_day = models.ForeignKey(UserTrainingDay, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.CharField(max_length=50)  
    rest_time = models.IntegerField()  
    notes = models.TextField(blank=True)
    order = models.IntegerField() 

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.sets}x{self.reps})"

class UserMealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meal_plans')
    name = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.CharField(max_length=50) 
    calories_target = models.IntegerField()
    protein_target = models.IntegerField()  
    carbs_target = models.IntegerField()  
    fats_target = models.IntegerField()  
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s {self.name} Meal Plan"

class UserMealTime(models.Model):
    meal_plan = models.ForeignKey(UserMealPlan, on_delete=models.CASCADE, related_name='meal_times')
    name = models.CharField(max_length=50)  
    time = models.TimeField()
    date = models.DateField(null=True, blank=True)
    calories = models.IntegerField()
    protein = models.IntegerField()  
    carbs = models.IntegerField()  
    fats = models.IntegerField()  
    notes = models.TextField(blank=True)
    order = models.IntegerField()  

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.meal_plan.name} - {self.name}"

class UserMealItem(models.Model):
    meal_time = models.ForeignKey(UserMealTime, on_delete=models.CASCADE, related_name='meal_items')
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)  
    calories = models.IntegerField()
    protein = models.FloatField() 
    carbs = models.FloatField()  
    fats = models.FloatField() 
    notes = models.TextField(blank=True)
    order = models.IntegerField()  

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.quantity}{self.unit})"

class TrainingPlan(models.Model):
    GOAL_CHOICES = [
        ('strength', 'Strength'),
        ('hypertrophy', 'Muscle Growth'),
        ('endurance', 'Endurance'),
        ('weight_loss', 'Weight Loss'),
        ('powerlifting', 'Powerlifting'),
        ('crossfit', 'CrossFit Style'),
        ('athletic', 'Athletic Performance'),
        ('rehabilitation', 'Rehabilitation'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('elite', 'Elite'),
    ]
    
    TRAINING_STYLE_CHOICES = [
        ('traditional', 'Traditional'),
        ('supersets', 'Supersets'),
        ('circuit', 'Circuit Training'),
        ('pyramid', 'Pyramid Sets'),
        ('dropsets', 'Drop Sets'),
        ('german_volume', 'German Volume Training'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_plans')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_weeks = models.IntegerField()
    training_style = models.CharField(max_length=20, choices=TRAINING_STYLE_CHOICES, default='traditional')
    equipment_available = models.JSONField(default=list)
    include_deload_weeks = models.BooleanField(default=False)
    experience_years = models.IntegerField(default=0)
    injuries_limitations = models.JSONField(default=list)
    preferred_exercises = models.JSONField(default=list)
    excluded_exercises = models.JSONField(default=list)
    cardio_preferences = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.goal} ({self.difficulty})"

class TrainingWeek(models.Model):
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.training_plan.name} - Week {self.week_number}"

class TrainingDay(models.Model):
    training_week = models.ForeignKey(TrainingWeek, on_delete=models.CASCADE, related_name='workouts')
    day_of_week = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(default=60)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['day_of_week']

    def __str__(self):
        return f"{self.name} - Day {self.day_of_week}"

class Exercise(models.Model):
    training_day = models.ForeignKey(TrainingDay, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=200)
    sets = models.IntegerField()
    reps = models.CharField(max_length=50)  
    weight = models.CharField(max_length=50)  
    notes = models.TextField(blank=True)
    order = models.IntegerField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.sets}x{self.reps}"

class TrainingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_progress')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets_completed = models.IntegerField()
    reps_completed = models.CharField(max_length=50)
    weight_used = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s progress on {self.exercise.name}"

class TrainingAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_type = models.CharField(max_length=50)  
    color_theme = models.CharField(max_length=50)  
    achieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.title} achievement"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()