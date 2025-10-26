## Codebase Fast Facts
- Python 3.11 project that turns structured Excel performance trackers into HTML reports.
- Core scripts: `transform_sp_excel_performance_to_json.py` (Excel ➜ JSON) and `main_generate_report.py` (dict ➜ Jinja2 HTML).
- Key folders: `input_data/` raw spreadsheets, `transformed_data/` JSON exports, `templates/` Jinja layouts, `output_reports/` generated HTML.
- Dependencies are lightweight: Jinja2 3.1.6 and openpyxl 3.1.5; avoid introducing heavier stacks unless justified.

## Data Transformation Flow
- `transform_sp_excel_performance_to_json.py` scans `input_data/*.xlsx`; skip non-month sheets via `VALID_MONTHS` (full and abbreviated names).
- Excel layout assumptions: column A lists team members until a "Sprint No." row; row 1 headers label metrics pulled for each person.
- Sprint metadata lives under the "Sprint No." block (number, URL, name across columns A-C) and is emitted as `sheet_data["sprint_info"]`.
- Output JSON structure: `{sheet_name: {"Member Name": [[header, value], ...], "sprint_info": {...}}}`; honor this shape when consuming or extending the pipeline.

## Report Generation Flow
- `generate_evaluation_report(data, template_name, output_filename)` loads templates from `templates/` and writes to `output_reports/`; base paths derive from `__file__`, so keep scripts beside assets.
- Expected data schema mirrors the sample `report_data` in `main_generate_report.py` (keys like `attendance_summary`, `sprint_velocity`, `monthly_evaluation`, `trainers_feedback`).
- When wiring transformed JSON into reports, map the list-of-pairs format into richer dicts before rendering; avoid pushing raw arrays directly into the template.
- Reports overwrite files with the same name; pick unique `output_filename` when generating multiple variants.

## Template & Frontend Notes
- `templates/report_template.html` is a self-contained Jinja template with inline styles and a Chart.js bar chart loaded via CDN.
- Chart labels and datasets expect `sprint_velocity` entries with `sprint`, `committed`, `delivered`, and a `plagiarism` flag of `"Yes"/"No"` to drive color coding.
- Attendance and evaluation sections guard against missing data; pass empty lists rather than `None` to suppress conditional blocks cleanly.
- If customizing visuals, retain the `sprintVelocityChart` canvas id or update the inline script accordingly.

## Developer Workflow
- Create a virtual environment and install `requirements.txt` before running scripts (`python -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt`).
- Regenerate JSON assets with `python transform_sp_excel_performance_to_json.py`; the script creates `transformed_data/` if needed and logs successes.
- Build reports via `python main_generate_report.py` or import `generate_evaluation_report` from other tooling for batch generation.
- `output_reports/evaluation_report.html` serves as the canonical example output—update it when the template or sample data changes to keep reviewers aligned.

## Conventions & Gotchas
- File paths resolve from script directories; keep related assets in sibling folders to avoid broken lookups.
- JSON writer uses `ensure_ascii=False` so non-English feedback remains intact—preserve this when refactoring serialization.
- The empty `utils/` directory is a staging area for shared helpers; coordinate naming before introducing modules to avoid top-level clutter.
- No automated tests yet; manual inspection of generated HTML in a browser is the current verification path.
