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


class AccountabilityYearlyCalendar:
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

    def __init__(self, save_path: str):
        self.save_path = save_path
        self.img = Image.new("RGB", size=(1920, 1080), color=(255, 255, 255))

        # create new blank picture
        width, height = self.img.size

        # self.rows = 2 titles + 6 self.rows of days + 2(head + footer)blank
        # self.cols = 7 self.cols of week + 1 blank for left + 3 col for pic
        self.left_padding = 2
        self.top_padding = 3
        self.rows = (self.top_padding + 6) * 3
        self.cols = (self.left_padding + len(self.WEEK)) * 4
        self.col_size = width // self.cols
        self.row_size = height // self.rows
        self.line_size = self.row_size // 10
        self.month_size = 34
        self.title_size = 22
        self.day_size = 28
        self.month_font = "/usr/share/fonts/TTF/Inconsolata-Bold.ttf"
        self.title_font = "/usr/share/fonts/TTF/Inconsolata-Bold.ttf"
        self.day_font = "/usr/share/fonts/TTF/Inconsolata-Regular.ttf"

        self.draw = ImageDraw.Draw(self.img)
        habit_completions = HabitCompletion.objects.select_related("habit")
        self.accountability_stats = self.generate_stats_dict(habit_completions)

    @staticmethod
    def generate_stats_dict(completion_entries):
        stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for entry in completion_entries:
            if entry.did_complete:
                stats[entry.create_ts.month][entry.create_ts.day][
                    "completed_habits"
                ].append(entry.habit)
            else:
                stats[entry.create_ts.month][entry.create_ts.day][
                    "incomplete_habits"
                ].append(entry.habit)
        print(stats)
        return stats

    def add_month_name(self, name, col, row):
        self.draw.text(
            (self.col_size * col - 1, self.row_size * row - 3 * self.row_size),
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
                (self.col_size * col - 3 - self.col_size * self.left_padding // 2, 0),
                (
                    self.col_size * col - 3 - self.col_size * self.left_padding // 2,
                    1080,
                ),
            ],
            fill=(0, 0, 0),
        )

    def add_horizontal_lines(self, col, row):
        self.draw.line(
            xy=[
                (self.col_size * col, (self.row_size * row - 3) - self.line_size * 2),
                (
                    (self.col_size * col - 1) * 7,
                    (self.row_size * row - 3) - self.line_size * 2,
                ),
            ],
            fill=(0, 0, 0),
        )
        self.draw.line(
            xy=[
                (
                    self.col_size * col - 1,
                    (self.row_size * row - 3) - self.line_size * 1,
                ),
                (
                    (self.col_size * col - 1) * 7,
                    (self.row_size * row - 3) - self.line_size * 1,
                ),
            ],
            fill=(0, 0, 0),
        )

    def draw_week_day_names(self, col, row):
        for i in range(len(self.WEEK)):
            # draw week title
            x = self.col_size * col + i * self.col_size
            y = self.row_size * row - self.row_size
            self.draw.text(
                (x, y),
                self.WEEK[i],
                font=ImageFont.truetype(
                    self.title_font,
                    size=self.title_size,
                    layout_engine=ImageFont.LAYOUT_BASIC,
                    encoding="unic",
                ),
                fill=(0, 0, 0),
            )

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
                        # draw green
                        self.draw.rectangle(
                            [
                                (col * self.col_size, self.row_size * row),
                                (
                                    col * self.col_size + self.col_size / 4 * 3,
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
                                    col * self.col_size + self.col_size / 4 * 3,
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
                    (self.col_size * col + self.col_size / 4, self.row_size * row),
                    str(day),
                    font=ImageFont.truetype(
                        self.day_font,
                        size=self.day_size,
                        layout_engine=ImageFont.LAYOUT_BASIC,
                        encoding="unic",
                    ),
                    fill=fill,
                )
            col += 1
            relative_col += 1
            if relative_col % 8 == 0:
                col -= 7
                relative_col -= 7
                row += 1

        return col, row

    def draw_calendar(self):
        row = 3
        col = 1
        month_starting_row = row
        for c, month in enumerate(self.MONTH):
            row = month_starting_row
            if not c == 0 and c % 4 == 0:
                col = 1
                row += self.top_padding + 6
                month_starting_row = row

            # draw month title and line
            self.add_month_name(self.MONTH[c], col, row)
            self.add_vertical_line(col)
            self.add_horizontal_lines(col, row)
            self.draw_week_day_names(col, row)
            col, row = self.draw_week_days(self.MONTH.index(month) + 1, col, row)
            col = (c + 1) % 4 * (7 + self.left_padding)

        self.img.save(self.save_path)
