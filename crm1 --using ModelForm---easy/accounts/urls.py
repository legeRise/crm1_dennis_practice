from django.urls import path
from . import views
from django.conf import settings
# from django.conf.settings import static

urlpatterns = [
    path('',views.home,name='dashboard'),
    path('user/',views.user,name='UserDashboard'),
    path('accountSettings/',views.accountSettings,name='accountSettings'),
    path('products/',views.products,name='products'),
    path('customer/<str:pk>/',views.customer,name='customer'),
    
    path('create_order/<str:pk>',views.createOrder,name='create_order'),
    path('update_order/<str:pk>',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>',views.deleteOrder,name='delete_order')
]


