from django.db import models
from habits.core.models import TimeStampedModel


class Habit(TimeStampedModel):
    name = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return self.name


class HabitCompletion(TimeStampedModel):
    habit = models.ForeignKey(Habit, null=False, on_delete=models.CASCADE)
    did_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.create_ts.month}/{self.create_ts.day}-{str(self.habit)}'

