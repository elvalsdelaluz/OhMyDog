# Generated by Django 4.2 on 2023-05-20 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='descuento',
            field=models.BooleanField(default=False),
        ),
    ]
