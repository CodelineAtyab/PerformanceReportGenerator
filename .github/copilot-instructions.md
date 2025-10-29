## Architecture Overview
**Four-stage ETL pipeline**: Excel → aggregate JSON → individual report JSONs → HTML reports → PDF reports. Each stage is decoupled and can run independently.

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

### Stage 3: JSON to HTML Reports (`generate_html_reports.py`)
- Reads `transformed_data/individual_reports/*.json` and renders `templates/report_template.html` via Jinja2
- **Path resolution**: Uses `os.path.dirname(os.path.abspath(__file__))` as base; all scripts must stay at repo root
- **Batch generation**: Creates one HTML per JSON file, naming convention: `{json_name}.html`
- **Output directory**: `output_reports_html/` (changed from `output_reports/`)
- **Schema expectations**: Template requires `employee_name`, `team`, `evaluation_period`, `attendance_summary`, `sprint_velocity`, `monthly_evaluation`, `trainers_feedback`
- **Chart.js integration**: `sprint_velocity` array powers inline bar chart; expects `sprint`, `committed`, `delivered` keys; optional `plagiarism: "Yes"/"No"` drives color coding

### Stage 4: HTML to PDF Reports (`generate_pdf_with_playwright.py` - Recommended)
- Converts `output_reports_html/*.html` to PDF with full JavaScript/Chart.js support
- **Output directory**: `output_reports_pdf/`
- **Technology**: Uses Playwright with Chromium browser for accurate rendering
- **Chart rendering**: Waits 3 seconds for Chart.js to execute before PDF generation
- **PDF format**: A4 with 10mm margins, print backgrounds enabled
- **Installation**: Requires `playwright install chromium` after pip install
- **Browser location**: Chromium installs system-wide in `%LOCALAPPDATA%\ms-playwright\` (not in venv)

**Alternative: `generate_pdf_reports_using_html.py` (pdfkit - Deprecated)**
- Uses pdfkit/wkhtmltopdf (older approach with limited JavaScript support)
- Charts may not render properly; use Playwright version instead
- Requires separate wkhtmltopdf binary installation

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
python main_app.py  # Orchestrates all 4 stages
```
This imports and calls: `transform_sp_excel_performance_to_json.main()` → `transform_sp_json_to_eval_report_json.main()` → `generate_html_reports.main()` → `generate_pdf_with_playwright.main()` (if uncommented)

### Individual Stage Testing
```bash
python transform_sp_excel_performance_to_json.py     # Stage 1 only
python transform_sp_json_to_eval_report_json.py      # Stage 2 only (requires stage 1 output)
python generate_html_reports.py                      # Stage 3 only (requires stage 2 output)
python generate_pdf_with_playwright.py               # Stage 4 only (requires stage 3 output)
```

### Changelog Generation
```bash
python generate_changelog.py  # Creates CHANGELOG.md from git history
```
- Requires git installed and repository initialized
- Outputs commit history with datetime and messages
- Version info read from `version.txt`

### Adding a New Team
1. Place team's Excel file in `input_data/` (e.g., `team_new_data.xlsx`)
2. Stage 1 auto-generates `transformed_data/sharepoint_excel_to_json_data/team_new_data.json`
3. In `transform_sp_json_to_eval_report_json.py`, duplicate `generate_member_reports()` logic or modify `SOURCE_JSON` path
4. Update `TARGET_MONTHS` tuple if evaluation period differs
5. Stages 3 & 4 automatically pick up new JSON files from `individual_reports/`

### Customizing Report Content
- **Attendance data**: Edit `_build_member_payload()` in stage 2; currently returns hardcoded `total_days: 22, present_days: 22, absent_days: 0`
- **Feedback sections**: Modify `strengths`, `improvements`, `trainers_feedback` lists in same function
- **Visual styling**: Edit `templates/report_template.html` inline `<style>` block; Chart.js config is in inline `<script>` at bottom

## Project Conventions

### File Paths & Directory Structure
- All Python scripts resolve paths relative to their own location via `os.path.dirname(os.path.abspath(__file__))` or `Path(__file__).resolve().parent`
- Maintain flat repo structure (scripts at root) to prevent path resolution failures
- `utils/` exists but is unused; shared functions should go here with coordinated naming
- **Output directories**: `output_reports_html/` for HTML, `output_reports_pdf/` for PDF

### JSON Serialization
- **Always use** `ensure_ascii=False` in `json.dump()` to preserve non-English characters (feedback often contains Arabic text)
- Use `indent=2` or `indent=4` for human-readable output (all stages do this)

### Excel Column Matching
- Header matching is case-insensitive and uses substring checks: `if any(keyword in header.lower() for keyword in [...])`
- When adding new metrics, update filter list in `extract_row_data()` in stage 1

### Error Handling
- Stage 1 wraps per-file processing in try/except, prints errors but continues batch
- Stage 2/3 assume valid input; add validation if processing untrusted data
- Stage 4 wraps conversion in try/except per file
- No automated tests; verify by opening `output_reports_html/*.html` in browser and checking chart rendering

### Performance Considerations
- Stage 1 uses `openpyxl` with `data_only=True` (reads cached values, not formulas) for speed
- Batch generation creates 20+ HTML files in seconds; no optimization needed for current scale
- Stage 4 (Playwright) takes ~3-5 seconds per PDF due to browser startup and chart rendering
- If adding many teams, consider parallel processing in stage 3/4 loops

### Version Management
- Current version stored in `version.txt` (plain text, single line)
- Changelog generated via `generate_changelog.py` from git commit history
- Format: `- [YYYY-MM-DD HH:MM:SS] <commit message>`

## Debugging Common Issues

**"Template not found"**: Ensure `templates/` is sibling to script; check `TEMPLATE_PARENT_DIR` path construction

**Missing members in reports**: Verify Excel column A has no empty cells before "Sprint No." row; check sheet name contains valid month

**Chart not rendering in HTML**: Open browser console; ensure `sprint_velocity` array exists and has `sprint`/`committed`/`delivered` keys

**Chart not rendering in PDF**: 
- Use `generate_pdf_with_playwright.py` (not pdfkit version)
- Verify Playwright installed: `playwright install chromium`
- Increase `page.wait_for_timeout(3000)` to `5000` for slower systems
- Check Chromium installed at: `%LOCALAPPDATA%\ms-playwright\chromium-*`

**Wrong sprint weights**: September/October sprints are 10% (not 50%); check month-specific logic in `_build_sprint_velocity()`

**Non-English characters broken**: Confirm `encoding='utf-8'` and `ensure_ascii=False` in all file I/O operations

**Playwright errors**: 
- Run `playwright install` to download browsers
- Chromium binary is system-wide (~200MB in `AppData\Local\ms-playwright\`)
- If venv deleted, browser remains; no reinstall needed for new venvs

**Git not found for changelog**: Install Git and ensure it's in system PATH; verify with `git --version`

## Dependencies
- **Jinja2** (3.1.6): Template rendering
- **openpyxl** (3.1.5): Excel parsing
- **pdfkit** (1.0.0): PDF generation (deprecated, use Playwright)
- **Playwright** (1.55.0): Modern PDF generation with JS support (recommended)

Install: `pip install -r requirements.txt && playwright install chromium`
