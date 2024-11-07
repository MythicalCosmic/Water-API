from django.urls import path
from .views import *
from .views import LoginView, LogoutView

urlpatterns = [
    path('api-auth/login/', LoginView.as_view(), name='login'),
    path('api-auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('api/brands/<int:pk>/', BrandDetailView.as_view(), name='brand-detail'),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/branches/', BranchListCreateView.as_view(), name='branch-list-create'),
    path('api/branches/<int:pk>/', BranchDetailView.as_view(), name='branch-detail'),
    path('api/supplier/', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('api/supplier/<int:pk>/',SupplierDetailView.as_view(), name='supplier-detail'),
    path('api/clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('api/clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('api/product-variants/', ProductVariantListCreateView.as_view(), name='product-variant-list-create'),
    path('api/product-variants/<int:pk>/', ProductVariantDetailView.as_view(), name='product-variant-detail'),
    path('api/sizes/', SizeListCreateView.as_view(), name='size-list-create'),
    path('api/sizes/<int:pk>/', SizeDetailView.as_view(), name='size-detail'),

]
