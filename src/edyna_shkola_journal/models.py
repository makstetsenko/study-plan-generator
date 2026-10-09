from pydantic import BaseModel


class Lesson(BaseModel):
    topic: str
    notes: str | None
    homework: str | None


class Theme(BaseModel):
    title: str
    lessons: list[Lesson]


class Semester(BaseModel):
    semester: int
    themes: list[Theme]


class LessonXlsxRow(BaseModel):
    semester_number: int
    theme_title: str
    lesson_topic: str
    notes: str
    homework: str
