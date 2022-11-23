from django.urls import path

from .views import buy_product, get_item

app_name = "payment"

urlpatterns = [
    path('buy/<int:id>', buy_product, name='buy_product'),
    path('item/<int:id>', get_item, name='get_item'),

]
