# Generated by Django 4.1.6 on 2023-06-21 13:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0025_alter_ordernumber_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordernumber",
            name="ordertime",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]