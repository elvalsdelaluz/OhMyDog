# Generated by Django 4.1.7 on 2023-06-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donacion', '0007_alter_donacion_finalizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donacion',
            name='finalizacion',
            field=models.DateField(),
        ),
    ]
