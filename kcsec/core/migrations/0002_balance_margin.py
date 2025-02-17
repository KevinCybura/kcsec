# Generated by Django 3.1.2 on 2020-11-03 13:15

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_portfolio"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="balance",
            field=models.DecimalField(decimal_places=4, default=0, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="portfolio",
            name="margin",
            field=models.DecimalField(decimal_places=4, default=0, max_digits=15),
            preserve_default=False,
        ),
    ]
