import transform_sp_excel_performance_to_json
import transform_sp_json_to_eval_report_json
import generate_html_reports
import generate_pdf_from_html_with_playwright


if __name__ == '__main__':
    # Step 1: Transform Sharepoint Excel performance data to JSON
    transform_sp_excel_performance_to_json.main()

    # Step 2: Transform JSON data in step 1 to evaluation report JSON data
    transform_sp_json_to_eval_report_json.main()

    # Step 3: Use the evaluation report JSON data to generate .html reports for all team members
    generate_html_reports.main()

    # Step 4: Generate a pdf for all the HTML reports
    generate_pdf_from_html_with_playwright.main()