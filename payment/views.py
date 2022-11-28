import json

import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from .models import Item, Order, OrderElements, Promocode

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    """Template for success pay"""
    template_name = "payment/success.html"


class CancelView(TemplateView):
    """Template for cancel pay"""
    template_name = "payment/cancel.html"


def create_checkout_session(request, item_id=1):
    """Create sessionId for Stripe Pay.
    GET: 1 item, need item_id arg in URL.
    POST: several items, need items in body.
    """
    if request.method == 'GET':
        item = get_object_or_404(Item, id=item_id)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/api/success'),
            cancel_url=request.build_absolute_uri('/api/cancel'),
        )
        return JsonResponse({'sessionId': session.stripe_id})
    if request.method == 'POST':
        # TODO create DRF serializer instead this
        products = json.loads(request.body)
        line_items = []

        order = Order.objects.create()
        for product in products:
            item_id = product.get('id')
            item_price = product.get('price')
            item_quantity = product.get('quantity')
            customer_firstname = product.get('customer_firstname')
            if customer_firstname:
                order.customer_firstname = customer_firstname
                order.save()
            customer_lastname = product.get('customer_lastname')
            if customer_lastname:
                order.customer_lastname = customer_lastname
                order.save()
            customer_address = product.get('customer_address')
            if customer_address:
                order.customer_address = customer_address
                order.save()
            customer_promocode = product.get('customer_promocode')
            try:
                promocode = Promocode.objects.get(promocode=customer_promocode)
                coupon = stripe.Coupon.create(
                    percent_off=promocode.discount,
                    duration="once"
                )
                coupon_id = coupon.get('id')
            except Promocode.DoesNotExist:
                coupon_id = None
            if item_id is None or item_price is None or item_quantity is None:
                order.delete()
                HttpResponseServerError("Incorrect format")
            item = get_object_or_404(Item, id=item_id)
            OrderElements.objects.create(
                order=order,
                item=item,
                quantity=item_price,
                price_in_order=item_quantity
            )
            line_items.append(
                {
                    'price_data': {
                        'currency': 'rub',
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': item.price * 100,
                    },
                    'quantity': item_quantity,
                }
            )

    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        discounts=[{
            'coupon': coupon_id,
        }],
        success_url=request.build_absolute_uri('/api/success'),
        cancel_url=request.build_absolute_uri('/api/cancel'),
    )
    return JsonResponse({'sessionId': session.stripe_id})


def get_item(request, item_id):
    """Render page with item=item_id"""
    item = get_object_or_404(Item, id=item_id)

    context = {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    return render(request, "payment/item.html", context=context)


def get_items(request):
    """Render page with all items from db"""
    items = Item.objects.all()

    context = {'items': items, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    return render(request, "payment/items.html", context=context)
