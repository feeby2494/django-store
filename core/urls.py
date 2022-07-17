from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    OrderSummaryView,
    service_page,
    checkout_page,
    user_account,
    add_to_cart,
    remove_from_cart,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('service/', service_page, name='service_page'),
    path('checkout/', checkout_page, name='checkout_page'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('user_account/', user_account, name='user_account'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product_page'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')
]
