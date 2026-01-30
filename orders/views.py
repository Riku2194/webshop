from django.shortcuts import render
from django.core import signing
from django.http import FileResponse, Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from pathlib import Path
from django.conf import settings
from django.urls import reverse
from orders.models import OrderItem

# 署名付きダウンロードURLの発行
def generate_download_url(order_item):
    signer = signing.TimestampSigner()
    value = str(order_item.id)
    signed_value = signer.sign(value)

    return reverse(
        "orders:download",
        kwargs={"signed_value": signed_value}
    )

# ダウンロードView
@login_required
def download_material(request, signed_value):
    signer = signing.TimestampSigner()

    try:
        order_item_id = signer.unsign(
            signed_value,
            max_age=60 * 60 * 24 * 30  # 30日
        )
    except signing.BadSignature:
        raise Http404("Invalid or expired link")

    order_item = (
        OrderItem.objects
        .select_related("order", "product")
        .get(id=order_item_id)
    )

    # 所有者チェック
    if order_item.order.user != request.user:
        raise Http404()

    # 期限チェック
    if timezone.now() > order_item.download_expires_at:
        raise Http404("Expired")

    # DL回数チェック
    if order_item.download_count >= order_item.download_limit:
        raise Http404("Download limit exceeded")

    # DL回数更新
    order_item.download_count += 1
    order_item.save(update_fields=["download_count"])

    file_path = Path(settings.PROTECTED_MEDIA_ROOT) / order_item.product.material_file.name

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=file_path.name
    )
