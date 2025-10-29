# Performance Report Generator

A three-stage ETL pipeline for transforming Excel performance data into professional HTML and PDF evaluation reports with interactive Chart.js visualizations.

## Overview

This project automates the generation of employee performance reports from SharePoint Excel files, producing both HTML and PDF outputs with sprint velocity charts, monthly evaluations, and trainer feedback.

## Architecture

**Three-Stage ETL Pipeline:**

1. **Stage 1: Excel → Aggregate JSON** (`transform_sp_excel_performance_to_json.py`)
   - Ingests `input_data/*.xlsx` files
   - Produces team-level JSON in `transformed_data/sharepoint_excel_to_json_data/`
   - Extracts member performance metrics and sprint metadata

2. **Stage 2: Aggregate JSON → Individual Report JSONs** (`transform_sp_json_to_eval_report_json.py`)
   - Transforms team JSON into per-member reports
   - Outputs to `transformed_data/individual_reports/*.json`
   - Normalizes scores and generates monthly notes

3. **Stage 3: JSON → HTML Reports** (`generate_html_reports.py`)
   - Renders `templates/report_template.html` via Jinja2
   - Outputs to `output_reports_html/*.html`
   - Includes Chart.js visualizations

4. **Stage 4 (Optional): HTML → PDF Reports** (`generate_pdf_with_playwright.py`)
   - Converts HTML reports to PDF with chart rendering
   - Outputs to `output_reports_pdf/*.pdf`
   - Uses Playwright for JavaScript/Chart.js support

## Project Structure

```
PerformanceReportGenerator/
├── input_data/                          # Source Excel files
│   └── *.xlsx
├── transformed_data/
│   ├── sharepoint_excel_to_json_data/   # Stage 1 output
│   └── individual_reports/              # Stage 2 output
├── output_reports_html/                 # Stage 3 output (HTML)
├── output_reports_pdf/                  # Stage 4 output (PDF)
├── templates/
│   └── report_template.html             # Jinja2 template
├── schema/
│   └── report_schema.json               # JSON schema for validation
├── transform_sp_excel_performance_to_json.py    # Stage 1
├── transform_sp_json_to_eval_report_json.py     # Stage 2
├── generate_html_reports.py                     # Stage 3
├── generate_pdf_reports_using_html.py           # Stage 4 (pdfkit - deprecated)
├── generate_pdf_with_playwright.py              # Stage 4 (Playwright - recommended)
├── generate_changelog.py                        # Changelog generator
├── main_app.py                                  # Pipeline orchestrator
├── requirements.txt                             # Python dependencies
├── version.txt                                  # Current version
└── README.md
```

## Installation

### Prerequisites

- Python 3.8+
- Git (for changelog generation)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PerformanceReportGenerator
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers (for PDF generation):**
   ```bash
   playwright install chromium
   ```
   *Note: Chromium (~200MB) installs system-wide in `C:\Users\<User>\AppData\Local\ms-playwright\`*

## How to Run

### Full Pipeline Execution

To run all stages (Excel → JSON → HTML → PDF):

```bash
python main_app.py
```

**Pipeline stages executed:**
1. Excel files → Aggregate JSON
2. Aggregate JSON → Individual report JSONs
3. Individual JSONs → HTML reports
4. HTML reports → PDF reports (if uncommented in `main_app.py`)

### Individual Stage Testing

Run stages independently for debugging or partial processing:

```bash
# Stage 1 only: Excel to aggregate JSON
python transform_sp_excel_performance_to_json.py

# Stage 2 only: Aggregate JSON to individual reports (requires Stage 1 output)
python transform_sp_json_to_eval_report_json.py

# Stage 3 only: Generate HTML reports (requires Stage 2 output)
python generate_html_reports.py

# Stage 4 only: Generate PDF reports (requires Stage 3 output)
python generate_pdf_with_playwright.py
```

### Generate Changelog

```bash
python generate_changelog.py
```

This creates `CHANGELOG.md` with git commit history.

## Configuration

### Input Data Requirements

**Excel File Structure:**
- Column A: Team member names (until "Sprint No." marker row)
- Row 1: Metric column headers
- Sheet names: Must contain valid month names (e.g., "April 2025", "May", etc.)
- Metrics extracted: Sprint commitments, Mini quizzes, Monthly evaluation, Final evaluation, Hackathon, Total score

**Place Excel files in:** `input_data/`

### Customizing Reports

**Modify attendance data:**
- Edit `_build_member_payload()` in `transform_sp_json_to_eval_report_json.py`

**Update feedback templates:**
- Modify `strengths`, `improvements`, `trainers_feedback` in same function

**Change visual styling:**
- Edit `templates/report_template.html` (inline `<style>` and Chart.js config)

### Target Months

To change evaluation period, update `TARGET_MONTHS` tuple in `transform_sp_json_to_eval_report_json.py`:

```python
TARGET_MONTHS = ('April 2025', 'May 2025', 'June 2025', 'July 2025', 'August 2025', 'September 2025', 'October 2025')
```

## Dependencies

- **Jinja2** (3.1.6): HTML template rendering
- **openpyxl** (3.1.5): Excel file parsing
- **pdfkit** (1.0.0): PDF generation (requires wkhtmltopdf - deprecated)
- **Playwright** (1.55.0): Modern PDF generation with JavaScript support (recommended)

**Install all:**
```bash
pip install -r requirements.txt
playwright install chromium
```

## Output

### HTML Reports (`output_reports_html/`)
- Interactive Chart.js bar charts
- Responsive design
- Viewable in any browser

### PDF Reports (`output_reports_pdf/`)
- A4 format with 10mm margins
- Embedded Chart.js visualizations
- Professional formatting

## Troubleshooting

**"Template not found"**
- Verify `templates/` folder exists alongside scripts
- Check `TEMPLATE_PARENT_DIR` path in `generate_html_reports.py`

**Missing members in reports**
- Verify Excel column A has no empty cells before "Sprint No." row
- Check sheet names contain valid month names

**Charts not rendering in PDF**
- Use `generate_pdf_with_playwright.py` (not pdfkit version)
- Ensure Playwright Chromium is installed: `playwright install chromium`
- Increase `page.wait_for_timeout()` value for slower systems

**Wrong sprint weights**
- September/October use 10% sprint weight (not 50%)
- Check month-specific logic in `_build_sprint_velocity()`

**Non-English characters broken**
- Confirm `encoding='utf-8'` in all file operations
- Verify `ensure_ascii=False` in `json.dump()` calls

## Version

Current version: **1.0.0** (see `version.txt`)

## Contact

syed.atyab.hussain@gmail.com