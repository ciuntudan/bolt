
from rest_framework import serializers
from .models import (
    TrainingPlan, TrainingWeek, Workout, Exercise, WorkoutExercise, 
    WorkoutSession, ExerciseSet, UserAchievement
)

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'exercise_type', 'primary_muscle_group', 
                 'secondary_muscle_groups', 'instructions', 'tips']

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    exercise_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'exercise_id', 'order', 'sets', 'reps', 'weight', 
                 'rest_time', 'notes', 'completed', 'completed_sets']

class ExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ['id', 'set_number', 'reps', 'weight', 'duration', 'completed', 'created_at']

class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercise_sets = ExerciseSetSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkoutSession
        fields = ['id', 'started_at', 'ended_at', 'duration', 'notes', 'exercise_sets']

class WorkoutDetailSerializer(serializers.ModelSerializer):
    workout_exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    sessions = WorkoutSessionSerializer(many=True, read_only=True)
    completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Workout
        fields = ['id', 'day_of_week', 'title', 'description', 'estimated_duration', 
                 'completed', 'completed_at', 'actual_duration', 'workout_exercises', 
                 'sessions', 'completion_percentage']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'day_of_week', 'title', 'description', 'estimated_duration', 
                 'completed', 'completed_at', 'actual_duration', 'exercises']
    
    def get_exercises(self, obj):
        workout_exercises = obj.workout_exercises.all()
        exercises = []
        for we in workout_exercises:
            exercises.append({
                'name': we.exercise.name,
                'sets': we.sets,
                'reps': we.reps,
                'weight': we.weight,
                'completed': we.completed
            })
        return exercises

class TrainingWeekSerializer(serializers.ModelSerializer):
    workouts = WorkoutSerializer(many=True, read_only=True)
    completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = TrainingWeek
        fields = ['id', 'week_number', 'name', 'is_completed', 'workouts', 'completion_percentage']

class TrainingPlanSerializer(serializers.ModelSerializer):
    weeks = TrainingWeekSerializer(many=True, read_only=True)
    completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = TrainingPlan
        fields = ['id', 'name', 'description', 'plan_type', 'total_weeks', 'current_week', 
                 'is_active', 'created_at', 'updated_at', 'weeks', 'completion_percentage']

class TrainingPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlan
        fields = ['name', 'description', 'plan_type', 'total_weeks']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement_type', 'title', 'description', 'icon_color', 'earned_at']

class WorkoutStatsSerializer(serializers.Serializer):
    weekly_workouts_completed = serializers.IntegerField()
    weekly_workouts_total = serializers.IntegerField()
    weekly_completion_rate = serializers.FloatField()
    volume_progress = serializers.FloatField()
    program_adherence = serializers.FloatField()
    current_streak = serializers.IntegerField()
    total_workouts_completed = serializers.IntegerField()

class StartWorkoutSerializer(serializers.Serializer):
    workout_id = serializers.IntegerField()

class CompleteWorkoutSerializer(serializers.Serializer):
    workout_id = serializers.IntegerField()
    duration = serializers.IntegerField(help_text="Duration in seconds")
    notes = serializers.CharField(required=False, allow_blank=True)

class CompleteExerciseSerializer(serializers.Serializer):
    workout_exercise_id = serializers.IntegerField()
    sets_completed = serializers.IntegerField()

class LogExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ['workout_exercise', 'set_number', 'reps', 'weight', 'duration', 'completed']
    
    def create(self, validated_data):
        # Get or create the current workout session
        request = self.context['request']
        workout_exercise = validated_data['workout_exercise']
        workout = workout_exercise.workout
        
        session, created = WorkoutSession.objects.get_or_create(
            user=request.user,
            workout=workout,
            ended_at__isnull=True,
            defaults={'started_at': timezone.now()}
        )
        
        validated_data['session'] = session
        return super().create(validated_data)