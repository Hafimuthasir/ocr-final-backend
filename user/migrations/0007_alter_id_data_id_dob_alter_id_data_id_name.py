# Generated by Django 4.1.7 on 2023-03-22 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_id_data_id_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='id_data',
            name='id_dob',
            field=models.CharField(blank=True, default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='id_data',
            name='id_name',
            field=models.CharField(blank=True, default=1, max_length=100),
            preserve_default=False,
        ),
    ]
