from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Term:
    start: date
    end: date


@dataclass
class LessonSchedule:
    weekday: int  # Monday=0, Sunday=6
    lessons_count: int = 1
    week_number: int | None = None  # None = every week


def calculate_lessons(
    terms: list[Term],
    schedules: list[LessonSchedule],
    week_one_start: date,
) -> list[date]:
    lesson_dates = []

    for term in terms:
        current = term.start

        while current <= term.end:
            weeks_passed = (current - week_one_start).days // 7
            current_week = (weeks_passed % 2) + 1

            for schedule in schedules:
                if current.weekday() != schedule.weekday:
                    continue

                if schedule.week_number is not None and schedule.week_number != current_week:
                    continue

                lesson_dates.extend([current] * schedule.lessons_count)

            current += timedelta(days=1)

    return sorted(lesson_dates)
