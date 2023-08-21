# Generated by Django 4.2.3 on 2023-08-20 20:32

from django.db import migrations, models
import products.validators


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_product_pre_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                max_length=200,
                validators=[products.validators.validate_first_character],
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]