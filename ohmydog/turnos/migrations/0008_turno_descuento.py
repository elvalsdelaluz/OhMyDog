# Generated by Django 4.2 on 2023-05-20 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0007_alter_turno_monto'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='descuento',
            field=models.BooleanField(default=False),
        ),
    ]
