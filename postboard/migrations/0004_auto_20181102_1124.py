# Generated by Django 2.1.2 on 2018-11-02 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postboard', '0003_auto_20181031_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='djangoboard',
            name='file',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='djangoboard',
            name='place',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]