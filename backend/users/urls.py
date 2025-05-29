from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, UserView, ProfileView,
    WeightHistoryView, StrengthProgressView, WorkoutLogView,
    NutritionLogView, UserGoalView, ProgressSummaryView, ProgressMetricsView,
    UserTrainingPlanListCreateView, UserTrainingPlanDetailView,
    UserMealPlanListCreateView, UserMealPlanDetailView,
    GenerateUserTrainingPlanView, GenerateUserMealPlanView,
    TrainingPlanViewSet, TrainingDayViewSet, ExerciseViewSet,
    TrainingProgressViewSet, TrainingAchievementViewSet, UserProfileView,
    generate_meal_plan
)

app_name = 'users'

# Create router for viewsets
router = DefaultRouter()
router.register(r'training-plans', TrainingPlanViewSet, basename='training-plan')
router.register(r'training-days', TrainingDayViewSet, basename='training-day')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'training-progress', TrainingProgressViewSet, basename='training-progress')
router.register(r'training-achievements', TrainingAchievementViewSet, basename='training-achievement')

# Auth URLs
auth_patterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    # Progress endpoints under auth
    path('progress/summary/', ProgressSummaryView.as_view(), name='progress_summary'),
    path('progress/metrics/', ProgressMetricsView.as_view(), name='progress_metrics'),
]

# API URLs
api_patterns = [
    path('', include(router.urls)),
    path('training-plans/generate/', GenerateUserTrainingPlanView.as_view(), name='generate-training-plan'),
    path('progress/weight/', WeightHistoryView.as_view(), name='weight_history'),
    path('progress/strength/', StrengthProgressView.as_view(), name='strength_progress'),
    path('progress/workouts/', WorkoutLogView.as_view(), name='workout_log'),
    path('progress/nutrition/', NutritionLogView.as_view(), name='nutrition_log'),
    path('progress/goals/', UserGoalView.as_view(), name='user_goals'),
    path('meal-plans/', UserMealPlanListCreateView.as_view(), name='meal_plans'),
    path('meal-plans/<int:pk>/', UserMealPlanDetailView.as_view(), name='meal_plan_detail'),
    path('meal-plans/generate/', generate_meal_plan, name='generate_meal_plan'),
]

# Use auth_patterns when included under /api/auth/
urlpatterns = auth_patterns + api_patterns