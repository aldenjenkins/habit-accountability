from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
from django.utils import timezone

from habits.mods.calendar import services


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_month = timezone.localtime(timezone.now()).month
        monthly_cal = services.AccountabilityMonthlyCalendar(
            save_path="/home/alden/.cache/cal_monthly.png", month_int=current_month
        )
        monthly_cal.draw_calendar()
        annual_cal = services.AccountabilityYearlyCalendar(
            save_path="/home/alden/.cache/cal_annual.png"
        )
        annual_cal.draw_calendar()
