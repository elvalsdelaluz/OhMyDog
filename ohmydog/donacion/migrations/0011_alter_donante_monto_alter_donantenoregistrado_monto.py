# Generated by Django 4.1.7 on 2023-06-07 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donacion', '0010_donantenoregistrado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donante',
            name='monto',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6),
        ),
        migrations.AlterField(
            model_name='donantenoregistrado',
            name='monto',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6),
        ),
    ]
