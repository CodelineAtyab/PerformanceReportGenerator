import src.transform_sp_excel_performance_to_json as transform_sp_excel_performance_to_json
import src.transform_sp_json_to_eval_report_json as transform_sp_json_to_eval_report_json
import src.generate_html_reports as generate_html_reports
import src.generate_doc_from_html as generate_doc_from_html
import src.generate_pdf_from_html_with_playwright as generate_pdf_from_html_with_playwright
import src.generate_pdf_from_doc as generate_pdf_from_doc


if __name__ == '__main__':
    print("=" * 60)
    print("Performance Report Generator - Full Pipeline")
    print("=" * 60)
    
    # Step 1: Transform Sharepoint Excel performance data to JSON
    print("\n[Stage 1/6] Excel → Aggregate JSON")
    transform_sp_excel_performance_to_json.main()

    # Step 2: Transform JSON data in step 1 to evaluation report JSON data
    print("\n[Stage 2/6] Aggregate JSON → Individual Report JSONs")
    transform_sp_json_to_eval_report_json.main()

    # Step 3: Use the evaluation report JSON data to generate .html reports for all team members
    print("\n[Stage 3/6] Individual JSONs → HTML Reports")
    generate_html_reports.main()

    # Step 4: Generate DOC reports for all HTML reports
    print("\n[Stage 4/6] HTML → DOC Reports")
    generate_doc_from_html.main()

    # Step 5: Generate PDFs from DOC reports for consistent formatting (alternative but dependant method)
    print("\n[Stage 5/6] DOC → PDF Reports (docx2pdf)")
    generate_pdf_from_doc.main()

    # Step Optional: Generate PDFs from HTML reports (alternative and independent method)
    # print("\n[Stage (Optional)] HTML → PDF Reports (Playwright)")
    # generate_pdf_from_html_with_playwright.main()
    
    print("\n" + "=" * 60)
    print("Pipeline execution complete!")
    print("=" * 60)