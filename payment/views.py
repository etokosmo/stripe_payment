import json

import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from .models import Item, Order, OrderElements

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"


def create_checkout_session(request, item_id=1):
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
        products = json.loads(request.body)
        line_items = []

        order = Order.objects.create()
        for product in products:
            try:
                item_id = product.get('id')
                item_price = product['price']
                item_quantity = product['quantity']
            except KeyError:
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
                            'name': item_id,
                        },
                        'unit_amount': item_price * 100,
                    },
                    'quantity': item_quantity,
                }
            )

    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/api/success'),
        cancel_url=request.build_absolute_uri('/api/cancel'),
    )
    return JsonResponse({'sessionId': session.stripe_id})


def get_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    context = {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    return render(request, "payment/item.html", context=context)


def get_items(request):
    items = Item.objects.all()

    context = {'items': items, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    return render(request, "payment/items.html", context=context)
