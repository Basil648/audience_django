from django.urls import path
from  .views import add_to_cart,  remove_from_cart,decrease_cart_quantity, process_payment,  card_payment, cod_view,thank_you,thanku_card
from cart.views import cart_view, checkout_view  


urlpatterns = [
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/decrease/<int:product_id>/", decrease_cart_quantity, name="decrease_cart_quantity"),
    path("view/", cart_view, name="cart_view"),
    path("checkout/", checkout_view, name="checkout"), 
    path('process-payment/', process_payment, name='process_payment'),
    path('payment/card/', card_payment, name='card_payment'),
    path('payment/cod/', cod_view, name='cod_view'),
    path('thank_you/', thank_you, name='thank_you'),
    path('thanku_card/', thanku_card, name='thanku_card'),
]

