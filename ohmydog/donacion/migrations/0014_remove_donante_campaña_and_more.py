# Generated by Django 4.2 on 2023-06-07 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donacion', '0013_donante_campaña_donantenoregistrado_campaña_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donante',
            name='campaña',
        ),
        migrations.RemoveField(
            model_name='donantenoregistrado',
            name='campaña',
        ),
    ]
