# Generated by Django 4.1.7 on 2023-07-02 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perdidaBusqueda', '0005_alter_perroperdido_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perroperdido',
            name='fecha_nacimiento',
            field=models.DateField(default=None, null=True),
        ),
    ]