import datetime

from pydantic import BaseModel
import pathlib
import yaml


class Subject(BaseModel):
    name: str
    name_gent: str


class Teacher(BaseModel):
    full_name: str
    full_name_gent: str


class Textbook(BaseModel):
    grade: str
    title: str


class StudyingProgram(BaseModel):
    grade: str
    title: str


class Lesson(BaseModel):
    topic: str
    homework: str
    safety_topic: str
    group_results: str = ""


class Topic(BaseModel):
    title: str
    lessons: list[Lesson]


class Semester(BaseModel):
    topics: list[Topic]
    terms: list[StudyingTermPeriod]


class Schedule(BaseModel):
    iso_weekday: int | None  # Monday=1, Sunday=7
    lessons_count: int = 1
    week_number: int | None = None  # None = every week


class StudyingTermPeriod(BaseModel):
    start: datetime.date  # inclusive
    end: datetime.date  # inclusive
    week_one_start: datetime.date | None = None


class StudyingPlan(BaseModel):
    subject: Subject
    teacher: Teacher
    academic_year: str
    semester_name_in_title: str
    class_name: str
    individual_student_name_gent: str | None = None
    textbooks: list[Textbook] | None = None
    programs: list[StudyingProgram]
    semesters: list[Semester]
    schedule: list[Schedule]


def read_plan_from_yml(path_list: list[pathlib.Path]):
    data: dict = {}

    # merging all info into one dictionary object
    for p in path_list:
        if not p.exists():
            raise ValueError(f"File does not exist by path: {p.as_posix()}")

        if not p.is_file():
            raise ValueError(f"Specified path {p.as_posix()} is not a file")

        with open(p.as_posix(), "r") as f:
            data = data | yaml.safe_load(f)

    return StudyingPlan.model_validate(data)
