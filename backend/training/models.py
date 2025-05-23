from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TrainingPlan(models.Model):
    PLAN_TYPES = [
        ('strength', 'Strength Training'),
        ('hypertrophy', 'Muscle Building'),
        ('endurance', 'Endurance'),
        ('powerlifting', 'Powerlifting'),
        ('bodybuilding', 'Bodybuilding'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_plans')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='strength')
    total_weeks = models.IntegerField(default=8, validators=[MinValueValidator(1), MaxValueValidator(52)])
    current_week = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    @property
    def completion_percentage(self):
        total_workouts = self.weeks.aggregate(
            total=models.Count('workouts')
        )['total'] or 0
        
        completed_workouts = self.weeks.aggregate(
            completed=models.Count('workouts', filter=models.Q(workouts__completed=True))
        )['completed'] or 0
        
        if total_workouts == 0:
            return 0
        return round((completed_workouts / total_workouts) * 100, 1)

class TrainingWeek(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.IntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['week_number']
        unique_together = ['plan', 'week_number']
    
    def __str__(self):
        return f"{self.plan.name} - Week {self.week_number}"
    
    @property
    def completion_percentage(self):
        total_workouts = self.workouts.count()
        if total_workouts == 0:
            return 0
        completed_workouts = self.workouts.filter(completed=True).count()
        return round((completed_workouts / total_workouts) * 100, 1)

class Workout(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    week = models.ForeignKey(TrainingWeek, on_delete=models.CASCADE, related_name='workouts')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    actual_duration = models.IntegerField(null=True, blank=True, help_text="Actual duration in seconds")
    
    class Meta:
        ordering = ['day_of_week']
        unique_together = ['week', 'day_of_week']
    
    def __str__(self):
        return f"{self.week} - {self.get_day_of_week_display()}: {self.title}"
    
    @property
    def completion_percentage(self):
        total_exercises = self.exercises.count()
        if total_exercises == 0:
            return 0
        completed_exercises = self.workout_exercises.filter(completed=True).count()
        return round((completed_exercises / total_exercises) * 100, 1)

class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('compound', 'Compound'),
        ('isolation', 'Isolation'),
        ('cardio', 'Cardio'),
        ('stretching', 'Stretching'),
        ('mobility', 'Mobility'),
    ]
    
    MUSCLE_GROUPS = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('shoulders', 'Shoulders'),
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('core', 'Core'),
        ('glutes', 'Glutes'),
        ('full_body', 'Full Body'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES, default='compound')
    primary_muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUPS)
    secondary_muscle_groups = models.JSONField(default=list, blank=True)
    instructions = models.TextField(blank=True)
    tips = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    sets = models.IntegerField(validators=[MinValueValidator(1)])
    reps = models.CharField(max_length=50, help_text="e.g., '8-10', '12', 'AMRAP'")
    weight = models.CharField(max_length=50, blank=True, help_text="e.g., '135 lbs', 'Bodyweight'")
    rest_time = models.IntegerField(default=60, help_text="Rest time in seconds")
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    completed_sets = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        unique_together = ['workout', 'exercise']
    
    def __str__(self):
        return f"{self.workout.title} - {self.exercise.name}"

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_sessions')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.workout.title} - {self.started_at.date()}"

class ExerciseSet(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercise_sets')
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    set_number = models.IntegerField()
    reps = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds for time-based exercises")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['set_number']
        unique_together = ['session', 'workout_exercise', 'set_number']
    
    def __str__(self):
        return f"{self.session} - {self.workout_exercise.exercise.name} - Set {self.set_number}"

class UserAchievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('consistency', 'Consistency'),
        ('weight_milestone', 'Weight Milestone'),
        ('volume', 'Volume'),
        ('streak', 'Streak'),
        ('first_time', 'First Time'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_color = models.CharField(max_length=20, default='blue')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"