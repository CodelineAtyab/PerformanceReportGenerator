## Architecture Overview
**Three-stage ETL pipeline**: Excel → aggregate JSON → individual report JSONs → HTML reports. Each stage is decoupled and can run independently.

### Stage 1: Excel to Aggregate JSON (`transform_sp_excel_performance_to_json.py`)
- Ingests `input_data/*.xlsx` files and produces team-level JSON in `transformed_data/sharepoint_excel_to_json_data/`
- **Excel structure assumptions**: Column A contains team member names from row 1 until "Sprint No." marker. Row 1 headers define metric columns.
- **Sheet filtering**: Only processes sheets containing valid month names (full or abbreviated) from `calendar.month_name`/`calendar.month_abbr`
- **Sprint metadata extraction**: After "Sprint No." row, columns A/B/C hold sprint number/URL/name, emitted as `sprint_info` dict keyed by `sprint_{number}`
- **Member data format**: `{sheet_name: {"Member Name": [[header, value], ...], "sprint_info": {...}}}` — list of tuples, not dicts
- **Column filtering**: Only extracts columns matching keywords: "sprint commitments", "mini quizzes", "monthly evaluation", "final evaluation", "hackathon", "total score"

### Stage 2: Aggregate JSON to Individual Reports (`transform_sp_json_to_eval_report_json.py`)
- Transforms team JSON into per-member reports matching `schema/report_schema.json` structure
- **Month handling**: `TARGET_MONTHS` tuple defines processing window; normalizes whitespace via `_normalise_month_key()`
- **Metric extraction**: Uses specific key constants (`SPRINT_SCORE_KEY`, `QUIZ_SCORE_KEY`, etc.) to parse the `[[header, value]]` format from stage 1
- **Special month logic**: September/October use `LOW_WEIGHT_SPRINT_SCORE_KEY` (10% vs 50%) and `FINAL_EVAL_KEY` (90%) instead of monthly evaluation
- **Score normalization**: Last two months multiply percentages by 100; earlier months use raw values
- **Monthly notes**: Auto-generated via `_derive_monthly_note()` based on month and available metrics
- **Hardcoded placeholders**: Attendance, strengths/improvements, trainers_feedback use template text; customize in `_build_member_payload()`
- **Source file assumption**: Currently hardcoded to `team_code_orbit_data.json`; extend `generate_member_reports()` to support multiple teams

### Stage 3: JSON to HTML Reports (`main_generate_report.py`)
- Reads `transformed_data/individual_reports/*.json` and renders `templates/report_template.html` via Jinja2
- **Path resolution**: Uses `os.path.dirname(os.path.abspath(__file__))` as base; all scripts must stay at repo root
- **Batch generation**: `generate_all_evaluation_reports()` creates one HTML per JSON file, naming convention: `{json_name}_report.html`
- **Schema expectations**: Template requires `employee_name`, `team`, `evaluation_period`, `attendance_summary`, `sprint_velocity`, `monthly_evaluation`, `trainers_feedback`
- **Chart.js integration**: `sprint_velocity` array powers inline bar chart; expects `sprint`, `committed`, `delivered` keys; optional `plagiarism: "Yes"/"No"` drives color coding

## Data Flow & Format Contracts
```python
# Stage 1 output (aggregate JSON):
{
  "April 2025": {
    "John Doe": [
      ["Sprint commitments vs deliveries total score (out of 50%)", "35.5"],
      ["Mini Quizzes total score (out of 10%)", "8.0"]
    ],
    "sprint_info": {
      "sprint_1": {"name_of_sprint": "Intro", "url": "https://..."}
    }
  }
}

# Stage 2 output (individual JSON):
{
  "employee_name": "John Doe",
  "sprint_velocity": [
    {"sprint": "April 2025", "committed": 50.0, "delivered": 35.5}
  ],
  "monthly_evaluation": {
    "Monthly Progress": [
      {"month": "April 2025", "percentage": 43.5, "notes": "Sprint score: 35.50%, Quiz: 8.00%, Monthly evaluation: N/A."}
    ]
  }
}
```

## Critical Developer Workflows

### Full Pipeline Execution
```bash
python main_generate_report.py  # Orchestrates all 3 stages via imports
```
This imports and calls: `transform_sp_excel_performance_to_json.main()` → `transform_sp_json_to_eval_report_json.main()` → `generate_all_evaluation_reports()`

### Individual Stage Testing
```bash
python transform_sp_excel_performance_to_json.py     # Stage 1 only
python transform_sp_json_to_eval_report_json.py      # Stage 2 only (requires stage 1 output)
```

### Adding a New Team
1. Place team's Excel file in `input_data/` (e.g., `team_new_data.xlsx`)
2. Stage 1 auto-generates `transformed_data/sharepoint_excel_to_json_data/team_new_data.json`
3. In `transform_sp_json_to_eval_report_json.py`, duplicate `generate_member_reports()` logic or modify `SOURCE_JSON` path
4. Update `TARGET_MONTHS` tuple if evaluation period differs
5. Stage 3 automatically picks up new JSON files from `individual_reports/`

### Customizing Report Content
- **Attendance data**: Edit `_build_member_payload()` in stage 2; currently returns hardcoded `total_days: 22, present_days: 22, absent_days: 0`
- **Feedback sections**: Modify `strengths`, `improvements`, `trainers_feedback` lists in same function
- **Visual styling**: Edit `templates/report_template.html` inline `<style>` block; Chart.js config is in inline `<script>` at bottom

## Project Conventions

### File Paths & Directory Structure
- All Python scripts resolve paths relative to their own location via `os.path.dirname(os.path.abspath(__file__))` or `Path(__file__).resolve().parent`
- Maintain flat repo structure (scripts at root) to prevent path resolution failures
- `utils/` exists but is unused; shared functions should go here with coordinated naming

### JSON Serialization
- **Always use** `ensure_ascii=False` in `json.dump()` to preserve non-English characters (feedback often contains Arabic text)
- Use `indent=2` or `indent=4` for human-readable output (all stages do this)

### Excel Column Matching
- Header matching is case-insensitive and uses substring checks: `if any(keyword in header.lower() for keyword in [...])`
- When adding new metrics, update filter list in `extract_row_data()` in stage 1

### Error Handling
- Stage 1 wraps per-file processing in try/except, prints errors but continues batch
- Stage 2/3 assume valid input; add validation if processing untrusted data
- No automated tests; verify by opening `output_reports/*.html` in browser and checking chart rendering

### Performance Considerations
- Stage 1 uses `openpyxl` with `data_only=True` (reads cached values, not formulas) for speed
- Batch generation creates 20+ HTML files in seconds; no optimization needed for current scale
- If adding many teams, consider parallel processing in stage 3's loop

## Debugging Common Issues

**"Template not found"**: Ensure `templates/` is sibling to script; check `TEMPLATE_PARENT_DIR` path construction

**Missing members in reports**: Verify Excel column A has no empty cells before "Sprint No." row; check sheet name contains valid month

**Chart not rendering**: Open browser console; ensure `sprint_velocity` array exists and has `sprint`/`committed`/`delivered` keys

**Wrong sprint weights**: September/October sprints are 10% (not 50%); check month-specific logic in `_build_sprint_velocity()`

**Non-English characters broken**: Confirm `encoding='utf-8'` and `ensure_ascii=False` in all file I/O operations
