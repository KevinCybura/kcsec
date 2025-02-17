# Generated by Django 3.1 on 2020-09-06 14:59

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0002_auto_20200829_1836"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="asset",
            name="asset",
        ),
        migrations.RemoveField(
            model_name="asset",
            name="data_quote_count",
        ),
        migrations.RemoveField(
            model_name="asset",
            name="data_trade_count",
        ),
        migrations.RemoveField(
            model_name="exchange",
            name="exchange",
        ),
        migrations.RemoveField(
            model_name="symbol",
            name="id",
        ),
        migrations.AddField(
            model_name="asset",
            name="asset_id",
            field=models.CharField(
                default="back-filled-data", max_length=50, primary_key=True, serialize=False, unique=True
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="asset",
            name="data_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="asset",
            name="data_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="exchange",
            name="exchange_id",
            field=models.CharField(
                default="back-filled-data", max_length=60, primary_key=True, serialize=False, unique=True
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="asset",
            name="data_orderbook_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="data_orderbook_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="data_quote_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="data_quote_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="data_symbols_count",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="data_trade_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="data_trade_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="name",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="price_usd",
            field=models.DecimalField(decimal_places=5, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="type_is_crypto",
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="volume_1day_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="volume_1hrs_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="volume_1mth_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_end",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_orderbook_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_orderbook_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_quote_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_quote_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_start",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_symbols_count",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_trade_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="data_trade_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="name",
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="volume_1day_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="volume_1hrs_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="volume_1mth_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="asset_id_base",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name="base", to="crypto.asset"
            ),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="asset_id_quote",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name="quote", to="crypto.asset"
            ),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="asset_id_unit",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name="unit", to="crypto.asset"
            ),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_end",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_orderbook_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_orderbook_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_quote_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_quote_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_start",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_trade_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="data_trade_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="price",
            field=models.DecimalField(decimal_places=5, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="symbol_id",
            field=models.CharField(max_length=150, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="volume_1day",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="volume_1day_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="volume_1hrs",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="volume_1hrs_usd",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="volume_1mth",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="symbol",
            name="volume_1mth_usd",
            field=models.FloatField(null=True),
        ),
    ]
