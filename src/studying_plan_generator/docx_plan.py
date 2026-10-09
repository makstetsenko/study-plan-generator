import docxtpl
import pathlib


from pydantic import BaseModel


class DocxSubject(BaseModel):
    name: str
    name_gent: str


class DocxTeacher(BaseModel):
    full_name: str
    full_name_gent: str


class DocxHours(BaseModel):
    semester: int
    hours_per_semester: int
    per_week: float
    diagnostic_works_count: int


class DocxTextbook(BaseModel):
    grade: str
    title: str


class DocxStudyingProgram(BaseModel):
    grade: str
    title: str


class DocxLesson(BaseModel):
    topic: str
    homework: str
    group_results: str
    number: int
    date: str


class DocxSemesterTheme(BaseModel):
    title: str
    number: int
    lessons: list[DocxLesson]


class DocxSemester(BaseModel):
    semester_number: int
    themes: list[DocxSemesterTheme]


class DocxStudyingPlan(BaseModel):
    class_name: str
    semester_name_in_title: str
    hours: list[DocxHours]
    textbooks: list[DocxTextbook]
    programs: list[DocxStudyingProgram]
    plan: list[DocxSemester]
    subject: DocxSubject
    teacher: DocxTeacher
    academic_year: str


def render_and_save_docx(template_path: pathlib.Path, data: DocxStudyingPlan, output_path: pathlib.Path) -> None:
    if not template_path.exists():
        raise ValueError(f"Template file does not exist by path {template_path.as_posix()}")

    if not template_path.is_file():
        raise ValueError(f"Specified template path {template_path.as_posix()} is not a file")

    doc = docxtpl.DocxTemplate(template_file=template_path.as_posix())
    doc.render(data.model_dump())
    doc.save(output_path.as_posix())
