# Generated by Django 4.0.3 on 2022-04-22 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MARS', '0014_search_movies_search_onas_search_ovas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animeentry',
            name='mean',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
    ]
