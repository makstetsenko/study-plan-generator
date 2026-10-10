from src.esh_journal_excel.excel_mapper import map_to_excel_plan
from src.esh_journal_excel.excel_plan import write_excel_plan_to_file
import src.docx.docx_plan as docx
import src.studying_plan as studying_plan
from src.app_args import get_app_args, AppArgs
from src.docx.docx_mapper import map_to_docx_plan


def write_excel(app_args: AppArgs, studying_plan_data: studying_plan.StudyingPlan):    
    excel_plan = map_to_excel_plan(studying_plan_data)
    write_excel_plan_to_file(excel_plan, app_args.excel_template_path, app_args.output_dir_path) # type: ignore


def write_docx(app_args: AppArgs, studying_plan_data: studying_plan.StudyingPlan):
    docx_plan = map_to_docx_plan(studying_plan_data)

    docx.render_and_save_docx(
        template_path=app_args.docx_template_path, # type: ignore
        data=docx_plan,
        output_path=app_args.output_dir_path.joinpath(
            f"{studying_plan_data.academic_year}-{studying_plan_data.subject.name}-{studying_plan_data.class_name}.docx"
        ),
    )


def main():
    app_args: AppArgs = get_app_args()

    studying_plan_data = studying_plan.read_plan_from_yml([app_args.common_data_yml_path, app_args.topics_yml_path])

    if not app_args.docx_template_path is None:
        write_docx(app_args, studying_plan_data)

    if not app_args.excel_template_path is None:
        write_excel(app_args, studying_plan_data)


if __name__ == "__main__":
    main()
