import src.docx_plan as docx
import src.studying_plan as studying_plan
from src.app_args import get_app_args, AppArgs
from src.mapper import map_to_docx_plan

def main():
    app_args: AppArgs = get_app_args()

    studying_plan_data = studying_plan.read_plan_from_yml([app_args.common_data_yml_path, app_args.topics_yml_path])
    docx_plan = map_to_docx_plan(studying_plan_data)

    docx.render_and_save_docx(
        template_path=app_args.docx_template_path,
        data=docx_plan,
        output_path=app_args.output_dir_path.joinpath(
            f"{studying_plan_data.academic_year}-{studying_plan_data.subject.name}-{studying_plan_data.class_name}.docx"
        ),
    )



if __name__ == "__main__":
    main()