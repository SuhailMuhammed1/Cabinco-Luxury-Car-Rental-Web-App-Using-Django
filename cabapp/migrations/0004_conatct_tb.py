# Generated by Django 3.1.5 on 2023-08-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabapp', '0003_car_tb'),
    ]

    operations = [
        migrations.CreateModel(
            name='conatct_tb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('message', models.CharField(default='', max_length=300)),
            ],
        ),
    ]