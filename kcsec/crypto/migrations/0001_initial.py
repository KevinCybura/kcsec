# Generated by Django 3.1 on 2020-08-23 16:10

import django.db.models.deletion
import psqlextra.manager.manager
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            """
            CREATE SCHEMA crypto;  
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.CreateModel(
            name="Asset",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("asset", models.CharField(max_length=25, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("type_is_crypto", models.BooleanField()),
                ("data_quote_start", models.DateTimeField()),
                ("data_quote_end", models.DateTimeField()),
                ("data_orderbook_start", models.DateTimeField()),
                ("data_orderbook_end", models.DateTimeField()),
                ("data_trade_start", models.DateTimeField()),
                ("data_trade_end", models.DateTimeField()),
                ("data_quote_count", models.IntegerField()),
                ("data_trade_count", models.IntegerField()),
                ("data_symbols_count", models.IntegerField()),
                ("volume_1hrs_usd", models.FloatField()),
                ("volume_1day_usd", models.FloatField()),
                ("volume_1mth_usd", models.FloatField()),
                ("price_usd", models.DecimalField(decimal_places=2, max_digits=100)),
            ],
            options={
                "verbose_name": "Asset",
                "verbose_name_plural": "Assets",
                "db_table": 'crypto"."asset',
            },
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name="Exchange",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("exchange", models.CharField(max_length=30, primary_key=True, serialize=False)),
                ("website", models.URLField()),
                ("name", models.CharField(max_length=30)),
                ("data_start", models.DateField()),
                ("data_end", models.DateField()),
                ("data_quote_start", models.DateTimeField()),
                ("data_quote_end", models.DateTimeField()),
                ("data_orderbook_start", models.DateTimeField()),
                ("data_orderbook_end", models.DateTimeField()),
                ("data_trade_start", models.DateTimeField()),
                ("data_trade_end", models.DateTimeField()),
                ("data_symbols_count", models.IntegerField()),
                ("volume_1hrs_usd", models.FloatField()),
                ("volume_1day_usd", models.FloatField()),
                ("volume_1mth_usd", models.FloatField()),
            ],
            options={
                "verbose_name": "Crypto currency exchange",
                "verbose_name_plural": "Crypto currency exchanges",
                "db_table": 'crypto"."exchange',
            },
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name="Symbol",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("symbol_id", models.CharField(max_length=150, unique=True)),
                (
                    "symbol_type",
                    models.CharField(
                        choices=[
                            ("SPOT", "Spot"),
                            ("FUTURES", "Futures"),
                            ("OPTION", "Option"),
                            ("PERPETUAL", "Perpetual"),
                            ("INDEX", "Index"),
                            ("CREDIT", "Credit"),
                        ],
                        max_length=10,
                    ),
                ),
                ("data_start", models.DateField()),
                ("data_end", models.DateField()),
                ("data_quote_start", models.DateTimeField()),
                ("data_quote_end", models.DateTimeField()),
                ("data_orderbook_start", models.DateTimeField()),
                ("data_orderbook_end", models.DateTimeField()),
                ("data_trade_start", models.DateTimeField()),
                ("data_trade_end", models.DateTimeField()),
                ("volume_1hrs", models.FloatField()),
                ("volume_1day", models.FloatField()),
                ("volume_1mth", models.FloatField()),
                ("volume_1hrs_usd", models.FloatField()),
                ("volume_1day_usd", models.FloatField()),
                ("volume_1mth_usd", models.FloatField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=100)),
                (
                    "asset_id_base",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, related_name="base", to="crypto.asset"
                    ),
                ),
                (
                    "asset_id_quote",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, related_name="quote", to="crypto.asset"
                    ),
                ),
                (
                    "asset_id_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, related_name="unit", to="crypto.asset"
                    ),
                ),
                ("exchange", models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="crypto.exchange")),
            ],
            options={
                "verbose_name": "Symbol",
                "verbose_name_plural": "Symbols",
                "db_table": 'crypto"."symbol',
            },
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
    ]
