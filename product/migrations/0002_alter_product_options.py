# Generated by Django 4.1 on 2022-09-04 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "permissions": (
                    ("can_change_product_name", "Can change product name"),
                    ("can_change_product_category", "Can change product category"),
                )
            },
        ),
    ]