# Generated by Django 3.1.6 on 2021-03-27 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0002_auto_20210327_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='releaseDate',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]