from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.utils.timezone import localdate
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from habits.mods.accountability.forms import HabitCompletionForm, HabitForm
from habits.mods.accountability.models import Habit, HabitCompletion
from habits.mods.accountability.serializers import HabitSerializer, HabitCompletionSerializer


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


class HabitViewSet(ModelViewSet, LoginRequiredMixin):
    model = Habit
    serializer_class = HabitSerializer

    def get_queryset(self):
        habit_qs = Habit.objects.order_by('name')
        date_filter = self.request.GET.get('date')
        if date_filter:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d",)
            habit_qs = habit_qs.filter(create_ts__date__lte=date_filter)
        return habit_qs


class HabitCompletionViewSet(ModelViewSet, LoginRequiredMixin):
    model = HabitCompletion
    serializer_class = HabitCompletionSerializer

    def get_queryset(self):
        today = localdate()
        for habit in Habit.objects.filter(
                create_ts__date__lte=timezone.now()
            ).exclude(
                Exists(
                    HabitCompletion.objects.filter(
                        habit=OuterRef('pk'),
                        create_ts__date=timezone.now()
                    )
                )
            ):
            print("creating new habitcompletion for:", habit)
            HabitCompletion.objects.create(habit=habit)
        habitcompletions = HabitCompletion.objects.filter(
            create_ts__date=timezone.now()
        )
        date_filter = self.request.GET.get('date')
        date_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
        habit_completions = HabitCompletion.objects.filter(create_ts__date=date_filter)
        return habit_completions.select_related('habit').order_by('habit__name')

