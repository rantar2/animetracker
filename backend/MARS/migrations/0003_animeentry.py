# Generated by Django 4.0.3 on 2022-03-17 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MARS', '0002_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('rank', models.IntegerField()),
                ('genres', models.CharField(max_length=120)),
            ],
        ),
    ]
