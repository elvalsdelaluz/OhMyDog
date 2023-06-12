# Generated by Django 4.2 on 2023-06-12 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0015_entradalibretasanitaria_cantidad_desparasitario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradalibretasanitaria',
            name='motivo',
            field=models.CharField(choices=[('1', 'Vacuna A'), ('2', 'Vacuna B'), ('3', 'Desparasitario')], max_length=1, verbose_name='Motivo'),
        ),
    ]
