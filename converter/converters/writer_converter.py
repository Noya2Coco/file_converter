import os
import subprocess
from docx import Document
from fpdf import FPDF
import pandas as pd
from django.conf import settings
from converter.utils import conversion_default_exception, is_file_created


def convert_writer_to_pdf(instance):
    """Convertit des documents (docx, odt, txt, xlsx, pptx) en PDF."""
    try:
        file_name = os.path.basename(instance.input_file.name)
        file_root, _ = os.path.splitext(file_name)
        pdf_path = os.path.join(settings.MEDIA_ROOT, f"converted/{file_root}.pdf")

        # Conversion en fonction du format source
        if instance.source_format == "docx":
            _convert_docx_to_pdf(instance.input_file.path, pdf_path)
        elif instance.source_format == "odt":
            _convert_via_libreoffice(instance.input_file.path, pdf_path, "pdf")
        elif instance.source_format == "txt":
            _convert_txt_to_pdf(instance.input_file.path, pdf_path)
        elif instance.source_format == "xlsx":
            _convert_xlsx_to_pdf(instance.input_file.path, pdf_path)
        elif instance.source_format == "pptx":
            _convert_via_libreoffice(instance.input_file.path, pdf_path, "pdf")
        else:
            raise ValueError(f"Unsupported document format: {instance.source_format}")

        # Vérification que le fichier a été créé
        if is_file_created(pdf_path):
            instance.output_file.name = pdf_path
            instance.converted = True
            instance.error_message = None
            instance.save()
        else:
            raise FileNotFoundError(f"PDF file not created at {pdf_path}")

    except Exception as e:
        conversion_default_exception(instance, e)


def convert_writer_to_writer(instance):
    """Convertit des documents entre eux (docx, odt, txt, xlsx, pptx)."""
    try:
        file_name = os.path.basename(instance.input_file.name)
        file_root, _ = os.path.splitext(file_name)
        output_path = os.path.join(settings.MEDIA_ROOT, f"converted/{file_root}.{instance.target_format}")

        # Conversion via LibreOffice
        _convert_via_libreoffice(instance.input_file.path, output_path, instance.target_format)

        # Vérification que le fichier de sortie a été créé
        if is_file_created(output_path):
            instance.output_file.name = output_path
            instance.converted = True
            instance.error_message = None
            instance.save()
        else:
            raise FileNotFoundError(f"Converted file not created at {output_path}")

    except Exception as e:
        conversion_default_exception(instance, e)


def _convert_docx_to_pdf(input_path, output_path):
    """Convertit un fichier DOCX en PDF."""
    try:
        doc = Document(input_path)
        doc.save(output_path)
    except Exception as e:
        raise ValueError(f"Error during DOCX to PDF conversion: {e}")


def _convert_txt_to_pdf(input_path, output_path):
    """Convertit un fichier TXT en PDF."""
    try:
        with open(input_path, 'r') as txt_file:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in txt_file:
                pdf.cell(200, 10, txt=line.strip(), ln=True)
            pdf.output(output_path)
    except Exception as e:
        raise ValueError(f"Error during TXT to PDF conversion: {e}")


def _convert_xlsx_to_pdf(input_path, output_path):
    """Convertit un fichier XLSX en PDF."""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        data = pd.ExcelFile(input_path)
        for sheet_name in data.sheet_names:
            sheet = data.parse(sheet_name)
            pdf.cell(200, 10, txt=f"Sheet: {sheet_name}", ln=True)
            for row in sheet.itertuples(index=False):
                row_text = " | ".join(map(str, row))
                pdf.cell(200, 10, txt=row_text, ln=True)
        pdf.output(output_path)
    except Exception as e:
        raise ValueError(f"Error during XLSX to PDF conversion: {e}")


def _convert_via_libreoffice(input_path, output_path, target_format):
    """Convertit un fichier via LibreOffice."""
    try:
        command = [
            "soffice",
            "--headless",
            "--invisible",
            "--convert-to", target_format,
            "--outdir", os.path.dirname(output_path),
            input_path,
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    except Exception as e:
        raise ValueError(f"Error during conversion via LibreOffice: {e}")
