from django.urls import path

from habits.mods.accountability import views


urlpatterns = [
    path('', views.manage_habits, name='manage_habits'),
]
