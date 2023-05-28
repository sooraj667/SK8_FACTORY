# Generated by Django 4.1.6 on 2023-05-27 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0015_products_offer1_products_offer2_products_offer3"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="products",
            name="offer1",
        ),
        migrations.RemoveField(
            model_name="products",
            name="offer2",
        ),
        migrations.RemoveField(
            model_name="products",
            name="offer3",
        ),
        migrations.CreateModel(
            name="Productoffer",
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
                ("offer_description", models.CharField(max_length=200)),
                ("discount", models.PositiveIntegerField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.products"
                    ),
                ),
            ],
        ),
    ]
