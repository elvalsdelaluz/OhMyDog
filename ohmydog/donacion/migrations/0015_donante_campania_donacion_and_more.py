# Generated by Django 4.2 on 2023-06-07 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donacion', '0014_remove_donante_campaña_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donante',
            name='campania_donacion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='donacion.donacion'),
        ),
        migrations.AddField(
            model_name='donantenoregistrado',
            name='campania_donacion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='donacion.donacion'),
        ),
    ]