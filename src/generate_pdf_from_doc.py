import os
from pathlib import Path
from docx2pdf import convert


def convert_doc_to_pdf(doc_path, pdf_path):
    """Convert a .docx file to PDF using docx2pdf."""
    try:
        convert(str(doc_path), str(pdf_path))
        print(f"✓ Converted: {doc_path.name} → {pdf_path.name}")
        return True
    except Exception as e:
        print(f"✗ Error converting {doc_path.name}: {e}")
        return False


def main():
    """Main function to convert all .docx reports to PDF."""
    # Resolve paths relative to script location
    script_dir = Path(__file__).resolve().parent.parent
    doc_dir = script_dir / 'output_reports_doc'
    pdf_dir = script_dir / 'output_reports_pdf'
    
    # Create output directory if it doesn't exist
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all .docx files
    doc_files = list(doc_dir.glob('*.docx'))
    
    if not doc_files:
        print(f"No .docx files found in {doc_dir}")
        return
    
    print(f"Found {len(doc_files)} .docx file(s) to convert")
    print("-" * 60)
    
    success_count = 0
    fail_count = 0
    
    for doc_file in doc_files:
        pdf_file = pdf_dir / f"{doc_file.stem}.pdf"
        if convert_doc_to_pdf(doc_file, pdf_file):
            success_count += 1
        else:
            fail_count += 1
    
    print("-" * 60)
    print(f"Conversion complete: {success_count} successful, {fail_count} failed")


if __name__ == "__main__":
    main()
