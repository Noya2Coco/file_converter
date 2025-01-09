from converter.utils import conversion_default_exception, handle_conversion_error, unsupported_format
from converter.formats import image_formats, writer_formats, table_formats, slide_formats, pdf_format
from .image_converter import convert_image
from .writer_converter import (
    convert_writer_to_pdf,
    convert_writer_to_writer,
)
from .pdf_converter import convert_pdf_to_images

def convert_file(instance):
    """Effectue la conversion du fichier selon les formats source et cible."""
    from converter.utils import normalize_format

    # Normaliser les formats pour cohérence, mais permettre des conversions explicites entre JPG et JPEG
    if not (
        instance.source_format.lower() in ["jpg", "jpeg"]
        and instance.target_format.lower() in ["jpg", "jpeg"]
    ):
        instance.source_format = normalize_format(instance.source_format)
        instance.target_format = normalize_format(instance.target_format)

    # Vérifier si les formats source et cible sont identiques
    if instance.source_format == instance.target_format:
        handle_conversion_error(instance, "Source and target formats are the same. No conversion needed.")
        return

    try:
        # Redirection vers les convertisseurs selon le format
        
        # image_converter.py
        if instance.source_format in image_formats and instance.target_format in image_formats + pdf_format:
            convert_image(instance)
            
        # writer_converter.py
        elif instance.source_format in writer_formats and instance.target_format in pdf_format:
            convert_writer_to_pdf(instance)
        elif instance.source_format in writer_formats and instance.target_format in writer_formats:
            convert_writer_to_writer(instance)
            
        # table_converter.py
        
        # slide_converter.py
        
        # pdf_converter.py 
        elif instance.source_format in pdf_format and instance.target_format in image_formats:
            convert_pdf_to_images(instance)
        else:
            unsupported_format(instance)
    except Exception as e:
        conversion_default_exception(instance, e)
