from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from habits.mods.calendar.services import AccountabilityYearlyCalendar

class Command(BaseCommand):

    def handle(self, *args, **options):

        cal = AccountabilityYearlyCalendar(save_path="/home/alden/call.png")
        cal.draw_calendar()
