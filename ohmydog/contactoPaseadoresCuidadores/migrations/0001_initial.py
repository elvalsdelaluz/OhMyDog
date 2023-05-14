# Generated by Django 4.1.7 on 2023-05-13 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perdidaBusqueda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
                ('apellido', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=10)),
                ('rol', models.CharField(choices=[('0', 'Paseador'), ('1', 'Cuidador')], max_length=1, verbose_name='Trabajo')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perdidaBusqueda.zona')),
            ],
            options={
                'verbose_name': 'proveedor',
                'verbose_name_plural': 'proveedores',
            },
        ),
    ]
