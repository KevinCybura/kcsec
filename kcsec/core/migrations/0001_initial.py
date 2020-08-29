# Generated by Django 3.1 on 2020-08-16 18:02

import django.contrib.postgres.fields
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
            CREATE SCHEMA core;  
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
            ],
            options={"verbose_name": "Currency", "verbose_name_plural": "Currencies", "db_table": 'core"."currency',},
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="InternationalExchange",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("exchange", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("region", models.CharField(max_length=20)),
                ("description", models.CharField(max_length=255)),
                ("mic", models.CharField(max_length=10)),
                ("exchange_suffix", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "International Exchange",
                "verbose_name_plural": "International Exchanges",
                "db_table": 'core"."international_exchange',
            },
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="Sector",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={"verbose_name": "Sector", "verbose_name_plural": "Sectors", "db_table": 'core"."sector',},
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="Symbol",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("symbol", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("exchange", models.CharField(max_length=20)),
                ("name", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("is_enabled", models.BooleanField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ad", "ad"),
                            ("re", "re"),
                            ("ce", "ce"),
                            ("si", "si"),
                            ("lp", "lp"),
                            ("cs", "cs"),
                            ("et", "et"),
                            ("wt", "wt"),
                            ("oef", "oef"),
                            ("cef", "cef"),
                            ("ps", "ps"),
                            ("ut", "ut"),
                            ("temp", "temp"),
                        ],
                        max_length=5,
                    ),
                ),
                ("region", models.CharField(max_length=25)),
                ("iex_id", models.CharField(max_length=20)),
                ("figi", models.CharField(max_length=25)),
                ("cik", models.CharField(max_length=20)),
                ("currency", models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="core.currency")),
            ],
            options={"verbose_name": "Symbol", "verbose_name_plural": "Symbols", "db_table": 'core"."symbol',},
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={"verbose_name": "Tag", "verbose_name_plural": "Tags", "db_table": 'core"."tag',},
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="UsExchange",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("long_name", models.CharField(max_length=255)),
                ("mic", models.CharField(max_length=10)),
                ("tape_id", models.CharField(max_length=10)),
                ("oats_id", models.CharField(max_length=10)),
                ("ref_id", models.CharField(max_length=10)),
                ("type", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "US Exchange",
                "verbose_name_plural": "US Exchanges",
                "db_table": 'core"."us_exchange',
            },
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="IexSymbol",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "symbol",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="core.symbol",
                    ),
                ),
                ("date", models.DateField()),
                ("is_enabled", models.BooleanField()),
            ],
            options={
                "verbose_name": "Iex supported symbol",
                "verbose_name_plural": "Iex supported symbols",
                "db_table": 'core"."iex_symbol',
            },
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "symbol",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to="core.symbol"
                    ),
                ),
                ("dates", django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), size=None)),
            ],
            options={"verbose_name": "Option", "verbose_name_plural": "Options", "db_table": 'core"."option',},
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="MutualFundSymbol",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("symbol", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("type", models.CharField(choices=[("oef", "oef"), ("cef", "cef")], max_length=4)),
                ("region", models.CharField(max_length=20)),
                ("iex_id", models.CharField(max_length=25)),
                ("currency", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.currency")),
            ],
            options={
                "verbose_name": "Mutual Fund Symbol",
                "verbose_name_plural": "Mutual Fund Symbols",
                "db_table": 'core"."mutual_fund_symbol',
            },
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="InternationalSymbol",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("symbol", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("is_enabled", models.BooleanField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ad", "ad"),
                            ("re", "re"),
                            ("ce", "ce"),
                            ("si", "si"),
                            ("lp", "lp"),
                            ("cs", "cs"),
                            ("et", "et"),
                            ("wt", "wt"),
                            ("oef", "oef"),
                            ("cef", "cef"),
                            ("ps", "ps"),
                            ("ut", "ut"),
                            ("temp", "temp"),
                        ],
                        max_length=5,
                    ),
                ),
                ("region", models.CharField(max_length=20)),
                ("iex_id", models.CharField(max_length=25)),
                ("currency", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.currency")),
                (
                    "exchange",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.internationalexchange"),
                ),
            ],
            options={
                "verbose_name": "International Symbol",
                "verbose_name_plural": "International Symbols",
                "db_table": 'core"."international_symbol',
            },
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="CurrencyPair",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("symbol", models.CharField(max_length=10, primary_key=True, serialize=False)),
                (
                    "from_currency",
                    models.ForeignKey(
                        max_length=10,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_currency",
                        to="core.currency",
                    ),
                ),
                (
                    "to_currency",
                    models.ForeignKey(
                        max_length=10,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_currency",
                        to="core.currency",
                    ),
                ),
            ],
            options={
                "verbose_name": "Currency Pair",
                "verbose_name_plural": "Currency Pairs",
                "db_table": 'core"."currency_pair',
            },
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
        migrations.CreateModel(
            name="Otc",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "symbol",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to="core.symbol"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("date", models.DateField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ad", "ad"),
                            ("re", "re"),
                            ("ce", "ce"),
                            ("si", "si"),
                            ("lp", "lp"),
                            ("cs", "cs"),
                            ("et", "et"),
                            ("wt", "wt"),
                        ],
                        max_length=3,
                    ),
                ),
                ("region", models.CharField(max_length=25)),
                ("iex_id", models.CharField(max_length=20)),
                ("currency", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.currency")),
            ],
            options={"verbose_name": "OTC symbol", "verbose_name_plural": "OTC symbols", "db_table": 'core"."otc',},
            managers=[("objects", psqlextra.manager.manager.PostgresManager()),],
        ),
    ]
