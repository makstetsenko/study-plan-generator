import datetime

from src.studying_plan_generator.studying_plan import StudyingPlan, Schedule, StudyingTermPeriod
from src.studying_plan_generator.docx_plan import (
    DocxHours,
    DocxStudyingPlan,
    DocxStudyingProgram,
    DocxTextbook,
    DocxSubject,
    DocxTeacher,
    DocxSemester,
    DocxLesson,
    DocxSemesterTheme,
)
import src.studying_plan_generator.dates_calculator as dates_calculator

def get_docx_hours(semester_number: int,  diagnostic_works_count: int, class_schedule: list[Schedule], hours_per_semester: int) -> DocxHours:
    return DocxHours(
            semester=semester_number,
            per_week=sum([c.lessons_count for c in class_schedule])/len(class_schedule),
            diagnostic_works_count=diagnostic_works_count,
            hours_per_semester=hours_per_semester
        )

def get_lesson_dates(class_schedule: list[Schedule], terms: list[StudyingTermPeriod]) -> list[datetime.date]:
    lesson_schedule = [
        dates_calculator.LessonSchedule(
            weekday=c.iso_weekday - 1, lessons_count=c.lessons_count, week_number=c.week_number
        )
        for c in class_schedule
    ]
    lesson_terms = [dates_calculator.Term(start=c.start, end=c.end) for c in terms]
    return dates_calculator.calculate_lessons(
        terms=lesson_terms, schedules=lesson_schedule, week_one_start=terms[0].start
    )


def map_to_docx_plan(plan: StudyingPlan) -> DocxStudyingPlan:

    docx_plan_semesters = []
    docx_hours = []
    
    global_lessons_counter = 0
    global_themes_counter = 0

    for semester_index, semester in enumerate(plan.semesters):
        lessons_counter = 0
        lesson_dates = get_lesson_dates(class_schedule=plan.schedule, terms=semester.terms)
        
        total_lessons = len(lesson_dates)
        total_lesson_topics = sum([len(c.lessons) for c in semester.topics])
        
        if total_lessons != total_lesson_topics:
            raise Exception(f"Total topics count {total_lesson_topics} is not the same as total dates count {total_lessons} for semester {semester_index+1}")
        
        docx_themes: list[DocxSemesterTheme] = []

        for topic in semester.topics:
            global_themes_counter += 1

            docx_lessons: list[DocxLesson] = []

            for lesson in topic.lessons:
                lessons_counter += 1
                global_lessons_counter += 1

                docs_topic = f"{lesson.safety_topic} {lesson.group_results} {lesson.topic}"
                docs_topic = " ".join(docs_topic.split())  # reformat to replace multiple spaces into single spaces
                
                date = lesson_dates[lessons_counter-1]

                docx_lessons.append(
                    DocxLesson(
                        topic=docs_topic,
                        homework=lesson.homework,
                        date=date.strftime("%d/%m/%Y"),
                        number=global_lessons_counter,
                        group_results=lesson.group_results,
                    )
                )

            docx_themes.append(DocxSemesterTheme(title=topic.title, number=global_themes_counter, lessons=docx_lessons))

        docx_hours.append(get_docx_hours(semester_index + 1, semester.diagnostic_works_count, plan.schedule, total_lessons))
        docx_plan_semesters.append(DocxSemester(semester_number=semester_index + 1, themes=docx_themes))

    docx_plan = DocxStudyingPlan(
        class_name=plan.class_name,
        semester_name_in_title=plan.semester_name_in_title,
        hours=docx_hours,
        programs=[DocxStudyingProgram.model_validate(p.model_dump()) for p in plan.programs],
        textbooks=[DocxTextbook.model_validate(t.model_dump()) for t in plan.textbooks],
        teacher=DocxTeacher.model_validate(plan.teacher.model_dump()),
        subject=DocxSubject.model_validate(plan.subject.model_dump()),
        academic_year=plan.academic_year,
        plan=docx_plan_semesters,
    )

    return docx_plan
