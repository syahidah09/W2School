from django.urls import path
from .views import (
    homepage,
    manageStudent,
    createStudent,
    updateStudent,

    productPage,    
    createProduct,
    updateProduct,
    deleteProduct,  

    transactions,

)

app_name = 'ewalletAdmin'
urlpatterns = [   
    path('', homepage, name='home'),

    path('students/', manageStudent, name='manage_student'),    
    path('create_student/', createStudent, name='create_student'),
    path('update_student/<int:pk>/', updateStudent, name='update_student'),

    path('products/', productPage, name='products'),
    path('create_product/', createProduct, name='create_product'),
    path('update_product/<int:pk>/', updateProduct, name='update_product'),
    path('delete_product/<int:pk>/', deleteProduct, name='delete_product'),

    path('transactions/', transactions, name='transactions'), 

    
]