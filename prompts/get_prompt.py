import sys

semester_1_lessons = sys.argv[1]
semester_2_lessons = sys.argv[2]
prompt_template_path = sys.argv[3]


with open(prompt_template_path, "r") as f:
    prompt_text = f.read()


prompt_text = prompt_text.replace("@SEMESTER_1_LESSONS", semester_1_lessons)
prompt_text = prompt_text.replace("@SEMESTER_2_LESSONS", semester_2_lessons)
prompt_text = prompt_text.replace("@TOTAL_LESSONS", str(int(semester_1_lessons) + int(semester_2_lessons)))

print(prompt_text)
