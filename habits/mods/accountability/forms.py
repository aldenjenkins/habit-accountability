from django.forms import ModelForm

from habits.mods.accountability.models import HabitCompletion

class HabitCompletionForm(ModelForm):
    class Meta:
        model = HabitCompletiion
        fields = ('did_do',)
