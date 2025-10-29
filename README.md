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

## Usage

To generate the performance reports, you need to run a series of scripts in order. The main script orchestrates the entire process, but you can also run the steps individually.

### Running All Steps

To run all the steps and generate the final report, use the `main_generate_report.py` script:

```bash
python main_generate_report.py
```

This script will:
1. Transform the Excel data to JSON format.
2. Transform the JSON data to the evaluation report format.
3. Generate the final HTML report.

### Individual Steps

You can also run each step individually:

1. **Transform Excel to JSON:**
   ```bash
   python transform_sp_excel_performance_to_json.py
   ```

2. **Transform JSON to Evaluation Report JSON:**
   ```bash
   python transform_sp_json_to_eval_report_json.py
   ```

3. **Generate HTML Report:**
   The main script `main_generate_report.py` is responsible for this step after the previous transformations are complete.

## Features

- Generate comprehensive performance reports
- Customize report parameters
- Export reports in various formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.