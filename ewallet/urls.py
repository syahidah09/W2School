from django.urls import path
from . import views

app_name = 'ewallet'
urlpatterns = [
     path('', views.frontPage, name='front_page'),
     path('register/', views.registerPage, name='register'),
     path('login/', views.loginPage, name='login'),
     path('logout/', views.logoutUser, name='logout'),

     path('home/', views.homepage, name='home'),
     path('user_profile/', views.user_detail, name='user_detail'),
     path('user_update/', views.user_update, name='user_update'),

     path('wallet/', views.wallet_page, name='wallet'),
     path('topup/', views.topup_page, name='topup'),
     path('reload/<int:pk>', views.reload, name='reload'),

     path('transactions/<int:page>/', views.transaction_history, name='transactions'),
     path('transaction/detail/<int:pk>', views.transaction_detail, name='transaction-detail'),
     path('download_receipt/<int:pk>', views.download_receipt, name='download_receipt'),

     path('process_topup/', views.processTopup, name="process_topup"),
     path('process_transaction/', views.processTransaction,
          name="process_transaction"),
     path('process_reload/', views.processReload, name="process_reload"),

     path('store/', views.store, name='store'),
     path('cart/', views.cart, name="cart"),
     path('checkout/', views.checkout, name="checkout"),
     path('update_item/', views.updateItem, name="update_item"),
     path('process_order/', views.processOrder, name="process_order"),
   
]
