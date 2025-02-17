# Generated by Django 3.1.1 on 2020-09-06 16:44

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0004_auto_20200906_1558"),
    ]

    operations = [
        migrations.AlterField(
            model_name="symbol",
            name="asset_id_base",
            field=models.ForeignKey(
                default="",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="base",
                to="crypto.asset",
            ),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="asset_id_quote",
            field=models.ForeignKey(
                default="",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="quote",
                to="crypto.asset",
            ),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="asset_id_unit",
            field=models.ForeignKey(
                default="",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="unit",
                to="crypto.asset",
            ),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="exchange",
            field=models.ForeignKey(
                default="", null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="crypto.exchange"
            ),
        ),
    ]
