# Performance Report Generator

A Python application that generates performance reports.

## Description

The Performance Report Generator is a tool designed to create performance reports based on input data. It provides an easy way to analyze and visualize performance metrics.

## Requirements

- Python 3.11 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/PerformanceReportGenerator.git
  cd PerformanceReportGenerator
  ```

2. Create and activate a virtual environment (optional but recommended):
  ```bash
  python -m venv venv
  # On Windows
  venv\Scripts\activate
  # On macOS/Linux
  source venv/bin/activate
  ```

3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## How to run project

### Full Pipeline Execution
To run the complete three-stage ETL pipeline (Excel → JSON → Reports):

```bash
python main_app.py
```

This orchestrates all three stages:
1. **Stage 1**: Transforms Excel files from `input_data/` to aggregate JSON in `transformed_data/sharepoint_excel_to_json_data/`
2. **Stage 2**: Converts aggregate JSON to individual member reports in `transformed_data/individual_reports/`
3. **Stage 3**: Generates HTML reports in `output_reports/`

### Running Individual Stages

If you need to run stages independently for testing or debugging:

```bash
# Stage 1 only: Excel to aggregate JSON
python transform_sp_excel_performance_to_json.py

# Stage 2 only: Aggregate JSON to individual reports (requires Stage 1 output)
python transform_sp_json_to_eval_report_json.py

# Stage 3 only: Generate HTML reports (requires Stage 2 output)
python generate_html_reports.py
```

**Note**: Each stage depends on the output of the previous stage, so ensure prerequisites exist before running individual stages.

## Features

- Generate comprehensive performance reports
- Customize report parameters
- Export reports in various formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.