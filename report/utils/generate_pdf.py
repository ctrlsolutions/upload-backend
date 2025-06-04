import os
import subprocess
from django.template.loader import render_to_string
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfMerger

WEASYPRINT_PATH = r"D:\weasyprint\dist\weasyprint.exe"

def generate_pdf(template_name, context):
    html_string = render_to_string(template_name, context)

    # Save HTML to a temp file
    with NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as html_file:
        html_file.write(html_string)
        html_path = html_file.name

    # Create temporary output PDF file
    output_pdf = NamedTemporaryFile(delete=False, suffix=".pdf")
    output_pdf.close()  # Close so weasyprint.exe can write to it

    # Run the WeasyPrint executable
    result = subprocess.run([
        WEASYPRINT_PATH,
        html_path,
        output_pdf.name
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"WeasyPrint failed: {result.stderr}")

    # Clean up HTML temp file
    try:
        os.unlink(html_path)
    except FileNotFoundError:
        pass

    return open(output_pdf.name, "rb")  # Return file handle for use in merging

def generate_merged_pdf(sections):
    """
    sections: List of (template_name, context) tuples
    """
    pdf_files = [generate_pdf(template, ctx) for template, ctx in sections]

    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    output = NamedTemporaryFile(delete=False, suffix=".pdf")
    output.close()

    merger.write(output.name)
    merger.close()

    # Clean up temp PDFs
    for pdf in pdf_files:
        try:
            pdf.close()
            os.unlink(pdf.name)
        except FileNotFoundError:
            pass

    return open(output.name, "rb")
