from django.db import models

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="カテゴリ名"
    )

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="商品名"
    )
    description = models.TextField(
        verbose_name="商品説明"
    )
    price = models.PositiveIntegerField(
        verbose_name="価格（円）"
    )

    material_file = models.FileField(
        upload_to="products/materials/",
        verbose_name="素材ファイル（pptx）"
    )

    thumbnail_image = models.ImageField(
        upload_to="products/thumbnails/",
        verbose_name="サムネイル画像"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="公開フラグ"
    )

    categories = models.ManyToManyField(
        Category,
        through="ProductCategory",
        related_name="products"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    
class ProductCategory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("product", "category")
