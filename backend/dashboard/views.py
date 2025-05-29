from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import (
    UserProfile, ProgressEntry, WorkoutTemplate, UserWorkout, 
    MealPlan, Achievement, UserStreak
)
from .serializers import (
    UserProfileSerializer, ProgressEntrySerializer, WorkoutTemplateSerializer,
    UserWorkoutSerializer, MealPlanSerializer, AchievementSerializer,
    DashboardDataSerializer, UserStreakSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """
    Get comprehensive dashboard data for the authenticated user
    """
    user = request.user
    today = date.today()
    
    try:
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'current_weight': 70.0,
                'target_weight': 75.0,
                'height': 175.0,
                'age': 25,
                'gender': 'male',
                'fitness_level': 'intermediate',
                'goal': 'muscle_gain'
            }
        )
        
        # Get latest progress entries
        latest_progress = ProgressEntry.objects.filter(user=user).first()
        week_ago_progress = ProgressEntry.objects.filter(
            user=user, 
            date__lte=today - timedelta(days=7)
        ).first()
        
        # Calculate progress stats
        current_weight = latest_progress.weight if latest_progress else profile.current_weight
        current_strength = latest_progress.strength_score if latest_progress else 50
        
        weight_change = 0
        strength_change = 0
        
        if week_ago_progress:
            if week_ago_progress.weight > 0:
                weight_change = ((current_weight - week_ago_progress.weight) / week_ago_progress.weight) * 100
            if week_ago_progress.strength_score > 0:
                strength_change = ((current_strength - week_ago_progress.strength_score) / week_ago_progress.strength_score) * 100
        
        # Get streak info
        streak, _ = UserStreak.objects.get_or_create(
            user=user,
            defaults={'current_streak': 0, 'longest_streak': 0}
        )
        
        # Calculate training stats
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        weekly_workouts = UserWorkout.objects.filter(
            user=user,
            scheduled_date__range=[week_start, week_end]
        )
        
        weekly_workouts_completed = weekly_workouts.filter(is_completed=True).count()
        weekly_workouts_total = weekly_workouts.count()
        
        # Calculate volume progress
        thirty_days_ago = today - timedelta(days=30)
        completed_volume = UserWorkout.objects.filter(
            user=user,
            scheduled_date__gte=thirty_days_ago,
            is_completed=True
        ).count()
        
        total_volume = UserWorkout.objects.filter(
            user=user,
            scheduled_date__gte=thirty_days_ago
        ).count()
        
        volume_progress = (completed_volume / max(1, total_volume)) * 100 if total_volume > 0 else 0
        
        # Calculate program adherence
        adherence = UserWorkout.objects.filter(
            user=user,
            scheduled_date__gte=thirty_days_ago,
            is_completed=True
        ).count()
        
        total_scheduled = UserWorkout.objects.filter(
            user=user,
            scheduled_date__gte=thirty_days_ago
        ).count()
        
        program_adherence = (adherence / max(1, total_scheduled)) * 100 if total_scheduled > 0 else 0
        
        # Get training stats
        training_stats = {
            'weekly_workouts_completed': weekly_workouts_completed,
            'weekly_workouts_total': weekly_workouts_total,
            'volume_progress_percentage': round(volume_progress),
            'program_adherence_percentage': round(program_adherence),
            'current_streak': streak.current_streak
        }
        
        # Get achievements with types based on criteria
        achievements = []
        
        # Streak achievement
        if streak.current_streak >= 7:
            achievements.append({
                'id': len(achievements) + 1,
                'title': 'Consistency Champion',
                'description': f'{streak.current_streak} day workout streak!',
                'date': today.isoformat(),
                'type': 'gold'
            })
            
        # Volume achievement
        if volume_progress >= 80:
            achievements.append({
                'id': len(achievements) + 1,
                'title': 'Volume Master',
                'description': 'Completed over 80% of planned volume',
                'date': today.isoformat(),
                'type': 'silver'
            })
            
        # Adherence achievement
        if program_adherence >= 90:
            achievements.append({
                'id': len(achievements) + 1,
                'title': 'Program Dedication',
                'description': 'Over 90% program adherence',
                'date': today.isoformat(),
                'type': 'bronze'
            })
        
        # Get recent workouts
        recent_workouts = UserWorkout.objects.filter(
            user=user,
            scheduled_date__lte=today
        ).order_by('-scheduled_date')[:5]
        
        # Get today s workout
        today_workout = UserWorkout.objects.filter(
            user=user,
            scheduled_date=today
        ).first()
        
        # Get today s meals
        today_meals = MealPlan.objects.filter(
            user=user,
            date=today
        ).order_by('scheduled_time')
        
        # Get weekly nutrition data
        week_start = today - timedelta(days=today.weekday())
        weekly_nutrition = []
        
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_meals = MealPlan.objects.filter(user=user, date=day)
            
            daily_calories = sum(meal.calories for meal in day_meals)
            daily_protein = sum(meal.protein for meal in day_meals)
            daily_carbs = sum(meal.carbs for meal in day_meals)
            daily_fat = sum(meal.fat for meal in day_meals)
            
            weekly_nutrition.append({
                'name': day.strftime('%a'),
                'calories': daily_calories,
                'protein': daily_protein,
                'carbs': daily_carbs,
                'fat': daily_fat
            })
        
        # Prepare dashboard data
        dashboard_data = {
            'weight_change': weight_change,
            'strength_increase': strength_change,
            'workout_consistency': program_adherence,
            'goal_progress': volume_progress,
            'training_stats': training_stats,
            'recent_achievements': achievements,
            'body_metrics': ProgressEntrySerializer(latest_progress).data,
            'strength_metrics': [],  # Add strength metrics if available
            'workout_metrics': [{
                'date': workout.scheduled_date.isoformat(),
                'duration': workout.duration_minutes,
                'intensity': workout.intensity,
                'calories_burned': workout.calories_burned
            } for workout in recent_workouts],
            'nutrition_metrics': weekly_nutrition,
            'today_workout': UserWorkoutSerializer(today_workout).data if today_workout else None,
            'today_meals': MealPlanSerializer(today_meals, many=True).data
        }
        
        return Response(dashboard_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch dashboard data: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get or update user profile
    """
    try:
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'current_weight': 70.0,
                'target_weight': 75.0,
                'height': 175.0,
                'age': 25,
                'gender': 'male',
                'fitness_level': 'intermediate',
                'goal': 'muscle_gain'
            }
        )
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': f'Profile operation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class ProgressEntryListCreateView(generics.ListCreateAPIView):
    """
    List all progress entries for user or create a new one
    """
    serializer_class = ProgressEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProgressEntry.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutTemplateListView(generics.ListAPIView):
    """
    List all available workout templates
    """
    queryset = WorkoutTemplate.objects.all()
    serializer_class = WorkoutTemplateSerializer
    permission_classes = [IsAuthenticated]

class UserWorkoutListCreateView(generics.ListCreateAPIView):
    """
    List user's workouts or create/schedule a new one
    """
    serializer_class = UserWorkoutSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserWorkout.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_workout(request, workout_id):
    """
    Mark a workout as completed
    """
    try:
        workout = UserWorkout.objects.get(id=workout_id, user=request.user)
        workout.is_completed = True
        workout.completed_date = timezone.now()
        workout.duration_minutes = request.data.get('duration_minutes', 0)
        workout.notes = request.data.get('notes', '')
        workout.save()
      
        streak, _ = UserStreak.objects.get_or_create(user=request.user)
        today = date.today()
        
        if streak.last_workout_date == today - timedelta(days=1):
            streak.current_streak += 1
        elif streak.last_workout_date != today:
            streak.current_streak = 1
        
        streak.last_workout_date = today
        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        streak.save()
        
        return Response({'message': 'Workout completed successfully'})
        
    except UserWorkout.DoesNotExist:
        return Response(
            {'error': 'Workout not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to complete workout: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class MealPlanListCreateView(generics.ListCreateAPIView):
    """
    List user's meal plans or create a new one
    """
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        date_filter = self.request.query_params.get('date')
        queryset = MealPlan.objects.filter(user=self.request.user)
        
        if date_filter:
            queryset = queryset.filter(date=date_filter)
        
        return queryset.order_by('date', 'scheduled_time')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AchievementListView(generics.ListAPIView):
    """
    List user's achievements
    """
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_achievements_read(request):
    """
    Mark achievements as read (not new)
    """
    try:
        Achievement.objects.filter(user=request.user, is_new=True).update(is_new=False)
        return Response({'message': 'Achievements marked as read'})
    except Exception as e:
        return Response(
            {'error': f'Failed to mark achievements: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )