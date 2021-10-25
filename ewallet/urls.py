from django.urls import path
from .views import (
    registerPage,
    loginPage,
    logoutUser,

    homepage,
    wallet_page,      
    transaction_history,     
    store,
    add_dependent,    
)

app_name = 'ewallet'
urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('home/', homepage, name='home'), 
    path('wallet/', wallet_page, name='wallet'),    
    path('transaction_history/', transaction_history, name='transaction_history'),    
    path('store/', store, name='store'),
    
    path('add_dependent/', add_dependent, name='add_dependent'),    

]
