import stripe
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


def create_checkout_session(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(Item, id=item_id)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/api/success'),
            cancel_url=request.build_absolute_uri('/api/cancel'),
        )
        return HttpResponse(session.stripe_id)


def get_item(request):
    pass
