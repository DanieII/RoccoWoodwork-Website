from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from .validators import validate_first_character
from django.contrib.auth import get_user_model
from unidecode import unidecode


UserModel = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=200, validators=[validate_first_character])
    price = models.FloatField(validators=[MinValueValidator(0)])
    categories = models.ManyToManyField(to="Category")
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    pre_order = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def available(self):
        return self.quantity >= 1

    @property
    def thumbnail_image_url(self):
        try:
            image = self.productimage_set.all()[0]
            return image.image.url
        except IndexError:
            return "/static/images/no-image.jpg"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            ascii_name = unidecode(self.name)
            self.slug = f"{slugify(ascii_name)}-{self.id}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["pk"]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def get_choices(cls):
        return [(category.name, category.name) for category in cls.objects.all()]

    class Meta:
        verbose_name_plural = "Categories"


class ProductReview(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField()
    review = models.TextField()
