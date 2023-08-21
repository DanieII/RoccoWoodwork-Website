# Generated by Django 4.2.3 on 2023-08-21 18:49

from django.db import migrations


def remove_backslash_before_comma(apps, schema):
    Product = apps.get_model("products", "Product")

    for product in Product.objects.all():
        product.description = product.description.replace("\\,", ",")
        product.save()


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_auto_20230821_1144"),
    ]

    operations = [migrations.RunPython(remove_backslash_before_comma)]
