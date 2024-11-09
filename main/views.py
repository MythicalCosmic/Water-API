from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *  # type: ignore
from .decorators import * # type: ignore


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_supplier', 'view_supplier']


class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_supplier', 'view_supplier']


# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_category', 'view_category']


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_category', 'view_category']


# Size Views
class SizeListCreateView(generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_size', 'view_size']


class SizeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_size', 'view_size']


# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_product', 'view_product']


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_product', 'view_product']


# Product Variant Views
class ProductVariantListCreateView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_productvariant', 'view_productvariant']


class ProductVariantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_productvariant', 'view_productvariant']


# Stock Views
class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_stock', 'view_stock']


class StockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_stock', 'view_stock']


# Import Invoice Views
class ImportInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ImportInvoice.objects.all()
    serializer_class = ImportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importinvoice', 'view_importinvoice']


class ImportInvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportInvoice.objects.all()
    serializer_class = ImportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_importinvoice', 'view_importinvoice']


# Imported Invoice Item Views
class ImportedInvoiceItemListCreateView(generics.ListCreateAPIView):
    queryset = ImportedInvoiceItem.objects.all()
    serializer_class = ImportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importedinvoiceitem', 'view_importedinvoiceitem']


class ImportedInvoiceItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportedInvoiceItem.objects.all()
    serializer_class = ImportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_importedinvoiceitem', 'view_importedinvoiceitem']


# Stock Movement Views
class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_stockmovement', 'view_stockmovement']


class StockMovementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_stockmovement', 'view_stockmovement']


# Client Views
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_client', 'view_client']


class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_client', 'view_client']


# Export Invoice Views
class ExportInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ExportInvoice.objects.all()
    serializer_class = ExportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_exportinvoice', 'view_exportinvoice']


class ExportInvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportInvoice.objects.all()
    serializer_class = ExportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_exportinvoice', 'view_exportinvoice']


# Exported Invoice Item Views
class ExportedInvoiceItemListCreateView(generics.ListCreateAPIView):
    queryset = ExportedInvoiceItem.objects.all()
    serializer_class = ExportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_exportedinvoiceitem', 'view_exportedinvoiceitem']


class ExportedInvoiceItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportedInvoiceItem.objects.all()
    serializer_class = ExportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_exportedinvoiceitem', 'view_exportedinvoiceitem']


# Cashbox Views
class CashboxListCreateView(generics.ListCreateAPIView):
    queryset = Cashbox.objects.all()
    serializer_class = CashboxSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashbox', 'view_cashbox']


class CashboxRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cashbox.objects.all()
    serializer_class = CashboxSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_cashbox', 'view_cashbox']


# Cashbox Movement Views
class CashboxMovementListCreateView(generics.ListCreateAPIView):
    queryset = CashboxMovement.objects.all()
    serializer_class = CashboxMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashboxmovement', 'view_cashboxmovement']


class CashboxMovementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CashboxMovement.objects.all()
    serializer_class = CashboxMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_cashboxmovement', 'view_cashboxmovement']


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.add_user']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.change_user', 'auth.delete_user']


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_group', 'auth.add_group']


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_group', 'auth.change_group', 'auth.delete_group']


class PermissionListView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_permission']
