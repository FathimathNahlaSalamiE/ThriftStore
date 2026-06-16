from django.urls import path
from ThriftStoreApp import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('seller_products/',views.seller_products,name='seller_products'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:id>',views.edit_product,name= 'edit_product'),
    path('delete_product/<int:id>',views.delete_product,name= 'delete_product'),
    path('home_page/',views.home_page,name="home_page"),
    path('display_products/<str:category_name>/',views.display_products,name= 'display_products'),
    path('view_product/<int:id>/',views.view_product,name = 'view_product'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart_page/',views.cart_page,name='cart_page'),
    path('increase_quantity/<int:id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease_quantity/<int:id>/',views.decrease_quantity,name='decrease_quantity'),    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('address_page/', views.address_page, name='address_page'),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_again/<int:id>/', views.order_again, name='order_again'),
]