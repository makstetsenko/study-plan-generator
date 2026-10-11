import argparse
import pathlib
import pydantic


class AppArgs(pydantic.BaseModel):
    docx_template_path: pathlib.Path | None
    excel_template_path: pathlib.Path | None
    topics_yml_path: pathlib.Path | None
    topics_dir_path: pathlib.Path | None
    common_data_yml_path: pathlib.Path
    output_dir_path: pathlib.Path


def raise_if_invalid_file_path(path: pathlib.Path, arg_name: str):
    if not path.exists():
        raise ValueError(f"{arg_name} file does not exist by path {path.as_posix()}")

    if not path.is_file():
        raise ValueError(f"Specified {arg_name} path {path.as_posix()} is not a file")

def raise_if_invalid_dir_path(path: pathlib.Path, arg_name: str):
    if not path.exists():
        raise ValueError(f"{arg_name} directory does not exist by path {path.as_posix()}")

    if not path.is_dir():
        raise ValueError(f"Specified {arg_name} path {path.as_posix()} is not a directory")


def get_app_args() -> AppArgs:
    parser = argparse.ArgumentParser()

    parser.add_argument("--docx-template")
    parser.add_argument("--excel-template")

    parser.add_argument("--common-data-yml-path", default="./data/common.yml")
    parser.add_argument("--output-dir", default="./output")


    template_group = parser.add_mutually_exclusive_group(required=True)
    template_group.add_argument("--topics-yml-path")
    template_group.add_argument("--topics-dir-path")

    args = parser.parse_args()

    if not args.docx_template and not args.excel_template:
        parser.error("At least one of --docx-template or --excel-template is required")

    app_params = AppArgs(
        docx_template_path=pathlib.Path(args.docx_template) if not args.docx_template is None else None,
        excel_template_path=pathlib.Path(args.excel_template) if not args.excel_template is None else None,
        topics_yml_path=pathlib.Path(args.topics_yml_path) if not args.topics_yml_path is None else None,
        common_data_yml_path=pathlib.Path(args.common_data_yml_path),
        output_dir_path=pathlib.Path(args.output_dir),
        topics_dir_path=pathlib.Path(args.topics_dir_path) if not args.topics_dir_path is None else None
    )

    if not app_params.topics_yml_path is None:
        raise_if_invalid_file_path(app_params.topics_yml_path, "--topics-yml-path")

    if not app_params.topics_dir_path is None:
        raise_if_invalid_dir_path(app_params.topics_dir_path, "--topics-dir-path")

    raise_if_invalid_file_path(app_params.common_data_yml_path, "--common-data-yml-path")

    if app_params.excel_template_path is None and app_params.docx_template_path is None:
        raise ValueError("Either --docx-template or --excel-template must be provided")

    if not app_params.excel_template_path is None:
        raise_if_invalid_file_path(app_params.excel_template_path, "--excel-template")

    if not app_params.docx_template_path is None:
        raise_if_invalid_file_path(app_params.docx_template_path, "--docx-template")

    app_params.output_dir_path.mkdir(exist_ok=True)

    return app_params
