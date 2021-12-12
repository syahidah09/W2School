from django.urls import path
from . import views

app_name = 'ewalletAdmin'
urlpatterns = [   
    path('', views.homepage, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    # path('students/', views.manageStudent, name='manage_student'),    
    # path('create_student/', views.createStudent, name='create_student'),
    # path('update_student/<int:pk>/', views.updateStudent, name='update_student'),

    # path('products/', views.productPage, name='products'),
    # path('create_product/', views.createProduct, name='create_product'),
    # path('update_product/<int:pk>/', views.updateProduct, name='update_product'),
    # path('delete_product/<int:pk>/', views.deleteProduct, name='delete_product'),

    #  Student CBV
    path('student/create', views.StudentCreateView2, name='student-create'),
    path('students/', views.StudentListView.as_view(), name='students'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
    path('student/<int:pk>/update', views.StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:pk>/delete', views.StudentDeleteView.as_view(), name='student-delete'),   

    # Parent CBV
    path('parent/create', views.ParentCreateView.as_view(), name='parent-create'),
    path('parents/', views.ParentListView.as_view(), name='parents'),
    path('parent/<int:pk>', views.ParentDetailView2, name='parent-detail'), 
    path('parent/<int:pk>/update', views.ParentUpdateView.as_view(), name='parent-update'),
    path('parent/<int:pk>/delete', views.ParentDeleteView.as_view(), name='parent-delete'),    
    # path('parent/<int:pk>/create_student', views.StudentCreateView2, name='student-create'),

    # Transaction CBV
    path('transaction/create', views.TransactionCreateView2, name='transaction-create'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('transaction/<int:pk>', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/update', views.TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete', views.TransactionDeleteView.as_view(), name='transaction-delete'),
    path('process_transaction2/', views.processTransaction, name="process_transaction2"),

    #  Product CBV
    path('product/create', views.ProductCreateView.as_view(), name='product-create'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
    
    path('store/', views.storePage, name='store'),

    #  Order CBV
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/update', views.OrderUpdateView.as_view(), name='order-update'),
]