# Generated by Django 4.2.3 on 2023-08-20 19:46

from django.db import migrations
import csv
from django.utils.html import strip_tags
from django.core.files import File
from io import BytesIO
import requests
from django.utils.text import slugify
from unidecode import unidecode


def create_images_for_product(model, product, image_urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    product_images = []
    session = requests.session()
    for url in image_urls:
        response = session.get(url, headers=headers)
        img_name = f"{product.name}.jpg"
        img_data = BytesIO(response.content)
        image_file = File(img_data, name=img_name)
        product_image = model(product=product, image=image_file)
        product_images.append(product_image)

    model.objects.bulk_create(product_images)


def get_description_attr(number, row):
    description_attr_name = row.get(f"Име на атрибута {number}")

    if description_attr_name:
        description_attr_value = row.get(f"Стойност(и) на атрибута {number}")
        description_attr = description_attr_name + " " + description_attr_value

        return description_attr
    return None


def get_full_description(numbers, row, description):
    if description:
        description += "<br>"

    description_attrs = [get_description_attr(number, row) for number in numbers]
    description_attrs = [a for a in description_attrs if a]
    if description_attrs:
        description += "<br>".join(description_attrs)

    return description


def load_data(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    ProductImage = apps.get_model("products", "ProductImage")
    Category = apps.get_model("products", "Category")

    with open("wc-product-export-20-8-2023-1692558412792.csv") as jepeto_products:
        csv_reader = csv.DictReader(jepeto_products)

        for row in csv_reader:
            name = row.get("Име")

            description = strip_tags(row.get("Кратко описание")).replace("\\n", "")
            description = get_full_description(["1", "2", "3"], row, description)

            availability = row.get("В наличност?")

            quantity = 0
            preorder = availability == "backorder"

            if availability == "1":
                try:
                    quantity = int(row.get("Наличност"))
                except ValueError:
                    quantity = 1

            try:
                price = float(row.get("Редовна цена:"))
            except ValueError:
                continue

            given_categories = row.get("Категории").split(", ")

            categories = []
            for category_name in given_categories:
                categories.append(Category.objects.get_or_create(name=category_name)[0])

            product = Product.objects.create(
                name=name,
                description=description,
                quantity=quantity,
                price=price,
                pre_order=preorder,
            )

            product.categories.set(categories)

            ascii_name = unidecode(product.name)
            product.slug = f"{slugify(ascii_name)}-{product.id}"

            product.save()

            images = row.get("Изображения").split(", ")
            create_images_for_product(ProductImage, product, images)


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_alter_product_name_alter_product_slug"),
    ]

    operations = [migrations.RunPython(load_data)]
