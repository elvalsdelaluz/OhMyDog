# Generated by Django 4.1.7 on 2023-05-14 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15, unique=True)),
                ('nacimiento', models.DateField()),
                ('sexo', models.CharField(choices=[('0', 'Hembra'), ('1', 'Macho'), ('2', 'Ns/Nc')], max_length=1, verbose_name='Sexo')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('dueño', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'mascota',
                'verbose_name_plural': 'mascotas',
            },
        ),
        migrations.CreateModel(
            name='Raza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raza', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='libreta_sanitaria',
            fields=[
                ('perro', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mascotas.mascota')),
            ],
            options={
                'verbose_name': 'libreta',
            },
        ),
        migrations.AddField(
            model_name='mascota',
            name='raza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.raza'),
        ),
        migrations.CreateModel(
            name='entrada_libreta_sanitaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(choices=[('0', 'Vacuna A'), ('1', 'Vacuna B'), ('2', 'Desparasitario')], max_length=1, verbose_name='Motivo')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('libreta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.libreta_sanitaria')),
            ],
        ),
    ]
