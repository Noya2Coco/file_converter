import uuid
from django.db import models
from django.conf import settings

from converter.utils import handle_conversion_error
from .storage import OverwriteStorage
from .converters import convert_file

class Conversion(models.Model):
    input_file = models.FileField(upload_to='uploads/', storage=OverwriteStorage())
    output_file = models.FileField(upload_to='converted/', blank=True, null=True, storage=OverwriteStorage())
    source_format = models.CharField(max_length=10)
    target_format = models.CharField(max_length=10)
    converted = models.BooleanField(default=False)
    error_message = models.CharField(max_length=255, blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.source_format} to {self.target_format}"

    def convert_file(self):
        """Gère la conversion des fichiers en utilisant les modules de convertisseurs."""
        try:
            convert_file(self)
        except Exception as e:
            handle_conversion_error(self, e)
