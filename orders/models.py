from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "未決済"),
        ("paid", "支払済"),
        ("canceled", "キャンセル"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    total_amount = models.PositiveIntegerField(
        verbose_name="合計金額"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    purchase_price = models.PositiveIntegerField(
        verbose_name="購入時価格"
    )

    download_limit = models.PositiveIntegerField(
        default=5,
        verbose_name="DL回数上限"
    )

    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name="DL済回数"
    )

    download_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="DL有効期限"
    )

    def can_download(self):
        """DL可否判定"""
        from django.utils import timezone

        if self.download_expires_at and self.download_expires_at < timezone.now():
            return False

        if self.download_count >= self.download_limit:
            return False

        return True

