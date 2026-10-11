import pathlib

from src.esh_journal_excel.excel_mapper import map_to_excel_plan
from src.esh_journal_excel.excel_plan import write_excel_plan_to_file
import src.docx.docx_plan as docx
import src.studying_plan as studying_plan
from src.app_args import get_app_args, AppArgs
from src.docx.docx_mapper import map_to_docx_plan


def write_excel(app_args: AppArgs, studying_plan_data: studying_plan.StudyingPlan):
    excel_plan = map_to_excel_plan(studying_plan_data)
    write_excel_plan_to_file(excel_plan, app_args.excel_template_path, app_args.output_dir_path)  # type: ignore


def write_docx(app_args: AppArgs, studying_plan_data: studying_plan.StudyingPlan):
    docx_plan = map_to_docx_plan(studying_plan_data)
    individual_name = (
        ""
        if studying_plan_data.individual_student_name_gent is None
        else "_" + studying_plan_data.individual_student_name_gent
    )

    docx.render_and_save_docx(
        template_path=app_args.docx_template_path,  # type: ignore
        data=docx_plan,
        output_path=app_args.output_dir_path.joinpath(
            f"{studying_plan_data.academic_year}_{studying_plan_data.subject.name}_{studying_plan_data.class_name}{individual_name}.docx"
        ),
    )

def generate_plan_from_yml(app_args: AppArgs, topics_yml_path: pathlib.Path):
    studying_plan_data = studying_plan.read_plan_from_yml([app_args.common_data_yml_path, topics_yml_path])

    if not app_args.docx_template_path is None:
        write_docx(app_args, studying_plan_data)

    if not app_args.excel_template_path is None:
        write_excel(app_args, studying_plan_data)


def main():
    app_args: AppArgs = get_app_args()

    if not app_args.topics_yml_path is None:
        generate_plan_from_yml(app_args, app_args.topics_yml_path)
        return

    assert app_args.topics_dir_path is not None

    for yml_path in app_args.topics_dir_path.glob(pattern="*.yml"):
        if yml_path.samefile(app_args.common_data_yml_path):
            continue
        generate_plan_from_yml(app_args, yml_path)
        


if __name__ == "__main__":
    main()
