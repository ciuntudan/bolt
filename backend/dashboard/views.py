from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q
from django.db.models.functions import TruncDate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from datetime import timedelta, date, datetime
from .models import (
    ProgressEntry, WorkoutTemplate, UserWorkout, 
    MealPlan, Achievement, UserStreak
)
from users.models import WeightHistory, UserProfile, TrainingDay, TrainingWeek, TrainingPlan
from .serializers import (
    UserProfileSerializer, ProgressEntrySerializer, WorkoutTemplateSerializer,
    UserWorkoutSerializer, MealPlanSerializer, AchievementSerializer,
    UserStreakSerializer, DashboardStatsSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """
    Get dashboard overview data
    """
    user = request.user
    today = timezone.now().date()
    
    try:
        # Get user profile
        profile = UserProfile.objects.get(user=user)
        
        # Get latest progress entries
        latest_progress = ProgressEntry.objects.filter(user=user).first()
        week_ago_progress = ProgressEntry.objects.filter(
            user=user, 
            date__lte=today - timedelta(days=7)
        ).first()
        
        # Get all progress entries for the last 30 days
        recent_progress = ProgressEntry.objects.filter(
            user=user,
            date__gte=today - timedelta(days=30)
        ).order_by('-date')
        
        # Get latest weight from either ProgressEntry or WeightHistory
        latest_weight_entry = WeightHistory.objects.filter(user=user).order_by('-date').first()
        current_weight = latest_weight_entry.weight if latest_weight_entry else (latest_progress.weight if latest_progress else profile.weight)
        
        # Update profile's weight if it's different from the latest weight
        if current_weight != profile.weight:
            profile.weight = current_weight
            profile.save()
        
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
        
        # Get user's training plans
        user_plans = TrainingPlan.objects.filter(user=user)
        
        # Get all training days from user's plans
        training_days = TrainingDay.objects.filter(
            training_week__training_plan__in=user_plans
        )
        
        # Calculate weekly stats
        weekly_workouts = training_days.filter(
            completed_at__range=[week_start, week_end]
        )
        
        weekly_workouts_completed = weekly_workouts.filter(completed=True).count()
        weekly_workouts_total = weekly_workouts.count()
        
        # Calculate volume progress
        thirty_days_ago = today - timedelta(days=30)
        completed_volume = training_days.filter(
            completed=True,
            completed_at__gte=thirty_days_ago
        ).count()
        
        total_volume = training_days.filter(
            training_week__training_plan__in=user_plans
        ).count()
        
        volume_progress = (completed_volume / max(1, total_volume)) * 100 if total_volume > 0 else 0
        
        # Calculate program adherence
        adherence = completed_volume
        total_scheduled = total_volume
        
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
        
        # Get recent completed workouts (last 3)
        recent_workouts = training_days.filter(
            completed=True
        ).order_by('-completed_at')[:3]
        
        # Get today's workout
        today_workout = training_days.filter(
            training_week__training_plan__in=user_plans,
            completed=False
        ).first()
        
        # Get today's meals
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
            'recent_workouts': [
                {
                    'id': workout.id,
                    'workout_template': {
                        'name': workout.name,
                        'description': workout.description
                    },
                    'completed_date': workout.completed_at,
                    'duration_minutes': workout.duration_minutes,
                    'is_completed': workout.completed
                }
                for workout in recent_workouts
            ],
            'today_workout': {
                'id': today_workout.id,
                'workout_template': {
                    'name': today_workout.name,
                    'description': today_workout.description
                },
                'scheduled_date': today,
                'duration_minutes': today_workout.duration_minutes,
                'is_completed': today_workout.completed
            } if today_workout else None,
            'today_meals': MealPlanSerializer(today_meals, many=True).data,
            'weekly_nutrition': weekly_nutrition,
            'body_metrics': ProgressEntrySerializer(recent_progress, many=True).data,
            'strength_metrics': [],  # Add strength metrics if needed
            'nutrition_metrics': []  # Add nutrition metrics if needed
        }
        
        return Response(dashboard_data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get or update user profile
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                # If weight is being updated, create a weight log
                if 'weight' in request.data:
                    new_weight = float(request.data['weight'])
                    # Create both ProgressEntry and WeightHistory records
                    today = timezone.now().date()
                    
                    # Update or create ProgressEntry
                    progress_entry, created = ProgressEntry.objects.get_or_create(
                        user=request.user,
                        date=today,
                        defaults={
                            'weight': new_weight,
                            'strength_score': 50,
                            'notes': 'Weight updated from profile'
                        }
                    )
                    if not created:
                        progress_entry.weight = new_weight
                        progress_entry.save()
                    
                    # Update or create WeightHistory
                    weight_history, created = WeightHistory.objects.get_or_create(
                        user=request.user,
                        date=today,
                        defaults={
                            'weight': new_weight,
                            'notes': 'Weight updated from profile'
                        }
                    )
                    if not created:
                        weight_history.weight = new_weight
                        weight_history.save()
                
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
    List all progress entries for user or create a new one.
    If an entry already exists for the given date, it will be updated instead.
    """
    serializer_class = ProgressEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProgressEntry.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        date = serializer.validated_data.get('date')
        try:
            # Try to get existing entry for this date
            instance = ProgressEntry.objects.get(user=self.request.user, date=date)
            # Update existing entry
            for attr, value in serializer.validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        except ProgressEntry.DoesNotExist:
            # Create new entry if none exists
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_weight(request):
    """Log a new weight entry"""
    try:
        date = request.data.get('date')
        weight = request.data.get('weight')
        notes = request.data.get('notes', '')
        strength_score = request.data.get('strength_score', 50)
        
        # Validate required fields
        if not date or not weight:
            return Response(
                {'error': 'Date and weight are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate weight format and range
        try:
            weight = float(weight)
            if weight < 30 or weight > 300:
                return Response(
                    {'error': 'Weight must be between 30 and 300 kg'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Invalid weight format'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Parse and validate date
        try:
            log_date = datetime.strptime(date, '%Y-%m-%d').date()
            if log_date > timezone.now().date():
                return Response(
                    {'error': 'Cannot log weight for future dates'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update or create ProgressEntry
        progress_entry, created = ProgressEntry.objects.get_or_create(
            user=request.user,
            date=log_date,
            defaults={
                'weight': weight,
                'strength_score': strength_score,
                'notes': notes
            }
        )
        if not created:
            progress_entry.weight = weight
            progress_entry.strength_score = strength_score
            progress_entry.notes = notes
            progress_entry.save()

        # Update or create WeightHistory
        weight_history = WeightHistory.objects.filter(
            user=request.user,
            date=log_date
        ).first()
        
        if weight_history:
            weight_history.weight = weight
            weight_history.notes = notes
            weight_history.save()
        else:
            weight_history = WeightHistory.objects.create(
                user=request.user,
                date=log_date,
                weight=weight,
                notes=notes
            )

        # Update user's profile weight
        profile = request.user.profile
        profile.weight = weight
        profile.save()

        return Response({
            'message': 'Weight logged successfully',
            'weight': weight,
            'date': date
        })

    except Exception as e:
        return Response(
            {'error': f'Failed to log weight: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )