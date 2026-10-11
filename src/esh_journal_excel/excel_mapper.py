from src.esh_journal_excel.excel_plan import ExcelPlan, ExcelPlanRow
from src.studying_plan import StudyingPlan


def map_to_excel_plan(plan: StudyingPlan) -> ExcelPlan:

    rows = []
    topic_counter = 0
    lesson_counter = 0
    for index_s, semester in enumerate(plan.semesters):
        for _, topic in enumerate(semester.topics):
            topic_counter += 1
            for _, lesson in enumerate(topic.lessons):
                lesson_counter += 1
                rows.append(
                    ExcelPlanRow(
                        semester_number=index_s + 1,
                        topic_number=topic_counter,
                        topic=topic.title,
                        lesson_number=lesson_counter,
                        lesson_name=f"{lesson.safety_topic} {lesson.group_results} {lesson.topic}",
                        homework=lesson.homework,
                    )
                )

    return ExcelPlan(
        rows=rows,
        class_name=plan.class_name,
        academic_year=plan.academic_year,
        subject_name=plan.subject.name,
        individual_student_name_gent=plan.individual_student_name_gent,
    )
