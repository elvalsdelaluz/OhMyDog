# Generated by Django 4.1.7 on 2023-05-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0008_alter_mascota_raza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradalibretasanitaria',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
