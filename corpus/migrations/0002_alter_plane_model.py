# Generated by Django 4.0.5 on 2023-12-12 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plane',
            name='model',
            field=models.CharField(default='A320 Neo - ', max_length=45, unique=True, verbose_name='Modelo avión'),
        ),
    ]