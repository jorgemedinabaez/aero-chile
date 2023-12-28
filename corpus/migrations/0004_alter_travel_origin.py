# Generated by Django 4.0.5 on 2023-12-13 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0003_remove_passenger_travels_id_alter_travel_destination_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='origin',
            field=models.CharField(choices=[('Santiago', 'Santiago - Chile'), ('Lima', 'Lima - Perú'), ('Buenos Aires', 'Buenos Aires - Argentina'), ('La Paz', 'La Paz - Bolivia'), ('Quito', 'Quito - Ecuador')], default='Santiago - Chile', max_length=45, verbose_name='Origen de vuelo'),
        ),
    ]