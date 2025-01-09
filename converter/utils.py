import os

def is_file_created(file_path):
    """Vérifie si un fichier a été créé."""
    return os.path.isfile(file_path)

def delete_temporary_files(directory):
    """Supprime tous les fichiers temporaires d'un répertoire."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def normalize_format(format_name):
    """Normalise les formats de fichier pour cohérence."""
    if format_name.lower() == "jpg":
        return "jpeg"
    return format_name.lower()

def unsupported_format(instance):
    """Gère les formats non supportés."""
    handle_conversion_error(instance, f"Unsupported conversion: {instance.source_format} to {instance.target_format}")

def conversion_default_exception(instance, e):
    """Gère les exceptions de conversion par défaut."""
    handle_conversion_error(instance, f"Error during conversion: {e}")
    
def handle_conversion_error(instance, error_message):
    """Met à jour l'instance avec une erreur de conversion."""
    instance.converted = False
    instance.error_message = error_message
    instance.save()
