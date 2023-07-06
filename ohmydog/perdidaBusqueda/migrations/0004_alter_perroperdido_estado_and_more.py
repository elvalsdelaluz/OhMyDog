# Generated by Django 4.1.7 on 2023-07-02 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perdidaBusqueda', '0003_alter_perroperdido_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perroperdido',
            name='estado',
            field=models.CharField(choices=[('0', 'Extraviado'), ('1', 'Encontrado'), ('2', 'Localizado')], max_length=1, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='perroperdido',
            name='fecha_nacimiento',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='perroperdido',
            name='nombre',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombre'),
        ),
    ]