import os
import uuid
import csv
from PIL import Image
from django.conf import settings
from django.test import TestCase
from docx import Document

from converter.models import Conversion


class ConversionTestCase(TestCase):
    def setUp(self):
        """Initialise les variables de test et crée les dossiers nécessaires."""
        self.test_id = uuid.uuid4().hex  # Identifiant unique pour ce test
        self.uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(self.uploads_dir, exist_ok=True)
        self.generated_files = []  # Liste des fichiers générés pour les supprimer après les tests
        self.result_matrix = []  # Matrice des résultats des conversions
        self.supported_formats = ["png", "jpeg", "jpg", "bmp", "tiff", "gif", "webp", "ico", "docx", "odt", "txt", "xlsx", "pptx", "pdf"]

    def test_conversion_matrix(self):
        """Teste toutes les combinaisons de conversion et génère une matrice de résultats."""
        for source_format in self.supported_formats:
            row = [source_format]  # Chaque ligne commence par le format source
            for target_format in self.supported_formats:
                if source_format == target_format:
                    row.append("N/A")  # Pas de conversion si les formats sont identiques
                else:
                    file_name = f"test_{source_format}_{self.test_id}.{source_format}"
                    file_path = self.create_fake_file(file_name, source_format)
                    conversion = self.create_conversion(file_path, source_format, target_format)
                    try:
                        conversion.convert_file()
                        if conversion.converted:
                            row.append("✔")  # Conversion réussie
                        else:
                            row.append("✖")  # Conversion échouée
                            #row.append(f"✖ ({conversion.error_message})")  # Conversion échouée
                    except Exception as e:
                        row.append("✖")  # Erreur inattendue
                        #row.append(f"✖ (Exception: {str(e)})")  # Erreur inattendue
            self.result_matrix.append(row)

        # Sauvegarder la matrice des résultats
        self.save_result_matrix()

    def create_conversion(self, file_path, source_format, target_format):
        """Crée une instance de Conversion."""
        self.generated_files.append(file_path)  # Enregistre le fichier source pour suppression
        return Conversion(input_file=file_path, source_format=source_format, target_format=target_format)

    def create_fake_file(self, file_name, file_type):
        """Crée un fichier factice pour un format donné."""
        file_path = os.path.join(self.uploads_dir, file_name)
        if file_type == "docx":
            doc = Document()
            doc.add_paragraph("This is a test DOCX file.")
            doc.save(file_path)
        elif file_type in ["odt", "txt"]:
            with open(file_path, "w") as f:
                f.write("This is a test file.")
        elif file_type == "pdf":
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Test PDF", ln=True)
            pdf.output(file_path)
        elif file_type == "xlsx":
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws["A1"] = "Test XLSX"
            wb.save(file_path)
        elif file_type == "pptx":
            from pptx import Presentation
            presentation = Presentation()
            slide = presentation.slides.add_slide(presentation.slide_layouts[0])
            slide.shapes.title.text = "Test Presentation"
            slide.placeholders[1].text = "This is a test slide for conversion."
            presentation.save(file_path)
        elif file_type in ["png", "jpeg", "jpg", "bmp", "tiff", "gif", "webp", "ico"]:
            image = Image.new('RGB', (100, 100), color=(255, 0, 0))
            image.save(file_path)
        self.generated_files.append(file_path)
        return file_path

    def save_result_matrix(self):
        """Sauvegarde la matrice des résultats dans un fichier CSV."""
        result_path = os.path.join(settings.MEDIA_ROOT, "conversion_results.csv")
        with open(result_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            # En-têtes (formats cible)
            writer.writerow(["Source \ Target"] + self.supported_formats)
            # Écriture des lignes
            for row in self.result_matrix:
                writer.writerow(row)
        print(f"Résultats des conversions sauvegardés dans {result_path}")

    def tearDown(self):
        """Nettoie les fichiers générés après les tests."""
        for file_path in self.generated_files:
            if os.path.exists(file_path):
                os.remove(file_path)
