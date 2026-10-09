# Convert Excel file with topics into yml file for further usage to make docx calendar planning

from edyna_shkola_journal.app_args import get_app_args
from src.edyna_shkola_journal.data_reader import get_semesters
from src.edyna_shkola_journal.data_writer import save_as_yml_plan

app_params = get_app_args()

semesters = get_semesters(app_params.topics_path)

save_as_yml_plan(
    semesters, app_params.output_path, app_params.class_name, app_params.studying_grade, app_params.semester
)
