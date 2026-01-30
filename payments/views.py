import stripe
import json
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, Http404
from django.utils import timezone
from datetime import timedelta
from django.core import signing
from django.urls import reverse

from pathlib import Path
from products.models import Product
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

# Checkout Session 作成
def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # Order（仮）作成
    order = Order.objects.create(
        user=request.user,
        total_amount=product.price,
        status="pending"
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",  # ← スポット決済
        line_items=[
            {
                "price_data": {
                    "currency": "jpy",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": product.price,
                },
                "quantity": 1,
            }
        ],
        metadata={
            "order_id": order.id,
            "product_id": product.id,
            "user_id": request.user.id,
        },
        success_url=request.build_absolute_uri(
            "/payments/success/"
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri("/payments/cancel/"),
    )

    # Stripe PaymentIntent ID を保存
    order.stripe_payment_intent_id = session.payment_intent
    order.save(update_fields=["stripe_payment_intent_id"])

    return redirect(session.url)

# success / cancel ページ
def payment_success(request):
    # Stripe決済後のDL期限設定
    OrderItem.download_expires_at = timezone.now() + timedelta(days=30)
    OrderItem.download_limit = 5
    OrderItem.save()
    return render(request, "payments/success.html")

def payment_cancel(request):
    return render(request, "payments/cancel.html")

# Webhook
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        order_id = session["metadata"]["order_id"]
        product_id = session["metadata"]["product_id"]

        order = Order.objects.get(id=order_id)
        product = Product.objects.get(id=product_id)

        # 注文確定
        order.status = "paid"
        order.paid_at = timezone.now()
        order.save()

        # OrderItem（DL権限）作成 ← 超重要
        OrderItem.objects.create(
            order=order,
            product=product,
            purchase_price=product.price,
            download_limit=5,
            download_count=0,
            download_expires_at=timezone.now() + timedelta(days=30)
        )

    return HttpResponse(status=200)