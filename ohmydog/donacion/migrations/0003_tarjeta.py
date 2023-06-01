# Generated by Django 4.1.7 on 2023-05-31 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donacion', '0002_donante'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('numero_tarjeta', models.CharField(max_length=16)),
                ('vencimiento', models.DateField()),
                ('codigo_seguridad', models.CharField(max_length=3)),
            ],
        ),
    ]