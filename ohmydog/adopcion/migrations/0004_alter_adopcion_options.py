# Generated by Django 4.2 on 2023-05-06 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adopcion', '0003_alter_adopcion_created_alter_adopcion_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adopcion',
            options={'verbose_name': 'adopcion', 'verbose_name_plural': 'adopciones'},
        ),
    ]
