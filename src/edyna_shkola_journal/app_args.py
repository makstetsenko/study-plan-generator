import argparse
import pathlib
import pydantic


class AppArgs(pydantic.BaseModel):
    topics_path: pathlib.Path
    output_path: pathlib.Path
    semester: str
    class_name: str
    studying_grade: str


def get_app_args() -> AppArgs:
    parser = argparse.ArgumentParser()

    parser.add_argument("--topics", required=True, help="Path to xlsx topics file")
    parser.add_argument("--output", required=True, help="Path to output yml file where topics will be placed")
    parser.add_argument("--semester", required=True, help="Semester name like '1 семестр'")
    parser.add_argument("--class-name", required=True, help="Class name like '5-А' or just '5'")
    parser.add_argument("--studying-grade", required=True, help="Grading class like '5 клас' or '6 клас'")

    args = parser.parse_args()

    app_params = AppArgs(
        topics_path=pathlib.Path(args.topics),
        output_path=pathlib.Path(args.output),
        semester=args.semester,
        class_name=args.class_name,
        studying_grade=args.studying_grade,
    )

    if not app_params.topics_path.exists():
        raise ValueError(f"Topics file does not exist by path {app_params.topics_path.as_posix()}")

    if not app_params.topics_path.is_file():
        raise ValueError(f"Specified topics path {app_params.topics_path.as_posix()} is not a file")

    app_params.output_path.parent.mkdir(exist_ok=True)

    return app_params
