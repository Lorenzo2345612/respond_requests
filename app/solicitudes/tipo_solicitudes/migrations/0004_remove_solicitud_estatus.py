# Generated manually
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_solicitudes', '0003_solicitud_estatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='estatus',
        ),
    ]
