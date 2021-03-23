# Generated by Django 3.1.6 on 2021-03-22 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, max_length=120, null=True)),
                ('language', models.CharField(blank=True, max_length=120, null=True)),
                ('isAdult', models.BooleanField(blank=True, null=True)),
                ('movie_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Movies.movie')),
            ],
        ),
    ]
