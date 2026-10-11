# Topics generator

Use this app to generate DOCX and Excel files (for Єдина школа journal).

This is useful to keep single config file that can be used to produce both excel and docx files. Also this app calculated dates for each lessons which is incredibly useful.

Configure topics in yml file. Examples are in `./example` directory.

## Usage

### Generate from yml file and common file

To generate docx:

```bash
python main.py \
--docx-template templates/plan.docx \
--common-data-yml-path 'data/календарки/інформатика/common.yml' \
--topics-yml-path 'data/календарки/інформатика/5-Б.yml'
```

To generate excel:

```bash
python main.py \
--excel-template templates/topics-template.xlsx \
--common-data-yml-path 'data/календарки/інформатика/common.yml' \
--topics-yml-path 'data/календарки/інформатика/5-Б.yml'
```

To generate both excel and docx:

```bash
python main.py \
--excel-template templates/topics-template.xlsx \
--docx-template templates/plan.docx \
--common-data-yml-path 'data/календарки/інформатика/common.yml' \
--topics-yml-path 'data/календарки/інформатика/5-Б.yml'
```

### Generate from common file and directory with yml files

In this case common yml file will be ignored if it sits inside working directory.


```bash
python main.py \
--excel-template templates/topics-template.xlsx \
--docx-template templates/plan.docx \
--common-data-yml-path 'data/календарки/інформатика/common.yml' \
--topics-dir-path 'data/календарки/інформатика'
```

## Plan model setup

The structure of plan provided below.

Important thing is `semester.term.week_one_start`. This is the date when week A (week 1) starts. This is relevant for schedules with multiple weeks (like week A, week B etc). This property is optional. If the `term` is already starting from week A then you are good to just ignore this field. But if the term is starting from week B then you must to set the correct date when week A starting. So eventually this is reference point for correct lessons dates calculation.

```yml
academic_year: '2026-2027'

subject: 
 name: "Інформатика"
 name_gent: "Інформатики" # в родовому відмінку

teacher:
  full_name: "Стеценко Максим Віталійович"
  full_name_gent: "Стеценка Максима Віталійовича" # ПІБ в родовому відмінку

class_name: '5-Б'
individual_student_name_gent: 'Іванова Івана Івановича' # Optional. Use this if plan is mentioned for individual studying. So title will say this plan for this specific student (not for the whole class) 

semester_name_in_title: 1 і 2 семестри

schedule:
- iso_weekday: 1 # 1-Monday, 7-Sunday
  lessons_count: 2 # on this week config
  week_number: null # same every week

textbooks: # optional; can be null of subject does not have any official textbooks
- grade: 5 клас
  title: 'Н. В. Морзе, О. В. Барна M79 Інформатика: Підручник для 5 кл. закладів загальної середньої освіти / Н. В. Морзе, О. В. Барна. — Київ: УОВЦ «Оріон», 2023. - 256 с. : іл.'

programs:
- grade: 5 клас
  title: 'Типова освітня програма для 5-10(11) класів спеціальних закладів загальної середньої освіт для осіб з особливими освітніми потребами, затверджена наказом Міністерства освіти і науки України від 07.12.2021 р. № 1317, зі змінами, додаток 14'


semesters:
- topics:
  - title: Інформація
    lessons:
    - topic: Правила роботи за комп’ютером
      homework: Записати в зошит два правила безпечної роботи за комп’ютером.
      safety_topic: Первинний інструктаж з БЖД.
    - topic: Інформація та її значення в житті людини
      homework: Записати два приклади інформації, яку людина отримує щодня.
      safety_topic: Інструктаж з БЖД.
  terms:
  - start: '2026-09-01'
    end: '2026-10-25'
    week_one_start: '2026-08-31' # optional but be careful with this date.
  - start: '2026-11-02'
    end: '2026-12-23'
```