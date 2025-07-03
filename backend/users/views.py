from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, UserProfileSerializer,
    WeightHistorySerializer, StrengthProgressSerializer, WorkoutLogSerializer,
    NutritionLogSerializer, UserGoalSerializer, ProgressSummarySerializer,
    UserTrainingPlanSerializer, UserTrainingPlanCreateSerializer,
    UserMealPlanSerializer, UserMealPlanCreateSerializer, UserMealTimeSerializer,
    TrainingPlanSerializer, TrainingPlanCreateSerializer,
    TrainingDaySerializer, ExerciseSerializer,
    TrainingProgressSerializer, TrainingAchievementSerializer
)
from .models import (
    UserProfile, WeightHistory, StrengthProgress, WorkoutLog,
    NutritionLog, UserGoal, UserTrainingPlan, UserTrainingDay,
    UserExercise, UserMealPlan, UserMealTime, UserMealItem,
    TrainingPlan, TrainingWeek, TrainingDay, Exercise,
    TrainingProgress, TrainingAchievement
)
from dashboard.models import ProgressEntry
from .services.training_plan_generator import TrainingPlanGenerator
from .workout_generator import (
    generate_workouts, generate_cardio_workout, generate_cardio_days,
    generate_week_description
)
from .meal_plan_generator import MealPlanGenerator
import logging

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Create user and profile in a transaction
            from django.db import transaction
            with transaction.atomic():
                user = serializer.save()
                
                # Ensure profile exists and update it
                profile = user.profile
                profile_data = {
                    'age': request.data.get('age'),
                    'height': request.data.get('height'),
                    'weight': request.data.get('weight'),
                    'gender': request.data.get('gender'),
                    'fitness_level': request.data.get('fitness_level'),
                }
                
                for key, value in profile_data.items():
                    if value is not None:
                        setattr(profile, key, value)
                profile.save()
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
                # Get user data to return
                user_serializer = UserSerializer(user)
                
                return Response({
                    'user': user_serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)
                
                return Response({
                    'user': user_serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            # Get the token from request
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        """Get user profile data"""
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch profile: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        """Update user profile data"""
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            
            if serializer.is_valid():
                # If weight is being updated, create weight logs
                if 'weight' in request.data:
                    weight = float(request.data['weight'])
                    today = timezone.now().date()
                    
                    try:
                        # Update or create ProgressEntry
                        progress_entry, created = ProgressEntry.objects.get_or_create(
                            user=request.user,
                            date=today,
                            defaults={
                                'weight': weight,
                                'strength_score': 50,
                                'notes': 'Weight updated from profile'
                            }
                        )
                        if not created:
                            progress_entry.weight = weight
                            progress_entry.save()
                        
                        # Update or create WeightHistory
                        weight_history = WeightHistory.objects.filter(
                            user=request.user,
                            date=today
                        ).first()
                        
                        if weight_history:
                            weight_history.weight = weight
                            weight_history.notes = 'Weight updated from profile'
                            weight_history.save()
                        else:
                            WeightHistory.objects.create(
                                user=request.user,
                                date=today,
                                weight=weight,
                                notes='Weight updated from profile'
                            )
                    except Exception as e:
                        # Log the error but don't fail the profile update
                        print(f"Error updating weight history: {e}")
                
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f'Failed to update profile: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, user_id):
        """Get another user's profile data"""
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class WeightHistoryView(generics.ListCreateAPIView):
    serializer_class = WeightHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeightHistory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StrengthProgressView(generics.ListCreateAPIView):
    serializer_class = StrengthProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StrengthProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutLogView(generics.ListCreateAPIView):
    serializer_class = WorkoutLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NutritionLogView(generics.ListCreateAPIView):
    serializer_class = NutritionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NutritionLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserGoalView(generics.ListCreateAPIView):
    serializer_class = UserGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProgressSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get progress summary for the authenticated user"""
        try:
            user = request.user
            logger.info(f"Fetching progress summary for user {user.username}")
            
            now = timezone.now()
            thirty_days_ago = now - timedelta(days=30)
            seven_days_ago = now - timedelta(days=7)

            # Weight change calculation
            latest_weight = WeightHistory.objects.filter(user=user).order_by('-date').first()
            first_weight = WeightHistory.objects.filter(user=user).order_by('date').first()
            logger.info(f"Weight records - Latest: {latest_weight}, First: {first_weight}")
            
            weight_change = 0
            if latest_weight and first_weight:
                weight_change = latest_weight.weight - first_weight.weight
                logger.info(f"Calculated weight change: {weight_change}")
            
            # Strength increase calculation
            strength_increase = 0
            strength_exercises = StrengthProgress.objects.filter(
                user=user,
                date__gte=thirty_days_ago
            ).values('exercise').annotate(
                avg_weight=Avg('weight')
            )
            logger.info(f"Found {len(strength_exercises)} strength exercises")
            
            if strength_exercises:
                increases = []
                for exercise in strength_exercises:
                    first = StrengthProgress.objects.filter(
                        user=user,
                        exercise=exercise['exercise']
                    ).order_by('date').first()
                    
                    if first and first.weight > 0:  # Prevent division by zero
                        increase = (exercise['avg_weight'] - first.weight) / first.weight * 100
                        increases.append(increase)
                        logger.info(f"Strength increase for {exercise['exercise']}: {increase}%")
                
                if increases:
                    strength_increase = sum(increases) / len(increases)
                    logger.info(f"Average strength increase: {strength_increase}%")

            # Workout consistency calculation
            total_possible_workouts = 28  # 4 weeks * 7 days
            completed_workouts = WorkoutLog.objects.filter(
                user=user,
                date__gte=thirty_days_ago
            ).count()
            workout_consistency = (completed_workouts / total_possible_workouts) * 100 if total_possible_workouts > 0 else 0
            logger.info(f"Workout consistency: {workout_consistency}% ({completed_workouts}/{total_possible_workouts})")

            # Goal progress calculation
            active_goals = UserGoal.objects.filter(user=user, achieved=False)
            goal_progress = 0
            if active_goals:
                progress_sum = sum(goal.progress_percentage for goal in active_goals)
                goal_progress = progress_sum / active_goals.count()
                logger.info(f"Goal progress: {goal_progress}% across {active_goals.count()} active goals")

            # Recent achievements
            recent_achievements = []
            
            # Weight achievement check
            if latest_weight and first_weight:
                if weight_change < 0:  # Weight loss achievement
                    recent_achievements.append({
                        'title': 'Weight Loss Achievement',
                        'description': f'Lost {abs(weight_change):.1f} kg',
                        'date': latest_weight.date.isoformat(),
                        'icon': 'scale',
                        'color': 'green'
                    })
                elif weight_change > 0:  # Weight gain achievement
                    recent_achievements.append({
                        'title': 'Muscle Gain Achievement',
                        'description': f'Gained {weight_change:.1f} kg',
                        'date': latest_weight.date.isoformat(),
                        'icon': 'dumbbell',
                        'color': 'blue'
                    })

            # Strength achievement check
            recent_strength = StrengthProgress.objects.filter(
                user=user,
                date__gte=seven_days_ago
            ).order_by('-weight').first()
            
            if recent_strength:
                recent_achievements.append({
                    'title': 'Strength Milestone',
                    'description': f'New {recent_strength.exercise} record: {recent_strength.weight} kg',
                    'date': recent_strength.date.isoformat(),
                    'icon': 'dumbbell',
                    'color': 'purple'
                })

            # Workout streak check
            recent_workouts = WorkoutLog.objects.filter(
                user=user,
                date__gte=seven_days_ago
            ).count()
            
            if recent_workouts >= 5:
                recent_achievements.append({
                    'title': 'Workout Streak',
                    'description': f'Completed {recent_workouts} workouts in 7 days',
                    'date': now.date().isoformat(),
                    'icon': 'activity',
                    'color': 'orange'
                })
            logger.info(f"Found {len(recent_achievements)} recent achievements")

            # Prepare metrics data
            body_metrics = list(WeightHistory.objects.filter(
                user=user,
                date__gte=thirty_days_ago
            ).values('date', 'weight', 'body_fat', 'muscle_mass').order_by('date'))
            logger.info(f"Found {len(body_metrics)} body metric records")

            strength_metrics = list(StrengthProgress.objects.filter(
                user=user,
                date__gte=thirty_days_ago
            ).values('date', 'exercise', 'weight').order_by('date'))
            logger.info(f"Found {len(strength_metrics)} strength metric records")

            workout_metrics = list(WorkoutLog.objects.filter(
                user=user,
                date__gte=thirty_days_ago
            ).values('date', 'duration', 'intensity', 'calories_burned').order_by('date'))
            logger.info(f"Found {len(workout_metrics)} workout metric records")

            nutrition_metrics = list(NutritionLog.objects.filter(
                user=user,
                date__gte=thirty_days_ago
            ).values('date', 'calories', 'protein', 'carbs', 'fats', 'water').order_by('date'))
            logger.info(f"Found {len(nutrition_metrics)} nutrition metric records")

            data = {
                'weight_change': weight_change,
                'strength_increase': strength_increase,
                'workout_consistency': workout_consistency,
                'goal_progress': goal_progress,
                'recent_achievements': recent_achievements,
                'body_metrics': body_metrics,
                'strength_metrics': strength_metrics,
                'workout_metrics': workout_metrics,
                'nutrition_metrics': nutrition_metrics,
            }
            logger.info("Prepared data dictionary for serialization")

            serializer = ProgressSummarySerializer(data=data)
            if not serializer.is_valid():
                logger.error(f"Serializer validation failed: {serializer.errors}")
                return Response(
                    {"error": "Failed to process progress data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            logger.info("Successfully serialized progress data")

            return Response(serializer.validated_data)

        except Exception as e:
            logger.error(f"Error fetching progress summary: {str(e)}", exc_info=True)
            return Response(
                {"error": "Failed to fetch progress data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProgressMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get detailed progress metrics for the authenticated user"""
        try:
            user = request.user
            logger.info(f"Fetching progress metrics for user {user.username}")
            
            time_range = request.query_params.get('time_range', '7W')
            
            # Calculate date range
            now = timezone.now()
            if time_range == '1M':
                start_date = now - timedelta(days=30)
            elif time_range == '3M':
                start_date = now - timedelta(days=90)
            elif time_range == '7W':
                start_date = now - timedelta(weeks=7)
            elif time_range == '1Y':
                start_date = now - timedelta(days=365)
            else:  # ALL
                start_date = None
            
            # Query metrics with date filter if applicable
            date_filter = {'date__gte': start_date} if start_date else {}
            
            # Get body metrics
            body_metrics = list(WeightHistory.objects.filter(
                user=user,
                **date_filter
            ).order_by('date').values('date', 'weight', 'body_fat', 'muscle_mass'))
            logger.info(f"Found {len(body_metrics)} body metric records")
            
            # Get strength metrics
            strength_metrics = list(StrengthProgress.objects.filter(
                user=user,
                **date_filter
            ).order_by('date').values('date', 'exercise', 'weight'))
            logger.info(f"Found {len(strength_metrics)} strength metric records")
            
            # Get workout metrics
            workout_metrics = list(WorkoutLog.objects.filter(
                user=user,
                **date_filter
            ).order_by('date').values('date', 'duration', 'intensity', 'calories_burned'))
            logger.info(f"Found {len(workout_metrics)} workout metric records")
            
            # Get nutrition metrics
            nutrition_metrics = list(NutritionLog.objects.filter(
                user=user,
                **date_filter
            ).order_by('date').values('date', 'calories', 'protein', 'carbs', 'fats', 'water'))
            logger.info(f"Found {len(nutrition_metrics)} nutrition metric records")
            
            # Calculate achievements
            achievements = []
            
            # Weight achievements
            if body_metrics:
                first_weight = body_metrics[0]['weight']
                last_weight = body_metrics[-1]['weight']
                weight_change = last_weight - first_weight
                
                if abs(weight_change) >= 2:  # Achievement for 2kg change
                    achievements.append({
                        'title': 'Weight Goal Progress',
                        'description': f'{"Lost" if weight_change < 0 else "Gained"} {abs(weight_change):.1f} kg',
                        'date': now.date().isoformat(),
                        'icon': 'scale',
                        'color': 'green' if weight_change < 0 else 'blue'
                    })
            
            # Strength achievements
            recent_strength = StrengthProgress.objects.filter(
                user=user,
                **date_filter
            ).order_by('-weight').first()
            
            if recent_strength:
                achievements.append({
                    'title': 'Strength Milestone',
                    'description': f'New {recent_strength.exercise} record: {recent_strength.weight} kg',
                    'date': recent_strength.date.isoformat(),
                    'icon': 'dumbbell',
                    'color': 'purple'
                })
            
            # Workout consistency achievement
            workout_count = len(workout_metrics)
            if workout_count >= 12:  # 3 workouts per week for 4 weeks
                achievements.append({
                    'title': 'Consistency Champion',
                    'description': f'Completed {workout_count} workouts',
                    'date': now.date().isoformat(),
                    'icon': 'activity',
                    'color': 'orange'
                })
            
            data = {
                'body_metrics': body_metrics,
                'strength_metrics': strength_metrics,
                'workout_metrics': workout_metrics,
                'nutrition_metrics': nutrition_metrics,
                'achievements': achievements,
                'time_range': time_range
            }
            logger.info("Successfully prepared progress metrics data")
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching progress metrics: {str(e)}", exc_info=True)
            return Response(
                {"error": "Failed to fetch progress metrics", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserTrainingPlanListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserTrainingPlan.objects.filter(user=self.request.user, is_active=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserTrainingPlanCreateSerializer
        return UserTrainingPlanSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserTrainingPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserTrainingPlanSerializer
    
    def get_queryset(self):
        return UserTrainingPlan.objects.filter(user=self.request.user)

class UserMealPlanListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = UserMealPlan.objects.filter(user=self.request.user, is_active=True).order_by('-created_at')
        logger.info(f"User {self.request.user.username} (ID: {self.request.user.id}) querying meal plans. Found {queryset.count()} active plans.")
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserMealPlanCreateSerializer
        return UserMealPlanSerializer
    
    def perform_create(self, serializer):
        logger.info(f"User {self.request.user.username} creating meal plan via ListCreateView")
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Add debug info to list response - handle both paginated and non-paginated responses
        debug_info = {
            'user_id': request.user.id,
            'username': request.user.username,
            'query_timestamp': timezone.now().isoformat()
        }
        
        if isinstance(response.data, dict):
            # Paginated response
            if 'results' in response.data:
                debug_info['total_plans'] = len(response.data['results'])
                response.data['debug_info'] = debug_info
            else:
                # Single dict response
                debug_info['total_plans'] = 1
                response.data['debug_info'] = debug_info
        elif isinstance(response.data, list):
            # Non-paginated list response - convert to dict format
            debug_info['total_plans'] = len(response.data)
            response.data = {
                'results': response.data,
                'debug_info': debug_info
            }
        
        return response

class UserMealPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMealPlanSerializer
    
    def get_queryset(self):
        return UserMealPlan.objects.filter(user=self.request.user)

class GenerateUserTrainingPlanView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get user preferences from request
            user_data = {
                'goal': request.data.get('goal', 'strength'),
                'difficulty': request.data.get('difficulty', 'intermediate'),
                'duration_weeks': request.data.get('duration_weeks', 8),
                'user': request.user
            }
            
            # Initialize the generator
            generator = TrainingPlanGenerator()
            
            try:
                # Generate the plan
                plan = generator.generate_plan(user_data)
                
                # Serialize and return the plan
                serializer = TrainingPlanSerializer(plan)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error generating training plan: {str(e)}", exc_info=True)
                return Response(
                    {'error': 'Failed to generate training plan', 'details': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except Exception as e:
            logger.error(f"Error in training plan generation view: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class GenerateUserMealPlanView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Generate a personalized meal plan based on user preferences"""
        # Get user preferences from request
        goal = request.data.get('goal')
        calories_target = request.data.get('calories_target')
        dietary_restrictions = request.data.get('dietary_restrictions', [])
        meals_per_day = request.data.get('meals_per_day', 4)
        
        # Get user's profile for personalization
        profile = request.user.profile
        
        # Calculate macros based on goal
        protein_target = int(profile.weight * 2.2)  # 2.2g per kg of body weight
        if goal == 'muscle_gain':
            calories_target = calories_target or int(profile.weight * 35)  # 35 calories per kg
            carbs_target = int((calories_target * 0.5) / 4)  # 50% of calories from carbs
            fats_target = int((calories_target * 0.25) / 9)  # 25% of calories from fats
        elif goal == 'weight_loss':
            calories_target = calories_target or int(profile.weight * 25)  # 25 calories per kg
            carbs_target = int((calories_target * 0.4) / 4)  # 40% of calories from carbs
            fats_target = int((calories_target * 0.3) / 9)  # 30% of calories from fats
        else:  # maintenance
            calories_target = calories_target or int(profile.weight * 30)  # 30 calories per kg
            carbs_target = int((calories_target * 0.45) / 4)  # 45% of calories from carbs
            fats_target = int((calories_target * 0.275) / 9)  # 27.5% of calories from fats
        
        # Create meal plan structure
        meal_plan = {
            'name': f'{goal.title()} Meal Plan',
            'description': f'A personalized meal plan for {goal}',
            'goal': goal,
            'calories_target': calories_target,
            'protein_target': protein_target,
            'carbs_target': carbs_target,
            'fats_target': fats_target,
            'meal_times': self._generate_meal_times(
                meals_per_day,
                calories_target,
                protein_target,
                carbs_target,
                fats_target
            )
        }
        
        # Create the plan
        serializer = UserMealPlanCreateSerializer(data=meal_plan)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _generate_meal_times(self, meals_per_day, calories, protein, carbs, fats):
        """Generate meal times with appropriate macro distribution"""
        meal_times = []
        
        # Define meal schedules based on number of meals
        meal_schedules = {
            3: [
                {'name': 'Breakfast', 'time': '08:00', 'ratio': 0.3},
                {'name': 'Lunch', 'time': '13:00', 'ratio': 0.4},
                {'name': 'Dinner', 'time': '19:00', 'ratio': 0.3}
            ],
            4: [
                {'name': 'Breakfast', 'time': '08:00', 'ratio': 0.25},
                {'name': 'Lunch', 'time': '12:30', 'ratio': 0.35},
                {'name': 'Snack', 'time': '16:00', 'ratio': 0.1},
                {'name': 'Dinner', 'time': '19:30', 'ratio': 0.3}
            ],
            5: [
                {'name': 'Breakfast', 'time': '07:30', 'ratio': 0.25},
                {'name': 'Morning Snack', 'time': '10:30', 'ratio': 0.1},
                {'name': 'Lunch', 'time': '13:30', 'ratio': 0.3},
                {'name': 'Afternoon Snack', 'time': '16:30', 'ratio': 0.1},
                {'name': 'Dinner', 'time': '19:30', 'ratio': 0.25}
            ],
            6: [
                {'name': 'Early Breakfast', 'time': '07:00', 'ratio': 0.2},
                {'name': 'Morning Snack', 'time': '10:00', 'ratio': 0.1},
                {'name': 'Lunch', 'time': '13:00', 'ratio': 0.25},
                {'name': 'Afternoon Snack', 'time': '16:00', 'ratio': 0.1},
                {'name': 'Dinner', 'time': '19:00', 'ratio': 0.25},
                {'name': 'Evening Snack', 'time': '21:00', 'ratio': 0.1}
            ]
        }
        
        # Use the appropriate meal schedule or default to 4 meals
        schedule = meal_schedules.get(meals_per_day, meal_schedules[4])
        
        for i, meal in enumerate(schedule):
            meal_calories = int(calories * meal['ratio'])
            meal_protein = int(protein * meal['ratio'])
            meal_carbs = int(carbs * meal['ratio'])
            meal_fats = int(fats * meal['ratio'])
            
            meal_time = {
                'name': meal['name'],
                'time': meal['time'],
                'calories': meal_calories,
                'protein': meal_protein,
                'carbs': meal_carbs,
                'fats': meal_fats,
                'order': i + 1,
                'meal_items': self._generate_meal_items(
                    meal['name'],
                    meal_calories,
                    meal_protein,
                    meal_carbs,
                    meal_fats
                )
            }
            meal_times.append(meal_time)
        
        return meal_times
    
    def _generate_meal_items(self, meal_type, calories, protein, carbs, fats):
        """Generate meal items based on meal type and macros"""
        # This is a basic template - in a real app, you'd have a food database
        if meal_type == 'Breakfast':
            return [
                {
                    'name': 'Oatmeal',
                    'quantity': 100,
                    'unit': 'g',
                    'calories': int(calories * 0.4),
                    'protein': int(protein * 0.2),
                    'carbs': int(carbs * 0.6),
                    'fats': int(fats * 0.1),
                    'order': 1
                },
                {
                    'name': 'Eggs',
                    'quantity': 2,
                    'unit': 'piece',
                    'calories': int(calories * 0.3),
                    'protein': int(protein * 0.6),
                    'carbs': 0,
                    'fats': int(fats * 0.6),
                    'order': 2
                },
                {
                    'name': 'Banana',
                    'quantity': 1,
                    'unit': 'piece',
                    'calories': int(calories * 0.3),
                    'protein': int(protein * 0.2),
                    'carbs': int(carbs * 0.4),
                    'fats': int(fats * 0.3),
                    'order': 3
                }
            ]
        elif meal_type == 'Lunch' or meal_type == 'Dinner':
            return [
                {
                    'name': 'Chicken Breast',
                    'quantity': 150,
                    'unit': 'g',
                    'calories': int(calories * 0.4),
                    'protein': int(protein * 0.7),
                    'carbs': 0,
                    'fats': int(fats * 0.2),
                    'order': 1
                },
                {
                    'name': 'Brown Rice',
                    'quantity': 100,
                    'unit': 'g',
                    'calories': int(calories * 0.3),
                    'protein': int(protein * 0.1),
                    'carbs': int(carbs * 0.7),
                    'fats': int(fats * 0.1),
                    'order': 2
                },
                {
                    'name': 'Mixed Vegetables',
                    'quantity': 200,
                    'unit': 'g',
                    'calories': int(calories * 0.3),
                    'protein': int(protein * 0.2),
                    'carbs': int(carbs * 0.3),
                    'fats': int(fats * 0.7),
                    'order': 3
                }
            ]
        else:  # Snack
            return [
                {
                    'name': 'Greek Yogurt',
                    'quantity': 200,
                    'unit': 'g',
                    'calories': int(calories * 0.6),
                    'protein': int(protein * 0.8),
                    'carbs': int(carbs * 0.3),
                    'fats': int(fats * 0.4),
                    'order': 1
                },
                {
                    'name': 'Mixed Nuts',
                    'quantity': 30,
                    'unit': 'g',
                    'calories': int(calories * 0.4),
                    'protein': int(protein * 0.2),
                    'carbs': int(carbs * 0.7),
                    'fats': int(fats * 0.6),
                    'order': 2
                }
            ]

class TrainingPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingPlanSerializer

    def get_queryset(self):
        return TrainingPlan.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return TrainingPlanCreateSerializer
        return TrainingPlanSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TrainingDayViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingDaySerializer

    def get_queryset(self):
        return TrainingDay.objects.filter(training_week__training_plan__user=self.request.user)

class ExerciseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.filter(training_day__training_week__training_plan__user=self.request.user)

class TrainingProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingProgressSerializer

    def get_queryset(self):
        return TrainingProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TrainingAchievementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingAchievementSerializer

    def get_queryset(self):
        return TrainingAchievement.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_training_plan(request):
    """Generate a new training plan based on user preferences using TrainingPlanGenerator."""
    try:
        # Collect all relevant fields from the frontend
        user_data = {
            'goal': request.data.get('goal', 'strength'),
            'difficulty': request.data.get('difficulty', 'intermediate'),
            'duration_weeks': request.data.get('duration_weeks', 8),
            'training_style': request.data.get('training_style', 'traditional'),
            'equipment_available': request.data.get('equipment_available', ['barbell', 'dumbbell', 'bodyweight']),
            'include_deload_weeks': request.data.get('include_deload_weeks', False),
            'experience_years': request.data.get('experience_years', 0),
            'injuries_limitations': request.data.get('injuries_limitations', []),
            'preferred_exercises': request.data.get('preferred_exercises', []),
            'excluded_exercises': request.data.get('excluded_exercises', []),
            'cardio_preferences': request.data.get('cardio_preferences', {
                'type': ['running'],
                'duration': 20,
                'frequency': 2
            }),
            'days_per_week': request.data.get('days_per_week', 4),
            'preferred_workout_duration': request.data.get('preferred_workout_duration', 60),
            'user': request.user
        }
        generator = TrainingPlanGenerator()
        plan = generator.generate_plan(user_data)
        serializer = TrainingPlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_training_plan(request, plan_id):
    """Regenerate an existing training plan with new preferences using TrainingPlanGenerator."""
    try:
        logger.info(f"Regenerating training plan {plan_id} for user {request.user.username}")
        logger.info(f"Request data: {request.data}")
        
        training_plan = get_object_or_404(TrainingPlan, id=plan_id, user=request.user)
        logger.info(f"Found training plan: {training_plan.name}")
        
        # Update the existing plan's fields with new preferences
        training_plan.goal = request.data.get('goal', training_plan.goal)
        training_plan.difficulty = request.data.get('difficulty', training_plan.difficulty)
        training_plan.duration_weeks = request.data.get('duration_weeks', training_plan.duration_weeks)
        training_plan.training_style = request.data.get('training_style', training_plan.training_style)
        training_plan.equipment_available = request.data.get('equipment_available', training_plan.equipment_available)
        training_plan.include_deload_weeks = request.data.get('include_deload_weeks', training_plan.include_deload_weeks)
        training_plan.experience_years = request.data.get('experience_years', training_plan.experience_years)
        training_plan.injuries_limitations = request.data.get('injuries_limitations', training_plan.injuries_limitations)
        training_plan.preferred_exercises = request.data.get('preferred_exercises', training_plan.preferred_exercises)
        training_plan.excluded_exercises = request.data.get('excluded_exercises', training_plan.excluded_exercises)
        training_plan.cardio_preferences = request.data.get('cardio_preferences', training_plan.cardio_preferences)
        training_plan.save()
        logger.info("Updated training plan fields")
        
        # Delete existing weeks and workouts
        weeks_deleted = training_plan.weeks.all().count()
        training_plan.weeks.all().delete()
        logger.info(f"Deleted {weeks_deleted} existing weeks")
        
        # Collect all relevant fields for regeneration
        user_data = {
            'goal': training_plan.goal,
            'difficulty': training_plan.difficulty,
            'duration_weeks': training_plan.duration_weeks,
            'training_style': training_plan.training_style,
            'equipment_available': training_plan.equipment_available,
            'include_deload_weeks': training_plan.include_deload_weeks,
            'experience_years': training_plan.experience_years,
            'injuries_limitations': training_plan.injuries_limitations,
            'preferred_exercises': training_plan.preferred_exercises,
            'excluded_exercises': training_plan.excluded_exercises,
            'cardio_preferences': training_plan.cardio_preferences,
            'days_per_week': request.data.get('days_per_week', 4),
            'preferred_workout_duration': request.data.get('preferred_workout_duration', 60),
            'user': request.user,
            'existing_plan': training_plan  # Pass the existing plan to avoid creating new one
        }
        
        # Use the generator to regenerate weeks and exercises for the existing plan
        generator = TrainingPlanGenerator()
        logger.info("Calling regenerate_existing_plan...")
        regenerated_plan = generator.regenerate_existing_plan(training_plan, user_data)
        logger.info(f"Successfully regenerated plan: {regenerated_plan.name}")
        
        # Return the updated plan
        serializer = TrainingPlanSerializer(regenerated_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error regenerating training plan: {str(e)}", exc_info=True)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_workout(request, workout_id):
    """Mark a workout as completed and record the progress."""
    try:
        # Get the workout
        workout = get_object_or_404(TrainingDay, id=workout_id)
        
        # Verify user owns this workout
        if workout.training_week.training_plan.user != request.user:
            return Response(
                {'error': 'Not authorized to modify this workout'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            # Mark workout as completed
            workout.completed = True
            workout.completed_at = timezone.now()
            workout.save()
        except Exception as e:
            logger.warning(f"Error setting completed fields: {str(e)}")
            # If the fields don't exist, we'll still return success
            pass
        
        try:
            # Mark exercises as completed
            workout.exercises.all().update(completed=True)
        except Exception as e:
            logger.warning(f"Error marking exercises as completed: {str(e)}")
            pass
        
        try:
            # Create a workout log entry
            WorkoutLog.objects.create(
                user=request.user,
                date=timezone.now(),
                duration=workout.duration_minutes,
                workout_type=workout.name,
                notes=f"Completed {workout.name} from training plan"
            )
        except Exception as e:
            logger.warning(f"Error creating workout log: {str(e)}")
            pass
        
        # Return updated workout data
        serializer = TrainingDaySerializer(workout)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error completing workout: {str(e)}", exc_info=True)
        return Response(
            {'error': 'Failed to complete workout', 'details': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_meal_plan(request):
    """Generate a personalized meal plan using AI."""
    try:
        # Log incoming request data with user info
        logger.info(f"User {request.user.username} (ID: {request.user.id}) generating meal plan with data: {request.data}")
        
        # Get user profile data
        profile = request.user.profile
        logger.info(f"User {request.user.username} profile data: {profile.__dict__}")
        
        # Get the most recent weight from weight history if available, otherwise use profile weight
        latest_weight_entry = WeightHistory.objects.filter(user=request.user).order_by('-date').first()
        current_weight = float(latest_weight_entry.weight) if latest_weight_entry else float(profile.weight)
        
        # Get body fat from latest weight history if available
        current_body_fat = latest_weight_entry.body_fat if latest_weight_entry and latest_weight_entry.body_fat else 20
        
        # Validate that we have actual user data, not just defaults
        if profile.weight == 70.0 and profile.height == 170.0 and profile.age == 18:
            logger.warning("User appears to be using default profile values. Meal plan may not be accurate.")
        
        # Prepare user data for meal plan generation with enhanced data collection
        user_data = {
            'weight': current_weight,
            'height': float(profile.height),
            'age': profile.age,
            'gender': profile.gender,
            'activity_level': request.data.get('activity_level', 'moderate'),
            'goal': request.data.get('goal', 'maintenance'),
            'vegetarian': request.data.get('vegetarian', False),
            'vegan': request.data.get('vegan', False),
            'dietary_preferences': request.data.get('dietary_preferences', []),
            'allergies': request.data.get('allergies', []),
            'excluded_foods': request.data.get('excluded_foods', []),
            'preferred_foods': request.data.get('preferred_foods', []),
            'fitness_level': profile.fitness_level,
            'body_fat_pct': current_body_fat,
            'blood_pressure_systolic': 120,  # Could be enhanced with actual user data
            'blood_pressure_diastolic': 80,  # Could be enhanced with actual user data
            'resting_heart_rate': 70,  # Could be enhanced with actual user data
            'hours_sleep': 7  # Could be enhanced with actual user data
        }
        
        logger.info(f"User {request.user.username} prepared user data: {user_data}")
        
        # Initialize meal plan generator
        generator = MealPlanGenerator()
        
        # Generate meal plan
        meal_plan = generator.generate_meal_plan(
            user_data,
            duration_days=request.data.get('duration_days', 7)
        )
        
        logger.info(f"Successfully generated meal plan for user {request.user.username} (ID: {request.user.id})")
        
        # Mark any existing meal plans as inactive instead of deleting
        UserMealPlan.objects.filter(user=request.user, is_active=True).update(is_active=False)
        
        # Create meal plan in database with correct targets and unique name
        plan_name = f"{user_data['goal'].title()} Meal Plan - {timezone.now().strftime('%Y-%m-%d %H:%M')}"
        db_meal_plan = UserMealPlan.objects.create(
            user=request.user,
            name=plan_name,
            description=f"AI-generated meal plan for {user_data['goal']} (User: {request.user.username})",
            goal=user_data['goal'],
            calories_target=int(meal_plan['targets']['calories']),
            protein_target=int(meal_plan['targets']['protein']),
            carbs_target=int(meal_plan['targets']['carbs']),
            fats_target=int(meal_plan['targets']['fat']),
            start_date=meal_plan['start_date'],
            end_date=meal_plan['end_date'],
            is_active=True
        )
        
        # Create meal times and items for each day
        meal_order = {
            'breakfast': 1,
            'morning_snack': 2,
            'lunch': 3,
            'afternoon_snack': 4,
            'dinner': 5,
            'snack': 4,
            'snack1': 4,
            'snack2': 5
        }
        
        logger.info(f"Creating meal plan database entries for user {request.user.username} with {len(meal_plan['daily_plans'])} days")
        
        for date, daily_plan in meal_plan['daily_plans'].items():
            logger.info(f"Processing day {date} with {len(daily_plan['meals'])} meals for user {request.user.username}")
            for meal_name, meal_data in daily_plan['meals'].items():
                # Use the time from the meal plan generator instead of default times
                meal_time_str = meal_data.get('time', _get_default_meal_time(meal_name))
                
                # Use the proper display name from the meal plan generator
                display_name = meal_data.get('type', meal_name.title())
                
                meal_time = UserMealTime.objects.create(
                    meal_plan=db_meal_plan,
                    name=display_name,
                    time=meal_time_str,
                    calories=int(meal_data['nutrition']['calories']),
                    protein=int(meal_data['nutrition']['protein']),
                    carbs=int(meal_data['nutrition']['carbs']),
                    fats=int(meal_data['nutrition']['fat']),
                    date=date,
                    order=meal_order.get(meal_name.lower(), 1)
                )
                
                # Create meal items
                logger.info(f"Creating {len(meal_data['foods'])} food items for {meal_name} on {date} for user {request.user.username}")
                for idx, food in enumerate(meal_data['foods'], start=1):
                    UserMealItem.objects.create(
                        meal_time=meal_time,
                        name=food['name'],
                        quantity=float(food['quantity']),
                        unit=food['unit'],
                        calories=int(food['calories']),
                        protein=float(food['protein']),
                        carbs=float(food['carbs']),
                        fats=float(food['fat']),
                        order=idx
                    )
        
        # Return the created meal plan
        logger.info(f"Successfully saved meal plan {db_meal_plan.id} for user {request.user.username} to database")
        serializer = UserMealPlanSerializer(db_meal_plan)
        response_data = serializer.data
        
        # Add debug info to response
        response_data['debug_info'] = {
            'user_id': request.user.id,
            'username': request.user.username,
            'plan_id': db_meal_plan.id,
            'created_at': db_meal_plan.created_at.isoformat(),
            'is_active': db_meal_plan.is_active
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error generating meal plan: {str(e)}", exc_info=True)
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meal_plan_preview(request):
    """Get a preview of what data will be used for meal plan generation."""
    try:
        # Get user profile data
        profile = request.user.profile
        
        # Get the most recent weight from weight history if available
        latest_weight_entry = WeightHistory.objects.filter(user=request.user).order_by('-date').first()
        current_weight = float(latest_weight_entry.weight) if latest_weight_entry else float(profile.weight)
        current_body_fat = latest_weight_entry.body_fat if latest_weight_entry and latest_weight_entry.body_fat else None
        
        # Check if profile is complete
        is_complete = not (profile.weight == 70.0 and profile.height == 170.0 and profile.age == 18)
        
        # Calculate estimated calories using current data
        user_data = {
            'weight': current_weight,
            'height': float(profile.height),
            'age': profile.age,
            'gender': profile.gender,
            'activity_level': 'moderate',  # Default for preview
            'goal': 'maintenance'  # Default for preview
        }
        
        # Initialize meal plan generator to get calorie estimate
        try:
            generator = MealPlanGenerator()
            estimated_calories = generator.predict_calories(user_data)
        except Exception as e:
            estimated_calories = None
            logger.warning(f"Could not calculate calorie estimate: {str(e)}")
        
        preview_data = {
            'profile_complete': is_complete,
            'current_data': {
                'weight': current_weight,
                'weight_source': 'weight_history' if latest_weight_entry else 'profile',
                'height': float(profile.height),
                'age': profile.age,
                'gender': profile.gender,
                'fitness_level': profile.fitness_level,
                'body_fat': current_body_fat,
                'last_weight_update': latest_weight_entry.date.isoformat() if latest_weight_entry else None
            },
            'estimated_calories': {
                'maintenance': estimated_calories,
                'weight_loss': estimated_calories - 500 if estimated_calories else None,
                'muscle_gain': estimated_calories + 500 if estimated_calories else None
            } if estimated_calories else None,
            'recommendations': []
        }
        
        # Add recommendations based on profile completeness
        if not is_complete:
            preview_data['recommendations'].append(
                "Please update your profile with accurate height, weight, and age for more precise meal plan calculations."
            )
        
        if not latest_weight_entry:
            preview_data['recommendations'].append(
                "Consider adding your current weight to weight history for more accurate calculations."
            )
        
        if current_body_fat is None:
            preview_data['recommendations'].append(
                "Adding body fat percentage to your weight history will improve meal plan accuracy."
            )
        
        return Response(preview_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error getting meal plan preview: {str(e)}", exc_info=True)
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_meal_eaten(request, meal_time_id):
    """Mark a meal as eaten or not eaten."""
    try:
        # Get the meal time object, ensuring it belongs to the current user
        meal_time = UserMealTime.objects.filter(
            id=meal_time_id,
            meal_plan__user=request.user
        ).first()
        
        if not meal_time:
            return Response(
                {'error': 'Meal not found or not authorized'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Toggle or set the eaten status
        is_eaten = request.data.get('is_eaten', not meal_time.is_eaten)
        
        meal_time.is_eaten = is_eaten
        if is_eaten:
            meal_time.eaten_at = timezone.now()
        else:
            meal_time.eaten_at = None
        meal_time.save()
        
        logger.info(f"User {request.user.username} marked meal {meal_time.name} (ID: {meal_time_id}) as {'eaten' if is_eaten else 'not eaten'}")
        
        # Return updated meal time data
        serializer = UserMealTimeSerializer(meal_time)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error marking meal as eaten: {str(e)}", exc_info=True)
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _get_default_meal_time(meal_name: str) -> str:
    """Get default time for each meal type."""
    meal_times = {
        'breakfast': '08:00',
        'lunch': '13:00',
        'dinner': '19:00',
        'snack': '16:00',
        'morning_snack': '10:00',
        'afternoon_snack': '16:00'
    }
    return meal_times.get(meal_name.lower(), '12:00')