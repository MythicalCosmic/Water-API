from django.urls import path
from .views import *

urlpatterns = [
    path('api-auth/login/', LoginView.as_view(), name='login'),
    path('api-auth/logout/', LogoutView.as_view(), name='logout'),

    path('api/suppliers/', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('api/suppliers/<int:pk>/', SupplierRetrieveUpdateDestroyView.as_view(), name='supplier-detail'),
    
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    
    path('api/sizes/', SizeListCreateView.as_view(), name='size-list-create'),
    path('api/sizes/<int:pk>/', SizeRetrieveUpdateDestroyView.as_view(), name='size-detail'),
    
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    
    path('api/product-variants/', ProductVariantListCreateView.as_view(), name='productvariant-list-create'),
    path('api/product-variants/<int:pk>/', ProductVariantRetrieveUpdateDestroyView.as_view(), name='productvariant-detail'),
    
    path('api/stocks/', StockListCreateView.as_view(), name='stock-list-create'),
    path('api/stocks/<int:pk>/', StockRetrieveUpdateDestroyView.as_view(), name='stock-detail'),
    
    path('api/import-invoices/', ImportInvoiceListCreateView.as_view(), name='importinvoice-list-create'),
    path('api/import-invoices/<int:pk>/', ImportInvoiceRetrieveUpdateDestroyView.as_view(), name='importinvoice-detail'),
    
    path('api/imported-invoice-items/', ImportedInvoiceItemListCreateView.as_view(), name='importedinvoiceitem-list-create'),
    path('api/imported-invoice-items/<int:pk>/', ImportedInvoiceItemRetrieveUpdateDestroyView.as_view(), name='importedinvoiceitem-detail'),
    
    path('api/stock-movements/', StockMovementListCreateView.as_view(), name='stockmovement-list-create'),
    path('api/stock-movements/<int:pk>/', StockMovementRetrieveUpdateDestroyView.as_view(), name='stockmovement-detail'),
    
    path('api/clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('api/clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view(), name='client-detail'),
    
    path('api/export-invoices/', ExportInvoiceListCreateView.as_view(), name='exportinvoice-list-create'),
    path('api/export-invoices/<int:pk>/', ExportInvoiceRetrieveUpdateDestroyView.as_view(), name='exportinvoice-detail'),
    
    path('api/exported-invoice-items/', ExportedInvoiceItemListCreateView.as_view(), name='exportedinvoiceitem-list-create'),
    path('api/exported-invoice-items/<int:pk>/', ExportedInvoiceItemRetrieveUpdateDestroyView.as_view(), name='exportedinvoiceitem-detail'),
    
    path('api/cashboxes/', CashboxListCreateView.as_view(), name='cashbox-list-create'),
    path('api/cashbox/<int:pk>/deposit/', DepositMoneyView.as_view(), name='deposit-money'),
    path('api/cashbox/<int:pk>/withdraw/', WithdrawMoneyView.as_view(), name='withdraw-money'),
    
    path('api/cashbox-movements/', CashboxMovementListCreateView.as_view(), name='cashboxmovement-list-create'),
    path('api/cashbox-movements/<int:pk>/', CashboxMovementRetrieveUpdateDestroyView.as_view(), name='cashboxmovement-detail'),

    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),


    path('api/groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('api/groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),


    path('api/permissions/',PermissionListView.as_view(), name='permission-list'),
]