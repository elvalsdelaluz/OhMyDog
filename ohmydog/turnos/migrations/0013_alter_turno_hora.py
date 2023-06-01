# Generated by Django 4.2 on 2023-05-31 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0012_turno_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='hora',
            field=models.CharField(choices=[('0', '08:00 hs'), ('1', '08:30 hs'), ('2', '09:00 hs'), ('3', '09:30 hs'), ('4', '10:00 hs'), ('5', '10:30 hs'), ('6', '11:00 hs'), ('7', '11:30 hs'), ('8', '16:00 hs'), ('9', '16:30 hs'), ('10', '17:00 hs'), ('11', '17:30 hs'), ('12', '18:00 hs'), ('13', '18:30 hs'), ('14', '19:00 hs'), ('15', '19:30 hs')], max_length=8, verbose_name='Horario'),
        ),
    ]