# Generated by Django 4.1.6 on 2023-05-14 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_alter_cart_total"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("country", models.CharField(max_length=200)),
                ("state", models.CharField(max_length=200)),
                ("district", models.CharField(max_length=200)),
                ("locality", models.CharField(max_length=200)),
                ("house", models.CharField(max_length=200)),
                ("pincode", models.PositiveIntegerField()),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.customers",
                    ),
                ),
            ],
        ),
    ]
