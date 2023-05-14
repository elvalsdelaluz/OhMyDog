# Generated by Django 4.1.7 on 2023-05-13 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adopcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('edad', models.IntegerField()),
                ('comentarios', models.CharField(max_length=100)),
                ('sexo', models.CharField(choices=[('0', 'Hembra'), ('1', 'Macho'), ('2', 'Ns/Nc')], max_length=1, verbose_name='Sexo')),
                ('tamaño', models.CharField(choices=[('0', 'Chico: entre 3 y 10 kilos'), ('1', 'Mediano: entre 10 y 25 kilos'), ('2', 'Grande: entre 25 y 50 kilos'), ('3', 'Gigante: más de 50 kilos')], max_length=1, verbose_name='Tamaño')),
                ('estado', models.CharField(choices=[('0', 'En adopción'), ('1', 'Adoptado')], max_length=1, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'adopcion',
                'verbose_name_plural': 'adopciones',
            },
        ),
    ]
