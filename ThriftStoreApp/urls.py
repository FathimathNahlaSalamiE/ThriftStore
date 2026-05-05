from django.urls import path
from ThriftStoreApp import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('display_product/',views.display_product,name= 'display_product'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:id>',views.edit_product,name= 'edit_product'),
    path('delete_product/<int:id>',views.delete_product,name= 'delete_product')
]