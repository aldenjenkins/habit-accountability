import argparse
import calendar
import csv
import random
import pytz

from django.utils import timezone
from collections import defaultdict
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from habits.mods.accountability.models import Habit, HabitCompletion

WEEK = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")
MONTH = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

def generate_stats_dict(completion_entries):
    stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in completion_entries:
        if entry.did_complete and entry.create_ts > entry.habit.create_ts:
            stats[timezone.localtime(entry.create_ts).month][timezone.localtime(entry.create_ts).day][
                "completed_habits"
            ].append(entry.habit)
        elif entry.create_ts > entry.habit.create_ts:
            stats[timezone.localtime(entry.create_ts).month][timezone.localtime(entry.create_ts).day][
                "incompleted_habits"
            ].append(entry.habit)
    return stats


class CalendarMixin:
    num_calendars_per_row = 4
    left_padding = 2
    top_padding = 3
    num_calendars_to_show = 12

    def __init__(self, save_path: str):
        self.save_path = save_path
        self.img = Image.new("RGB", size=(1920, 1080), color=(255, 255, 255))

        # create new blank picture
        width, height = self.img.size

        # self.rows = 2 titles + 6 self.rows of days + 2(head + footer)blank
        # self.cols = 7 self.cols of week + 1 blank for left + 3 col for pic
        self.rows = (self.top_padding + 6) * (self.num_calendars_to_show / self.num_calendars_per_row)
        self.cols = (self.left_padding + len(WEEK)) * self.num_calendars_per_row
        self.col_size = width // self.cols
        self.row_size = height // self.rows
        self.line_size = self.row_size // 10
        self.month_font = "/usr/share/fonts/TTF/Inconsolata-Bold.ttf"
        self.title_font = "/usr/share/fonts/TTF/Inconsolata-Bold.ttf"
        self.day_font = "/usr/share/fonts/TTF/Inconsolata-Regular.ttf"

        self.draw = ImageDraw.Draw(self.img)
        habit_completions = HabitCompletion.objects.select_related("habit")
        self.accountability_stats = generate_stats_dict(habit_completions)

    def add_month_name(self, name, col, row):
        self.draw.text(
            (self.col_size * col - 1, self.row_size * row - 2 * self.row_size),
            name,
            fill=(
                0,
                0,
                0,
            ),
            font=ImageFont.truetype(
                self.month_font,
                size=self.month_size,
                layout_engine=ImageFont.LAYOUT_BASIC,
                encoding="unic",
            ),
            size=self.month_size,
        )

    def add_vertical_line(self, col):
        self.draw.line(
            xy=[
                (self.col_size * col - self.col_size * self.left_padding // 2, 0),
                (
                    self.col_size * col - self.col_size * self.left_padding // 2,
                    1080,
                ),
            ],
            fill=(0, 0, 0),
        )

    def draw_day_border(self, col, row):
        pass

    def add_horizontal_lines(self, col, row):
        self.draw.line(
            xy=[
                (
                    self.col_size * col,
                    (self.row_size * row - 4) - self.line_size * 2
                ),
                (
                    (self.col_size * col - 2) + self.col_size * 7,
                    (self.row_size * row - 3) - self.line_size * 2,
                ),
            ],
            fill=(0, 0, 0),
        )
        self.draw.line(
            xy=[
                (
                    self.col_size * col - 1,
                    (self.row_size * row - 4) - self.line_size,
                ),
                (
                    (self.col_size * col - 2) + self.col_size * 7,
                    (self.row_size * row - 4) - self.line_size,
                ),
            ],
            fill=(0, 0, 0),
        )

    def draw_week_day_names(self, col, row):
        for c, week in enumerate(WEEK):
            # draw week title
            x = col * self.col_size + c * self.col_size
            y = self.row_size * row - self.row_size
            self.draw.text(
                (x, y),
                week,
                font=ImageFont.truetype(
                    self.title_font,
                    size=self.title_size,
                    layout_engine=ImageFont.LAYOUT_BASIC,
                    encoding="unic",
                ),
                fill=(0, 0, 0),
            )

    def draw_habits(self, col, row, month, day):
        pass

    def draw_week_days(self, month, col, row) -> (int, int):
        cal = calendar.Calendar(firstweekday=0)
        relative_col = 1
        current_date = timezone.now()
        for cnt, day in enumerate(cal.itermonthdays(timezone.now().year, month)):
            if day > 0:
                if (
                    pytz.utc.localize(
                        datetime.strptime(
                            f"{month},{day},{current_date.year}", "%m,%d,%Y"
                        )
                    )
                    <= current_date
                ):
                    if (
                        len(self.accountability_stats[month][day]["completed_habits"])
                        >= 5
                    ):
                        # Draw green
                        self.draw.rectangle(
                            [
                                (col * self.col_size, self.row_size * row),
                                (
                                    col * self.col_size + self.col_size,
                                    row * self.row_size + self.row_size,
                                ),
                            ],
                            fill=(0, 255, 0),
                        )
                    else:
                        # Draw yellow
                        self.draw.rectangle(
                            [
                                (col * self.col_size, self.row_size * row),
                                (
                                    col * self.col_size + self.col_size,
                                    row * self.row_size + self.row_size,
                                ),
                            ],
                            fill=(255, 255, 0),
                        )
                # if weekend, draw with red color
                if relative_col % 6 == 0 or relative_col % 7 == 0:
                    fill = (255, 0, 0)
                else:
                    fill = (0, 0, 0)
                self.draw.text(
                    (self.col_size * col + self.col_size / 2, self.row_size * row),
                    str(day),
                    font=ImageFont.truetype(
                        self.day_font,
                        size=self.day_size,
                        layout_engine=ImageFont.LAYOUT_BASIC,
                        encoding="unic",
                    ),
                    fill=fill,
                )
                self.draw_habits(col, row, month, day)
                self.draw_day_border(col, row)

            col += 1
            relative_col += 1
            if relative_col % 8 == 0:
                col -= 7
                relative_col -= 7
                row += 1

        return col, row


class AccountabilityMonthlyCalendar(CalendarMixin):
    num_calendars_per_row = 1
    month_size = 80
    title_size = 40
    day_size = 20
    habit_size = 10
    top_padding = 2
    left_padding = 0.5
    num_calendars_to_show = 1

    def __init__(self, save_path: str, month_int: int):
        super().__init__(save_path)
        self.month_int = month_int

    def draw_calendar(self):
        row = self.top_padding
        col = self.left_padding

        self.add_month_name(MONTH[self.month_int - 1], col, row)
        self.add_horizontal_lines(col, row)
        self.draw_week_day_names(col, row)
        self.draw_week_days(self.month_int, col, row)
        self.img.save(self.save_path)

    def draw_day_border(self, col, row):
        # Top border
        self.draw.line(
            xy=[
                (self.col_size * col, row * self.row_size),
                (self.col_size * col + self.col_size, row * self.row_size),
            ],
            fill=(0, 0, 0),
        )
        # Bottom Border
        self.draw.line(
            xy=[
                (self.col_size * col, row * self.row_size + self.row_size),
                (self.col_size * col + self.col_size, row * self.row_size + self.row_size),
            ],
            fill=(0, 0, 0),
        )
        # Left Border
        self.draw.line(
            xy=[
                (self.col_size * col, row * self.row_size),
                (self.col_size * col, row * self.row_size + self.row_size),
            ],
            fill=(0, 0, 0),
        )
        # Right Border
        self.draw.line(
            xy=[
                (self.col_size * col, row * self.row_size),
                (self.col_size * col, row * self.row_size + self.row_size),
            ],
            fill=(0, 0, 0),
        )


    def draw_habits(self, col, row, month, day):
        rel_row = 0
        rel_col = 0
        for habit in self.accountability_stats[month][day]["completed_habits"]:
            print_row = row * self.row_size + self.day_size + self.habit_size * rel_row
            print_col = self.col_size * col + rel_col * (self.col_size/2)
            self.draw.text(
                (print_col, print_row),
                # TODO: change to habit short name
                '* ' + habit.name,
                font=ImageFont.truetype(
                    self.day_font,
                    size=self.habit_size,
                    layout_engine=ImageFont.LAYOUT_BASIC,
                    encoding="unic",
                ),
                fill=(0, 0, 0),
            )
            #if (print_row + self.habit_size) > (row * self.row_size):
            #    rel_row = 0
            #    col += 
            #else:
            rel_row += 1
        rel_col = 1
        rel_row = 0
        for habit in self.accountability_stats[month][day]["incompleted_habits"]:
            print_row = row * self.row_size + self.day_size + self.habit_size * rel_row
            print_col = self.col_size * col + rel_col * (self.col_size/2)
            self.draw.text(
                (print_col, print_row),
                # TODO: change to habit short name
                '* ' + habit.name,
                font=ImageFont.truetype(
                    self.day_font,
                    size=self.habit_size,
                    layout_engine=ImageFont.LAYOUT_BASIC,
                    encoding="unic",
                ),
                fill=(255, 0, 0),
            )
            #if (print_row + self.habit_size) > (row * self.row_size):
            #    rel_row = 0
            #    col += 
            #else:
            rel_row += 1


class AccountabilityYearlyCalendar(CalendarMixin):
    month_size = 34
    title_size = 22
    day_size = 28

    def draw_calendar(self):
        row = 3
        col = 1
        month_starting_row = row
        for c, month in enumerate(MONTH):
            row = month_starting_row
            if not c == 0 and c % self.num_calendars_per_row == 0:
                col = 1
                row += self.top_padding + 6
                month_starting_row = row

            # draw month title and line
            self.add_month_name(MONTH[c], col, row)
            self.add_vertical_line(col)
            self.add_horizontal_lines(col, row)
            self.draw_week_day_names(col, row)
            col, row = self.draw_week_days(MONTH.index(month) + 1, col, row)
            col = (c + 1) % self.num_calendars_per_row * (7 + self.left_padding)

        self.img.save(self.save_path)
