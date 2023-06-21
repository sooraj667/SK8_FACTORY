# Generated by Django 4.1.6 on 2023-06-20 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0023_rename_slno_orders_ordernumber_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordernumber",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.coupon",
            ),
        ),
        migrations.AddField(
            model_name="ordernumber",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.customers",
            ),
            preserve_default=False,
        ),
    ]