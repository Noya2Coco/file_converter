import os
from PIL import Image
from django.conf import settings

from converter.utils import conversion_default_exception

def convert_image(instance):
    try:
        file_name = os.path.basename(instance.input_file.name)
        file_root, _ = os.path.splitext(file_name)
        target_path = os.path.join(settings.MEDIA_ROOT, f"converted/{file_root}.{instance.target_format}")

        format_to_save = "JPEG" if instance.target_format.lower() in ["jpg", "jpeg"] else instance.target_format.upper()

        img = Image.open(instance.input_file.path).convert("RGB")
        img.save(target_path, format_to_save)
        instance.output_file.name = target_path
        instance.converted = True
        instance.error_message = None
        instance.save()
    except Exception as e:
        conversion_default_exception(instance, e)
