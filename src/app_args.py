import argparse
import pathlib
import pydantic


class AppArgs(pydantic.BaseModel):
    docx_template_path: pathlib.Path | None
    excel_template_path: pathlib.Path | None
    topics_yml_path: pathlib.Path
    common_data_yml_path: pathlib.Path
    output_dir_path: pathlib.Path


def raise_if_invalid_file_path(path: pathlib.Path, arg_name: str):
    if not path.exists():
        raise ValueError(f"{arg_name} file does not exist by path {path.as_posix()}")

    if not path.is_file():
        raise ValueError(f"Specified {arg_name} path {path.as_posix()} is not a file")


def get_app_args() -> AppArgs:
    parser = argparse.ArgumentParser()

    template_group = parser.add_mutually_exclusive_group(required=True)
    template_group.add_argument("--docx-template")
    template_group.add_argument("--excel-template")

    parser.add_argument("--common-data-yml-path", default="./data/common.yml")
    parser.add_argument("--topics-yml-path", required=True)
    parser.add_argument("--output-dir", default="./output")

    args = parser.parse_args()

    app_params = AppArgs(
        docx_template_path=pathlib.Path(args.docx_template) if not args.docx_template is None else None,
        excel_template_path=pathlib.Path(args.excel_template) if not args.excel_template is None else None,
        topics_yml_path=pathlib.Path(args.topics_yml_path),
        common_data_yml_path=pathlib.Path(args.common_data_yml_path),
        output_dir_path=pathlib.Path(args.output_dir),
    )

    raise_if_invalid_file_path(app_params.topics_yml_path, "--topics-yml-path")
    raise_if_invalid_file_path(app_params.common_data_yml_path, "--common-data-yml-path")

    if app_params.excel_template_path is None and app_params.docx_template_path is None:
        raise ValueError("Either --docx-template or --excel-template must be provided")

    if not app_params.excel_template_path is None:
        raise_if_invalid_file_path(app_params.excel_template_path, "--excel-template")

    if not app_params.docx_template_path is None:
        raise_if_invalid_file_path(app_params.docx_template_path, "--docx-template")

    app_params.output_dir_path.mkdir(exist_ok=True)

    return app_params
