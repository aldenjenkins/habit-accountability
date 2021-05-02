from django.urls import path

from habits.mods.accountability import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/habit', views.HabitViewSet, basename='habit')
router.register(r'api/habit_completion', views.HabitCompletionViewSet, basename='habit-accountability')

urlpatterns = [
    path('', views.manage_habits, name='manage_habits'),
]

urlpatterns += router.urls
