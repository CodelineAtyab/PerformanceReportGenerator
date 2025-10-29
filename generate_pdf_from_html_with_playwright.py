import os
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_REPORTS_DIR = os.path.join(BASE_DIR, 'output_reports_html')
PDF_OUTPUT_DIR = os.path.join(BASE_DIR, 'output_reports_pdf')


def generate_pdf_from_html_playwright(html_file_path, pdf_output_path):
    """
    Converts an HTML file to PDF using Playwright (better JavaScript support).
    
    :param html_file_path: Full path to the input HTML file.
    :param pdf_output_path: Full path for the output PDF file.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Load HTML file
            page.goto(f'file:///{html_file_path.replace(os.sep, "/")}')
            
            # Wait for Chart.js to render
            page.wait_for_timeout(3000)  # 3 seconds for chart rendering
            
            # Generate PDF
            page.pdf(
                path=pdf_output_path,
                format='A4',
                margin={
                    'top': '10mm',
                    'right': '10mm',
                    'bottom': '10mm',
                    'left': '10mm'
                },
                print_background=True
            )
            
            browser.close()
        
        print(f"✓ Successfully generated PDF: {os.path.basename(pdf_output_path)}")
        
    except Exception as e:
        print(f"✗ Failed to generate PDF for {os.path.basename(html_file_path)}: {e}")


def main():
    """
    Converts all HTML reports to PDF using Playwright.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(PDF_OUTPUT_DIR):
        os.makedirs(PDF_OUTPUT_DIR)
        print(f"Created directory: {PDF_OUTPUT_DIR}\n")
    
    # Get all HTML files
    html_files = [f for f in os.listdir(HTML_REPORTS_DIR) if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found in output_reports_html directory.")
        return
    
    print(f"Found {len(html_files)} HTML report(s). Starting conversion with Playwright...\n")
    
    # Convert each HTML file to PDF
    for html_filename in html_files:
        html_path = os.path.join(HTML_REPORTS_DIR, html_filename)
        pdf_filename = html_filename.replace('.html', '.pdf')
        pdf_path = os.path.join(PDF_OUTPUT_DIR, pdf_filename)
        
        generate_pdf_from_html_playwright(html_path, pdf_path)
    
    print(f"\nConversion complete! PDFs saved to: {PDF_OUTPUT_DIR}")


if __name__ == '__main__':
    main()
