from rest_framework import serializers

from habits.mods.accountability.models import Habit, HabitCompletion


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'name', 'one_word_label')


class HabitCompletionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='habit.one_word_label')
    name_full = serializers.CharField(source='habit.name')
    class Meta:
        model = HabitCompletion
        fields = ('id', 'name', 'name_full', 'habit', 'did_complete')
