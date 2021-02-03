from django.contrib import admin

from habits.mods.accountability.models import Habit, HabitCompletion


admin.site.register(Habit, admin.ModelAdmin)
admin.site.register(HabitCompletion, admin.ModelAdmin)

