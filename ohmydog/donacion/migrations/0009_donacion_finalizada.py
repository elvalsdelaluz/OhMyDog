# Generated by Django 4.2 on 2023-06-05 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donacion', '0008_alter_donacion_finalizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='donacion',
            name='finalizada',
            field=models.BooleanField(default=False),
        ),
    ]
