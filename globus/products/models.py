import os.path
import requests
from django.conf import settings
from django.db import models
from smart_selects.db_fields import GroupedForeignKey
from django.utils.translation import gettext_lazy as _
from PIL import Image

class Category(models.Model):
    name = models.CharField("Название", max_length=200)
    img = models.ImageField("Изображение", upload_to="product-category/%Y_%m")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="sub_categories")
    name = models.CharField("Название", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Product(models.Model):
    PRICE_FOR_CHOICES = [
        ("кг", "кг"),
        ("шт", "шт")
    ]

    status = models.BooleanField(_('Показать в мобильном приложении'), default=False)
    cat = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    sub_cat = GroupedForeignKey(SubCategory, "cat", verbose_name="Подкатегория", null=True, blank=True)
    title = models.CharField("Название товара", max_length=300)
    code = models.CharField("ID товара", max_length=100, null=True, blank=True, unique=True)
    old_price = models.CharField("Старая цена", max_length=100, blank=True, null=True)
    price = models.FloatField("Цена")
    wholesale_price = models.FloatField("Оптовая цена", null=True, blank=True)
    price_for = models.CharField("Цена за", choices=PRICE_FOR_CHOICES, default="шт")
    img = models.ImageField("Изображение", upload_to="product-detail/%Y_%m", null=True, blank=True)
    sales = models.IntegerField(_("Количество продаж"), default=0)
    quantity = models.CharField("Количество", max_length=100, null=True, blank=True, choices=[("kg", "кг"), ("unit", "шт")])
    barrcode = models.CharField(_("Штрих-код"), null=True, blank=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def save(self, *args, **kwargs):
        if self.sub_cat:
            self.cat = self.sub_cat.cat
        self.price = float(self.price)

        img_path = os.path.join(settings.MEDIA_ROOT, self.img.name)
        watermark_path = os.path.join(os.path.dirname(__file__), 'mark.png')

        if self.img and os.path.isfile(watermark_path):
            watermark = Image.open(watermark_path).convert("RGBA")
            img = Image.open(img_path).convert("RGBA").copy()

            img_width, img_height = img.size
            watermark_width, watermark_height = watermark.size

            scale = 0.5
            new_watermark_width = int(img_width * scale)
            new_watermark_height = int((new_watermark_width / watermark_width) * watermark_height)
            resized_watermark = watermark.resize((new_watermark_width, new_watermark_height))

            x = (img_width - new_watermark_width) // 2
            y = (img_height - new_watermark_height) // 2

            img.paste(resized_watermark, (x, y), resized_watermark)

            img.save(img_path, format="png", quality=100)

        super().save(*args, **kwargs)

class UnloadedCategories(models.Model):
    name = models.CharField(_("Название"), max_length=255)
    guid = models.CharField(_("GUID"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("1C категория")
        verbose_name_plural = _("1C категории")


class UnloadedProducts(models.Model):
    cat = models.ForeignKey(UnloadedCategories, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Дата"), auto_now_add=True, null=True, blank=True)
    status = models.BooleanField(_("Статус"), default=True)

    def __str__(self):
        return self.cat.name

    class Meta:
        verbose_name = _("1C Выгрузка")
        verbose_name_plural = _("1C Выгрузка")

    def save(self, *args, **kwargs):
        url = f"http://31.186.48.247/Roznica/hs/MobileApp/product-list?Guid={self.cat.guid}"
        headers = {"Authorization": settings.ONE_C}

        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            self.status = False
            super(UnloadedProducts, self).save(*args, **kwargs)
            return

        product_list = response.json()

        for product in product_list:
            price = product.get("price", "")
            cleaned_price = price.replace(' ', '').replace(',', '.')
            cleaned_price = ''.join(filter(lambda x: x.isdigit() or x == '.', cleaned_price))

            try:
                product_exist = Product.objects.get(code=product["product_id"])
                product_exist.price = cleaned_price
                product_exist.old_price = product.get("discounted_price", "")
                product_exist.save()
            except Product.DoesNotExist:
                Product.objects.create(
                    title=product["name"],
                    code=product["product_id"],
                    barrcode=product.get("Barcode", ""),
                    price=cleaned_price,
                    old_price=product.get("discounted_price", ""),
                    quantity=product.get("quantity", ""),
                    price_for=product.get("unit", "шт")
                )

        super(UnloadedProducts, self).save(*args, **kwargs)
