# Generated by Django 4.2 on 2023-07-03 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactoPaseadoresCuidadores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='baja',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]