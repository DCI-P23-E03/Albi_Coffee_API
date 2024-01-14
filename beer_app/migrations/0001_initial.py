# Generated by Django 4.2.9 on 2024-01-06 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brewery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Beer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("style", models.CharField(max_length=50)),
                ("abv", models.FloatField()),
                (
                    "brewery",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beer_app.brewery",
                    ),
                ),
            ],
        ),
    ]
