import argparse
import pathlib
import pydantic


class AppArgs(pydantic.BaseModel):
    docx_template_path: pathlib.Path
    topics_yml_path: pathlib.Path
    common_data_yml_path: pathlib.Path
    output_dir_path: pathlib.Path


def get_app_args() -> AppArgs:
    parser = argparse.ArgumentParser()

    parser.add_argument("--docx-template", required=True)
    parser.add_argument("--common-data-yml-path", required=False, default="./data/common.yml")
    parser.add_argument("--topics-yml-path", required=True)
    parser.add_argument("--output-dir", required=False, default="./output")

    args = parser.parse_args()

    app_params = AppArgs(
        docx_template_path=pathlib.Path(args.docx_template),
        topics_yml_path=pathlib.Path(args.topics_yml_path),
        common_data_yml_path=pathlib.Path(args.common_data_yml_path),
        output_dir_path=pathlib.Path(args.output_dir),
    )

    if not app_params.docx_template_path.exists():
        raise ValueError(f"Template file does not exist by path {app_params.docx_template_path.as_posix()}")

    if not app_params.docx_template_path.is_file():
        raise ValueError(f"Specified template path {app_params.docx_template_path.as_posix()} is not a file")

    if not app_params.topics_yml_path.exists():
        raise ValueError(f"Data file does not exist by path {app_params.topics_yml_path.as_posix()}")

    if not app_params.topics_yml_path.is_file():
        raise ValueError(f"Specified data path {app_params.topics_yml_path.as_posix()} is not a file")

    if not app_params.common_data_yml_path.exists():
        raise ValueError(f"Common data file does not exist by path {app_params.common_data_yml_path.as_posix()}")

    if not app_params.common_data_yml_path.is_file():
        raise ValueError(f"Specified common data path {app_params.common_data_yml_path.as_posix()} is not a file")

    app_params.output_dir_path.mkdir(exist_ok=True)

    return app_params
