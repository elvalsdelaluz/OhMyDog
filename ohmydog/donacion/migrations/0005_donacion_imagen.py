# Generated by Django 4.1.7 on 2023-06-01 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donacion', '0004_delete_tarjeta'),
    ]

    operations = [
        migrations.AddField(
            model_name='donacion',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='donacion'),
        ),
    ]
