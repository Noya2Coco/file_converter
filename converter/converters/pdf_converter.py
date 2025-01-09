import os
from pdf2image import convert_from_path
from zipfile import ZipFile
from django.conf import settings
from converter.utils import conversion_default_exception, delete_temporary_files

def convert_pdf_to_images(instance):
    """Convertit un fichier PDF en images et les sauvegarde dans un fichier ZIP."""
    try:
        # Déterminer le chemin vers Poppler si nécessaire
        poppler_path = None
        if os.name == "nt":  # Windows
            poppler_path = r"C:/Program Files/poppler-24.08.0/Library/bin"

        # Création du répertoire temporaire
        temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
        os.makedirs(temp_dir, exist_ok=True)

        fmt = "JPEG" if instance.target_format.lower() in ["jpg", "jpeg"] else instance.target_format.upper()

        # Conversion du PDF en images
        images = convert_from_path(
            instance.input_file.path,
            output_folder=temp_dir,
            fmt=fmt,
            poppler_path=poppler_path
        )

        # Création du fichier ZIP
        file_name = os.path.basename(instance.input_file.name)
        file_root, _ = os.path.splitext(file_name)
        zip_path = os.path.join(settings.MEDIA_ROOT, f"converted/{file_root}.zip")

        with ZipFile(zip_path, "w") as zipf:
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f"page_{i + 1}.{instance.target_format}")
                try:
                    image.save(image_path, fmt.upper())
                    zipf.write(image_path, os.path.basename(image_path))
                except Exception as e:
                    raise ValueError(f"Error saving image {i + 1}: {e}")

        # Mise à jour de l'instance après succès
        instance.output_file.name = zip_path
        instance.converted = True
        instance.error_message = None
        instance.save()

    except Exception as e:
        conversion_default_exception(instance, e)
    finally:
        delete_temporary_files(temp_dir)
