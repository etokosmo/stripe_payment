import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"


def create_checkout_session(request, item_id):
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


def get_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    context = {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    return render(request, "payment/item.html", context=context)
