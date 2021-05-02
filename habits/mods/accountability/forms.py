from django import forms

from habits.mods.accountability.models import HabitCompletion, Habit


class HabitCompletionForm(forms.ModelForm):
    class Meta:
        model = HabitCompletion
        fields = (
            "habit",
            "did_complete",
        )
        read_only_fields = ("habit",)


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = (
            "id",
            "name",
            "one_word_label",
        )
        read_only_fields = (
            "id",
            "name",
            "create_ts",
        )


