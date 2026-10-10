# Topics generator

Use this app to generate DOCX and Excel files (for Єдина школа journal).

Configure topics in yml file. Examples are in `./example` directory.

## Usage

To generate docx:

```bash
python main.py --docx-template templates/plan_without_group_results.docx --common-data-yml-path 'data/календарки/інформатика/common.yml' --topics-yml-path 'data/календарки/інформатика/5-Б.yml'
```

To generate excel:

```bash
python main.py --excel-template templates/topics-template.xlsx --common-data-yml-path 'data/календарки/інформатика/common.yml' --topics-yml-path 'data/календарки/інформатика/5-Б.yml'
```
