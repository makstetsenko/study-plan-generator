from dataclasses import dataclass
from pathlib import Path

from openpyxl import load_workbook


@dataclass
class ExcelPlanRow:
    semester_number: int
    topic_number: int
    topic: str
    lesson_number: int
    lesson_name: str
    homework: str


@dataclass
class ExcelPlan:
    rows: list[ExcelPlanRow]
    class_name: str
    subject_name: str
    academic_year: str
    individual_student_name_gent: str | None = None


COLUMN_MAPPING = {
    "B": "semester_number",
    "D": "topic_number",
    "E": "topic",
    "G": "lesson_number",
    "H": "lesson_name",
    "J": "homework",
}

START_ROW = 6


def write_excel_plan_to_file(
    plan: ExcelPlan,
    template_path: Path,
    output_dir_path: Path,
) -> None:
    workbook = load_workbook(template_path)
    sheet = workbook.active

    if sheet is None:
        raise ValueError("Active sheet is None")

    for row_number, plan_row in enumerate(plan.rows, start=START_ROW):
        for column, attribute in COLUMN_MAPPING.items():
            sheet[f"{column}{row_number}"] = getattr(plan_row, attribute)

    individual_name = "" if plan.individual_student_name_gent is None else "_" + plan.individual_student_name_gent

    workbook.save(
        output_dir_path.joinpath(f"{plan.academic_year}_{plan.subject_name}_{plan.class_name}{individual_name}.xlsx")
    )
