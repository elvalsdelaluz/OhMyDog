# Generated by Django 4.1.7 on 2023-05-14 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopcion', '0002_adopcion_dueño'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adopcion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
