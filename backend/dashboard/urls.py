from django.urls import path
from . import views

urlpatterns = [
    # Dashboard overview
    path('overview/', views.dashboard_overview, name='dashboard_overview'),
    
    # User profile
    path('profile/', views.user_profile, name='user_profile'),
    
    # Progress tracking
    path('progress/', views.ProgressEntryListCreateView.as_view(), name='progress_list_create'),
    
    # Workouts
    path('workout-templates/', views.WorkoutTemplateListView.as_view(), name='workout_templates'),
    path('workouts/', views.UserWorkoutListCreateView.as_view(), name='user_workouts'),
    path('workouts/<int:workout_id>/complete/', views.complete_workout, name='complete_workout'),
    
    # Meal plans
    path('meals/', views.MealPlanListCreateView.as_view(), name='meal_plans'),
    
    # Achievements
    path('achievements/', views.AchievementListView.as_view(), name='achievements'),
    path('achievements/mark-read/', views.mark_achievements_read, name='mark_achievements_read'),
]