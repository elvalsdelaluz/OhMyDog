# Generated by Django 4.2 on 2023-05-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0009_remove_turno_descuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='descuento',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
