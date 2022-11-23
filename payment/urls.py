from django.urls import path

from .views import create_checkout_session, get_item, CancelView, SuccessView

app_name = "payment"

urlpatterns = [
    path('buy/<int:item_id>/', create_checkout_session,
         name='create_checkout_session'),
    path('item/<int:item_id>/', get_item, name='get_item'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),

]
