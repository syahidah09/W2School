from django.urls import path
from account.views import (
    loginPage,
    registerPage,
    logoutUser    
)



app_name = 'account'
urlpatterns = [
    # path('home/', registerPage),

    # path('signup/', registerPage),
    # path('login/', loginPage, name='Login'),    
    # path('logout/', logoutUser, name='Logout'),

    
]
