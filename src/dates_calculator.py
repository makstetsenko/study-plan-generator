from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Term:
    start: date
    end: date
    week_one_start: date | None = None


@dataclass
class LessonSchedule:
    iso_weekday: int | None  # Monday=1, Sunday=7
    lessons_count: int = 1
    week_number: int | None = None  # None = every week


def calculate_lessons(
    terms: list[Term],
    schedules: list[LessonSchedule],
) -> list[date]:
    lesson_dates = []

    for term in terms:
        current = term.start
        week_one_start = (
            current - timedelta(days=current.weekday()) if term.week_one_start is None else term.week_one_start
        )

        while current <= term.end:
            weeks_passed = (current - week_one_start).days // 7
            current_week = (weeks_passed % 2) + 1

            for schedule in schedules:
                if schedule.iso_weekday is None:
                    continue

                if current.isoweekday() != schedule.iso_weekday:
                    continue

                if schedule.week_number is not None and schedule.week_number != current_week:
                    continue

                lesson_dates.extend([current] * schedule.lessons_count)

            current += timedelta(days=1)

    return sorted(lesson_dates)
