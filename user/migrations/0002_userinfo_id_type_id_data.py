# Generated by Django 4.1.7 on 2023-03-22 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='id_type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='id_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_name', models.CharField(max_length=100, null=True)),
                ('id_dob', models.DateField(null=True)),
                ('id_fulldata', models.CharField(max_length=10000)),
                ('userid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.userinfo')),
            ],
        ),
    ]
