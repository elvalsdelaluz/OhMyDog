# Generated by Django 4.2 on 2023-05-06 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Sexo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sexo', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tamaño',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamaño', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='adopcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('edad', models.IntegerField()),
                ('comentarios', models.CharField(max_length=100)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adopcion.estado')),
                ('sexo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adopcion.sexo')),
                ('tamaño', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adopcion.tamaño')),
            ],
        ),
    ]
