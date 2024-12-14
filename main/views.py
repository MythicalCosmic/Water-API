from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *  
from .decorators import * 
import jwt
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from .mixins import *


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")

        if not access_token:
            return Response({"ok": False, "message": "Access Token required or expired"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = AccessToken(access_token)


            return Response({"ok": True, "message": "Logout successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')

        if access_token:
            try:
                decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                expires_in = int(decoded_token['exp'] - datetime.utcnow().timestamp()) 
                user_id = decoded_token.get('user_id')  
                username = response.data.get('username')
                user_role = response.data.get('role')
                user_permissions = response.data.get('permissions')
                superuser_status = response.data.get('superuser_status')
                if superuser_status:
                    user_permissions = None
                    user_role = None
                response_data = {
                    'ok': True,
                    'message': 'Login successful',
                    'data': {
                        'user_data': {
                            'user_id': user_id,
                            'username': username,
                            'user_role': user_role,
                            'user_permissions': user_permissions,
                            'superuser_status': superuser_status
                        },  
                        'access_token': response.data['access'],
                        'token_type': 'Bearer',
                        'expires_in': expires_in 
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({'error': 'Access token has expired'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.DecodeError:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Failed to retrieve access token'}, status=status.HTTP_400_BAD_REQUEST)
    



class SupplierListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Supplier.objects.order_by('id')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_supplier', 'view_supplier']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone_number']


class SupplierRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.order_by('id')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_supplier', 'view_supplier']


class CategoryListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_category', 'view_category']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CategoryRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_category', 'view_category']


class SizeListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Size.objects.order_by('id')
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_size', 'view_size']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SizeRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.order_by('id')
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_size', 'view_size']


class ProductListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_product', 'view_product']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class ProductRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_product', 'view_product']


class ProductVariantListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = ProductVariant.objects.order_by('id')
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_productvariant', 'view_productvariant']
    filter_backends = [filters.SearchFilter]
    search_fields = ['uniq_code']

    def create(self, request, *args, **kwargs):
        data = request.data
        product_id = data.get('product')
        size_id = data.get('size')

        if not product_id or not size_id:
            return Response({
                "ok": False,
                "message": "Both product and size fields are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            existing_variant = ProductVariant.objects.filter(product_id=product_id, size_id=size_id).first()
            if existing_variant:
                return Response({
                    "ok": False,
                    "message": "Product Variant with the specified product and size already exists.",
                    "data": {
                        "id": existing_variant.id,
                        "product": {
                            "id": existing_variant.product.id,
                            "name": existing_variant.product.name
                        },
                        "size": {
                            "id": existing_variant.size.id,
                            "name": existing_variant.size.name
                        },
                        "unique_code": existing_variant.uniq_code
                    }
                }, status=status.HTTP_200_OK)

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()

                product_data = {
                    "id": instance.product.id,
                    "name": instance.product.name
                }
                size_data = {
                    "id": instance.size.id,
                    "name": instance.size.name
                }
                return Response({
                    "ok": True,
                    "message": "Product Variant created successfully.",
                    "data": {
                        "id": instance.id,
                        "product": product_data,
                        "size": size_data,
                        "unique_code": instance.uniq_code,
                    }
                }, status=status.HTTP_201_CREATED)

            else:
                return Response({
                    "ok": False,
                    "message": "Product Variant creation failed.",
                    "data": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "ok": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    


class ProductVariantRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.order_by('id')
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_productvariant', 'view_productvariant']


class StockListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Stock.objects.order_by('id')
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_stock', 'view_stock']
    filter_backends = [filters.SearchFilter]
    search_fields = ['variant', 'price']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            paginated_response.data.update({
                "summary": self.get_summary_data(queryset)
            })

            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Data retrieved successfully",
            "summary": self.get_summary_data(queryset),
            "data": serializer.data
        })

    def get_summary_data(self, queryset):
        total_quantity = sum(item.quantity for item in queryset)
        total_money = sum(float(item.price) for item in queryset)
        return {
            "total_money": f"{total_money:.2f}",
            "total_quantity": total_quantity,
            "total_items": len(queryset)
        }


class StockRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.order_by('id')
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_stock', 'view_stock']


class ImportInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ImportInvoice.objects.order_by('id')
    serializer_class = ImportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importinvoice', 'view_importinvoice']
    filter_backends = [filters.SearchFilter]
    search_fields = ['supplier', 'state']

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        items = data.pop("items", None) 

        if not items:
            return Response({
                "ok": False,
                "message": "Missing required field: items"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            created_items = []

            for item in items:
                variant_id = item.get("variant")
                input_price = item.get("input_price")
                quantity = item.get("quantity")

                if not variant_id or input_price is None or quantity is None:
                    return Response({
                        "ok": False,
                        "message": "Each item must include variant, input_price, and quantity."
                    }, status=status.HTTP_400_BAD_REQUEST)

                try:
                    variant = ProductVariant.objects.get(id=variant_id)

                    imported_item, item_created = ImportedInvoiceItem.objects.get_or_create(
                        import_invoice=instance,
                        variant=variant,
                        defaults={
                            "input_price": input_price,
                            "quantity": quantity,
                        }
                    )
                    if not item_created:
                        imported_item.quantity += quantity
                        imported_item.input_price = input_price
                        imported_item.save()


                    if instance.state != "new":
                        stock, created = Stock.objects.get_or_create(
                            variant=variant,
                            user=user,
                            defaults={"quantity": quantity, "price": input_price}
                        )
                        if not created:
                            stock.quantity += int(quantity)
                            stock.price = input_price
                        stock.save()

                        StockMovement.objects.create(
                            variant=variant,
                            type="arrival",
                            quantity=quantity,
                            description=f"Stock updated from Import Invoice {instance.id}"
                        )

                except ProductVariant.DoesNotExist:
                    return Response({
                        "ok": False,
                        "message": f"Variant with ID {variant_id} does not exist."
                    }, status=status.HTTP_400_BAD_REQUEST)

            supplier_data = {
                "id": instance.supplier.id,
                "name": instance.supplier.name
            }
            user_data = {
                "id": instance.user.id,
                "name": instance.user.username
            }
            return Response({
                "ok": True,
                "message": "Import Invoice and items created successfully.",
                "data": {
                    "id": instance.id,
                    "supplier": supplier_data,
                    "user": user_data,
                    "state": instance.state,
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "ok": False,
            "message": "Import Invoice creation failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class ImportInvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportInvoice.objects.order_by('id')
    serializer_class = ImportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_importinvoice', 'view_importinvoice']

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()

        if instance.state in ['accepted', 'canceled']:
            return Response({
                "ok": False,
                "message": f"Cannot edit an Import Invoice with state '{instance.state}'."
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        items = data.pop("items", None)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()

            if items:
                for item in items:
                    variant_id = item.get("variant")
                    input_price = item.get("input_price")
                    quantity = item.get("quantity")

                    if not variant_id or input_price is None or quantity is None:
                        return Response({
                            "ok": False,
                            "message": "Each item must include variant, input_price, and quantity."
                        }, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        variant = ProductVariant.objects.get(id=variant_id)

                        imported_item, item_created = ImportedInvoiceItem.objects.get_or_create(
                            import_invoice=instance,
                            variant=variant,
                            defaults={
                                "input_price": input_price,
                                "quantity": quantity,
                            }
                        )
                        if not item_created:
                            imported_item.quantity = quantity
                            imported_item.input_price = input_price
                            imported_item.save()

 
                        if updated_instance.state != "new":
                            stock, created = Stock.objects.get_or_create(
                                variant=variant,
                                user=request.user,
                                defaults={"quantity": quantity, "price": input_price}
                            )
                            if not created:
                                stock.quantity += quantity
                                stock.price = input_price
                            stock.save()

                            StockMovement.objects.create(
                                variant=variant,
                                type="update",
                                quantity=quantity,
                                description=f"Stock updated from Import Invoice {instance.id}"
                            )

                    except ProductVariant.DoesNotExist:
                        return Response({
                            "ok": False,
                            "message": f"Variant with ID {variant_id} does not exist."
                     }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "ok": True,
                "message": "Import Invoice updated successfully.",
                "data": self.get_serializer(updated_instance).data
            }, status=status.HTTP_200_OK)

        return Response({
            "ok": False,
            "message": "Import Invoice update failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ImportedInvoiceItemListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = ImportedInvoiceItem.objects.order_by('id')
    serializer_class = ImportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importedinvoiceitem', 'view_importedinvoiceitem']
    filter_backends = [filters.SearchFilter]
    search_fields = ['quantity', 'variant']


class ImportedInvoiceItemRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportedInvoiceItem.objects.order_by('id')
    serializer_class = ImportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_importedinvoiceitem', 'view_importedinvoiceitem']


class StockMovementListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = StockMovement.objects.order_by('id')
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_stockmovement', 'view_stockmovement']
    filter_backends = [filters.SearchFilter]
    search_fields = ['type', 'variant']
    

class StockMovementRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = StockMovement.objects.order_by('id')
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_stockmovement', 'view_stockmovement']


class ClientListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Client.objects.order_by('id')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_client', 'view_client']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone']


class ClientRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.order_by('id')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_client', 'view_client']
        
    def post(self, request, *args, **kwargs):
        if self.request.path.endswith('adjust-balance/'):
            return self.adjust_balance(request, *args, **kwargs)
        
        return super().post(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], url_path='adjust-balance')
    def adjust_balance(self, request, *args, **kwargs):
        client = self.get_object() 
        amount = request.data.get('amount')

        if not amount:
            return Response({
                "ok": False,
                "message": "'amount' field is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount < 0:
                return Response({
                    "ok": False,
                    "message": "Amount must be a positive number."
                }, status=status.HTTP_400_BAD_REQUEST)


            client.balance += amount  
            client.save()

            return Response({
                "ok": True,
                "message": "Balance updated successfully.",
                "data": {
                    "id": client.id,
                    "name": client.name,
                    "balance": client.balance
                }
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({
                "ok": False,
                "message": "Invalid amount format."
            }, status=status.HTTP_400_BAD_REQUEST)


class ExportInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ExportInvoice.objects.order_by('id')
    serializer_class = ExportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_exportinvoice', 'view_exportinvoice']
    filter_backends = [filters.SearchFilter]
    search_fields = ['client', 'state']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        items = data.pop("items", None)  
        payment_type = data.pop("payment_type", None)  

        if not items:
            return Response({
                "ok": False,
                "message": "Missing required field: items"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({
                "ok": False,
                "message": "Export Invoice creation failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        export_invoice = serializer.save(user=request.user)  
        total_price = Decimal(0)
        created_items = []

        for item in items:
            variant_id = item.get("product_variant_id")
            price = item.get("price")
            quantity = item.get("quantity")

            if not variant_id or price is None or quantity is None:
                return Response({
                    "ok": False,
                    "message": "Each item must include product_variant_id, price, and quantity."
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                variant = ProductVariant.objects.get(id=variant_id)
                stock = Stock.objects.filter(variant=variant).first()

                if not stock or stock.quantity < quantity:
                    return Response({
                        "ok": False,
                        "message": f"Insufficient stock for variant {variant_id}. Available: {stock.quantity if stock else 0}, requested: {quantity}."
                    }, status=status.HTTP_400_BAD_REQUEST)

                if export_invoice.state != "new":
                    if stock.quantity > quantity:
                        stock.quantity -= quantity
                        stock.save()
                    elif stock.quantity == quantity:
                        stock.delete()

                    StockMovement.objects.create(
                        variant=variant,
                        type="departure",
                        quantity=quantity,
                        description=f"Stock moved for Export Invoice {export_invoice.id}"
                    )

                exported_item = ExportedInvoiceItem.objects.create(
                    export_invoice=export_invoice,
                    variant=variant,
                    price=Decimal(price),
                    quantity=quantity
                )
                created_items.append(exported_item)
                total_price += Decimal(price) * Decimal(quantity)

            except ProductVariant.DoesNotExist:
                return Response({
                    "ok": False,
                    "message": f"Product variant with ID {variant_id} does not exist."
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            if payment_type == "Debt":
                export_invoice.client.balance -= total_price
                export_invoice.client.save()
            else:
                cashbox = get_object_or_404(Cashbox, id=2)
                cashbox.deposit(
                    total_price,
                    comment=f"Payment for Export Invoice {export_invoice.id}",
                    payment_type=payment_type,
                    user=request.user
                )
        except Exception as e:
            return Response({
                "ok": False,
                "message": f"Error processing payment: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        export_invoice_data = {
            "id": export_invoice.id,
            "client": {
                "id": export_invoice.client.id,
                "name": export_invoice.client.name,
                "balance": export_invoice.client.balance  
            },
            "user": {
                "id": export_invoice.user.id,
                "username": export_invoice.user.username
            },
            "state": export_invoice.state,
        }

        return Response({
            "ok": True,
            "message": "Export Invoice and items created successfully.",
            "data": {
                "invoice": export_invoice_data,
                "items": ExportedInvoiceItemSerializer(created_items, many=True).data
            }
        }, status=status.HTTP_201_CREATED)


class ExportInvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportInvoice.objects.order_by('id')
    serializer_class = ExportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_exportinvoice', 'view_exportinvoice']
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()


        if instance.state not in ["new"]:
            return Response({
                "ok": False,
                "message": f"Cannot edit an Export Invoice with state '{instance.state}'. Only invoices with state 'new' can be updated."
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        items = data.pop("items", None)
        payment_type = data.get("payment_type", None)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        if not serializer.is_valid():
            return Response({
                "ok": False,
                "message": "Export Invoice update failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        export_invoice = serializer.save()
        total_price = Decimal(0)

        if items:
            for item in items:
                variant_id = item.get("product_variant_id")
                price = item.get("price")
                quantity = item.get("quantity")

                if not variant_id or price is None or quantity is None:
                    return Response({
                        "ok": False,
                        "message": "Each item must include product_variant_id, price, and quantity."
                    }, status=status.HTTP_400_BAD_REQUEST)

                try:
                    variant = ProductVariant.objects.get(id=variant_id)
                    stock = Stock.objects.filter(variant=variant).first()

    
                    if not stock or stock.quantity < quantity:
                        return Response({
                            "ok": False,
                            "message": f"Insufficient stock for variant {variant_id}. Available: {stock.quantity if stock else 0}, requested: {quantity}."
                        }, status=status.HTTP_400_BAD_REQUEST)

                    if instance.state != "new":
                        if stock.quantity > quantity:
                            stock.quantity -= quantity
                            stock.save()
                        elif stock.quantity == quantity:
                            stock.delete()

                        StockMovement.objects.create(
                            variant=variant,
                            type="departure",
                            quantity=quantity,
                            description=f"Stock updated for Export Invoice {export_invoice.id}"
                        )

                    exported_item, created = ExportedInvoiceItem.objects.update_or_create(
                        export_invoice=export_invoice,
                        variant=variant,
                        defaults={
                            "price": Decimal(price),
                            "quantity": quantity
                        }
                    )

                    total_price += Decimal(price) * Decimal(quantity)

                except ProductVariant.DoesNotExist:
                    return Response({
                        "ok": False,
                        "message": f"Product variant with ID {variant_id} does not exist."
                    }, status=status.HTTP_400_BAD_REQUEST)

        try:
            if payment_type == "Debt":
                export_invoice.client.balance -= total_price
                export_invoice.client.save()
            else:
                cashbox = get_object_or_404(Cashbox, id=2)
                cashbox.deposit(
                    total_price,
                    comment=f"Payment updated for Export Invoice {export_invoice.id}",
                    payment_type=payment_type,
                    user=request.user
                )
        except Exception as e:
            return Response({
                "ok": False,
                "message": f"Error updating payment: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        export_invoice_data = {
            "id": export_invoice.id,
            "client": {
                "id": export_invoice.client.id,
                "name": export_invoice.client.name,
                "balance": export_invoice.client.balance
            },
            "user": {
                "id": export_invoice.user.id,
                "username": export_invoice.user.username
            },
            "state": export_invoice.state,
        }

        return Response({
            "ok": True,
            "message": "Export Invoice updated successfully.",
            "data": {
                "invoice": export_invoice_data,
                "items": ExportedInvoiceItemSerializer(
                    ExportedInvoiceItem.objects.filter(export_invoice=export_invoice),
                    many=True
                ).data
            }
        }, status=status.HTTP_200_OK)


class ExportedInvoiceItemListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = ExportedInvoiceItem.objects.order_by('id')
    serializer_class = ExportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_exportedinvoiceitem', 'view_exportedinvoiceitem']
    filter_backends = [filters.SearchFilter]
    search_fields = ['export_invoice', 'quantity']


class ExportedInvoiceItemRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportedInvoiceItem.objects.order_by('id')
    serializer_class = ExportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_exportedinvoiceitem', 'view_exportedinvoiceitem']

        
class DepositMoneyView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['deposit_money']

    def post(self, request, pk):
        cashbox = get_object_or_404(Cashbox, pk=pk)
        amount = request.data.get('amount')
        comment = request.data.get('comment', '')
        payment_type = request.data.get('payment_type', '')

        try:
            cashbox.deposit(
                amount=amount,
                comment=comment,
                payment_type=payment_type,
                user=request.user
            )
            return Response({
                "ok": True,
                "message": f"{amount} deposited successfully.",
                "data": {"remains": cashbox.remains}
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({
                "ok": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "ok": False,
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class WithdrawMoneyView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['withdraw_money']

    def post(self, request, pk):
        cashbox = get_object_or_404(Cashbox, pk=pk)
        amount = request.data.get('amount')
        comment = request.data.get('comment', '')
        payment_type = request.data.get('payment_type', '')

        try:
            cashbox.withdraw(
                amount=amount,
                comment=comment,
                payment_type=payment_type,
                user=request.user
            )
            return Response({
                "ok": True,
                "message": f"{amount} withdrawn successfully.",
                "data": {"remains": cashbox.remains}
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({
                "ok": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "ok": False,
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ResetCashboxView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['reset_cashbox'] 

    def post(self, request, pk):
        cashbox = get_object_or_404(Cashbox, pk=pk)

        try:
            cashbox.reset(user=request.user)

            return Response({
                "ok": True,
                "message": "Cashbox reset successfully.",
                "data": {"remains": cashbox.remains}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "ok": False,
                "message": "An error occurred while resetting the cashbox.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CashboxListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Cashbox.objects.order_by('id')
    serializer_class = CashboxSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashbox', 'view_cashbox']
    filter_backends = [filters.SearchFilter]
    search_fields = ['remains']



class CashboxMovementListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = CashboxMovement.objects.order_by('id')
    serializer_class = CashboxMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashboxmovement', 'view_cashboxmovement']
    filter_backends = [filters.SearchFilter]
    search_fields = ['type', 'user']

        
class CashboxMovementRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CashboxMovement.objects.order_by('id')
    serializer_class = CashboxMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_cashboxmovement', 'view_cashboxmovement']



class UserListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.add_user']
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']


class UserDetailView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.change_user', 'auth.delete_user']


class GroupListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_group', 'auth.add_group']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GroupDetailView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_group', 'auth.change_group', 'auth.delete_group']


class PermissionListView(CustomResponseMixin, generics.ListAPIView):
    queryset = Permission.objects.order_by('id')
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_permission']
