from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import urls as users_urls
from users.views import GenerateUserTrainingPlanView, regenerate_training_plan, complete_workout

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth endpoints
    path('api/auth/', include((users_urls.auth_patterns, 'users'), namespace='auth')),
    
    # Training plan endpoints
    path('api/training-plans/generate/', GenerateUserTrainingPlanView.as_view(), name='generate-training-plan'),
    path('api/training-plans/<int:plan_id>/regenerate/', regenerate_training_plan, name='regenerate-training-plan'),
    path('api/workouts/<int:workout_id>/complete/', complete_workout, name='complete-workout'),
    
    # API endpoints
    path('api/', include((users_urls.api_patterns, 'users'), namespace='api')),
    path('api/', include('dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)