from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add/<int:product_id>/', views.add_cart, name="add_cart"),
    path('details/', views.cart_detail, name='cart_detail'),
    # path('/products/<slug>/',name='cart_detail'),
    # path('<slug:c_slug>/<slug:product_slug>/', views.proDetail, name='get_absolute_url')
    path('remove/<int:product_id>/',views.cart_remove,name="cart_remove"),
    path('full_remove/<int:product_id>/', views.full_remove, name="full_remove"),

]
