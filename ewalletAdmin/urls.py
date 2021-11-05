from django.urls import path
from . import views

app_name = 'ewalletAdmin'
urlpatterns = [   
    path('', views.homepage, name='home'),

    path('students/create', views.StudentCreateView.as_view(), name='student-create'),
    path('students/', views.StudentListView.as_view(), name='students'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
    path('student/<int:pk>/update', views.StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:pk>/delete', views.StudentDeleteView.as_view(), name='student-delete'),

    # path('students/', views.manageStudent, name='manage_student'),    
    # path('create_student/', views.createStudent, name='create_student'),
    # path('update_student/<int:pk>/', views.updateStudent, name='update_student'),

    path('products/', views.productPage, name='products'),
    path('create_product/', views.createProduct, name='create_product'),
    path('update_product/<int:pk>/', views.updateProduct, name='update_product'),
    path('delete_product/<int:pk>/', views.deleteProduct, name='delete_product'),

    path('transactions/', views.transactions, name='transactions'), 

    
]