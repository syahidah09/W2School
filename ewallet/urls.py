from django.urls import path
from . import views

app_name = 'ewallet'
urlpatterns = [
    path('', views.frontPage, name=''),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('home/', views.homepage, name='home'), 
    path('wallet/', views.wallet_page, name='wallet'), 
    path('topup/', views.topup_page, name='topup'),
    path('reload/', views.reload, name='reload'),      
    path('transactions/<int:page>/', views.transaction_history, name='transactions'),

    path('process_topup/', views.processTopup, name="process_topup"),
    path('process_transaction/', views.processTransaction, name="process_transaction"),
    path('process_reload/', views.processReload, name="process_reload"),     

    path('store/', views.store, name='store'),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),  
    
    path('add_dependent/', views.add_dependent, name='add_dependent'),    

]
