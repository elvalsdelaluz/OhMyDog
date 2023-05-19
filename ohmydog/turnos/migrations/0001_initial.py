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
            name='Turno',
            fields=[
                ('mascota', models.CharField(max_length=20)),
                ('motivo', models.CharField(choices=[('0', 'Consulta General'), ('1', 'Vacuna A'), ('2', 'Vacuna B'), ('3', 'Desparasitacion'), ('4', 'Urgencia Intermedia'), ('5', 'Castracion')], max_length=1, verbose_name='Motivo')),
                ('franja_horaria', models.CharField(choices=[('0', 'Mañana'), ('1', 'Tarde')], max_length=1, verbose_name='Franja horaria')),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('0', 'Pendiente'), ('1', 'Aceptado'), ('2', 'Rechazado'), ('3', 'Cancelado'), ('4', 'Cerrado')], max_length=1, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dueño', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'turno',
                'verbose_name_plural': 'turnos',
            },
        ),
    ]