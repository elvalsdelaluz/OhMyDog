# Generated by Django 4.1.7 on 2023-05-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0002_rename_entrada_libreta_sanitaria_entradalibretasanitaria_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mascota',
            old_name='nacimiento',
            new_name='fecha_nacimiento',
        ),
        migrations.AddField(
            model_name='mascota',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
