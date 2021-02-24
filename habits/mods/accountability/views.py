from datetime import timedelta

from django import forms
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.utils.timezone import localdate

from habits.mods.accountability.models import Habit, HabitCompletion


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


def manage_habits(request):
    HabitCompletionFormSet = forms.modelformset_factory(
        HabitCompletion, form=HabitCompletionForm, fields=("habit", "did_complete")
    )
    HabitFormSet = forms.modelformset_factory(
        Habit, can_delete=True, form=HabitForm, fields=("name","one_word_label"), exclude=("create_ts",)
    )
    if request.method == "POST":
        habit_formset = HabitFormSet(request.POST, request.FILES, prefix="habits")
        habitcompletion_formset = HabitCompletionFormSet(
            request.POST, request.FILES, prefix="completion"
        )
        if habit_formset.is_valid() and habitcompletion_formset.is_valid():
            # do something with the cleaned_data on the formsets.
            print("valid!")
            habit_formset.save()
            habitcompletion_formset.save()
            return HttpResponseRedirect(reverse("manage_habits"))
    else:
        today = localdate()
        for habit in Habit.objects.all():
            HabitCompletion.objects.get_or_create(habit=habit, create_ts__date=today)
        todays_habitcompletions = HabitCompletion.objects.filter(
            create_ts__date=today
        )
        habits = Habit.objects.all()
        habit_formset = HabitFormSet(queryset=habits, prefix="habits")
        habitcompletion_formset = HabitCompletionFormSet(
            queryset=todays_habitcompletions, prefix="completion"
        )
    return render(
        request,
        "accountability/habits.html",
        {
            "habit_formset": habit_formset,
            "habitcompletion_formset": habitcompletion_formset,
        },
    )
