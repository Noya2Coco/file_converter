from django.db import migrations, models
import uuid

def generate_unique_tokens(apps, schema_editor):
    Conversion = apps.get_model('converter', 'Conversion')
    for conversion in Conversion.objects.all():
        conversion.token = uuid.uuid4()
        conversion.save()

class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0002_conversion_error_message'),  # Remplacez par votre dernière migration
    ]

    operations = [
        migrations.AddField(
            model_name='conversion',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.RunPython(generate_unique_tokens),  # Génère des tokens pour les entrées existantes
    ]
