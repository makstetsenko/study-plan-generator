from studying_plan_generator.studying_plan import (
    StudyingPlan,
    Semester,
    Lesson,
    Topic,
    StudyingProgram,
    Subject,
    Teacher,
    Textbook,
)
from src.edyna_shkola_journal.models import Lesson as XlsxLesson, Semester as XlsxSemester, Theme as XlsxTheme
import pathlib
import yaml

import re


def parse_topic(value: str) -> tuple[str | None, str | None, str]:
    safety_topic = None
    group_results = None

    # Extract "Інструктаж ... ."
    safety_match = re.match(r"^(Інструктаж[^.]*\.)\s*", value)
    if safety_match:
        safety_topic = safety_match.group(1)
        value = value[safety_match.end() :]

    # Extract "ГР1.", "ГР2.", etc.
    group_match = re.match(r"^(ГР\d+\.)\s*", value)
    if group_match:
        group_results = group_match.group(1)
        value = value[group_match.end() :]

    return safety_topic, group_results, value.strip()


def normalize_spaces_in_str(value: str) -> str:
    return " ".join(value.split())


def save_as_yml_plan(
    semesters: list[XlsxSemester], output_path: pathlib.Path, class_name: str, studying_grade: str, semester: str
) -> None:

    plan_semesters: list[Semester] = []

    for i,s in enumerate(semesters):

        topics: list[Topic] = []

        for t in s.themes:

            lessons: list[Lesson] = []

            for l in t.lessons:

                homework = l.homework or ""
                safety_topic, group_results, topic = parse_topic(l.topic)

                lessons.append(
                    Lesson(
                        homework=normalize_spaces_in_str(homework),
                        topic=normalize_spaces_in_str(topic),
                        group_results=normalize_spaces_in_str(group_results or l.notes or ""),
                        safety_topic=normalize_spaces_in_str(safety_topic or ""),
                    )
                )

            topics.append(Topic(title=t.title, lessons=lessons))

        plan_semesters.append(Semester(topics=topics, diagnostic_works_count=1, terms=[]))


    plan = StudyingPlan(
        class_name=class_name,
        semester_name_in_title=semester,
        semesters=plan_semesters,
        academic_year="",
        subject=Subject(name="", name_gent=""),
        teacher=Teacher(full_name="", full_name_gent=""),
        textbooks=[Textbook(grade=studying_grade, title="")],
        programs=[StudyingProgram(grade=studying_grade, title="")],
        schedule=[]
    )

    with open(output_path.as_posix(), "w") as f:
        yaml.dump(plan.model_dump(), f, allow_unicode=True, sort_keys=False)
