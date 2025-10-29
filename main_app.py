import src.transform_sp_excel_performance_to_json as transform_sp_excel_performance_to_json
import src.transform_sp_json_to_eval_report_json as transform_sp_json_to_eval_report_json
import src.generate_html_reports as generate_html_reports
import src.generate_pdf_from_html_with_playwright as generate_pdf_from_html_with_playwright


if __name__ == '__main__':
    print("=" * 60)
    print("Performance Report Generator - Full Pipeline")
    print("=" * 60)
    
    # Step 1: Transform Sharepoint Excel performance data to JSON
    print("\n[Stage 1/4] Excel → Aggregate JSON")
    transform_sp_excel_performance_to_json.main()

    # Step 2: Transform JSON data in step 1 to evaluation report JSON data
    print("\n[Stage 2/4] Aggregate JSON → Individual Report JSONs")
    transform_sp_json_to_eval_report_json.main()

    # Step 3: Use the evaluation report JSON data to generate .html reports for all team members
    print("\n[Stage 3/4] Individual JSONs → HTML Reports")
    generate_html_reports.main()

    # Step 4: Generate PDFs for all HTML reports
    print("\n[Stage 4/4] HTML → PDF Reports")
    generate_pdf_from_html_with_playwright.main()
    
    print("\n" + "=" * 60)
    print("Pipeline execution complete!")
    print("=" * 60)