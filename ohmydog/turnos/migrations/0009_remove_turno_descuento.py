# Generated by Django 4.2 on 2023-05-20 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0008_turno_descuento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='descuento',
        ),
    ]
