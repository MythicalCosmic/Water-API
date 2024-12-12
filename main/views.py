from rest_framework import generics, status
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
    



class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.order_by('id')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_supplier', 'view_supplier']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()  
            return Response({
                "ok": True,
                "message": "Supplier created successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                    "contact": instance.phone_number
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "ok": False,
            "message": "Supplier creation failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.order_by('id')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_supplier', 'view_supplier']

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Supplier with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Supplier retrieved successfully",
            "data": serializer.data  
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            
            return Response({
                "ok": True,
                "message": "Supplier updated successfully",
                "data": {
                    "id": updated_instance.id,
                    "name": updated_instance.name,
                    "contact": updated_instance.phone_number
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Supplier update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)



# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_category', 'view_category']
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()  
            return Response({
                "ok": True,
                "message": "Category created successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                    "contact": instance.description
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "ok": False,
            "message": "Cateogry creation failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_category', 'view_category']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Category with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Category retrieved successfully",
            "data": serializer.data  
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            
            return Response({
                "ok": True,
                "message": "Category updated successfully",
                "data": {
                    "id": updated_instance.id,
                    "name": updated_instance.name,
                    "description": updated_instance.description
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Category update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class SizeListCreateView(generics.ListCreateAPIView):
    queryset = Size.objects.order_by('id')
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_size', 'view_size']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()  
            return Response({
                "ok": True,
                "message": "Size created successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                }
            }, status=status.HTTP_201_CREATED)   
        
        return Response({
            "ok": False,
            "message": "Size creation failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SizeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.order_by('id')
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_size', 'view_size']

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Size with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Size retrieved successfully",
            "data": serializer.data  
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            
            return Response({
                "ok": True,
                "message": "Size updated successfully",
                "data": {
                    "id": updated_instance.id,
                    "name": updated_instance.name,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Size update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_product', 'view_product']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()  
            return Response({
                "ok": True,
                "message": "Product created successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                    "description": instance.description,
                    "category": instance.category.name,
                }
            }, status=status.HTTP_201_CREATED)   
        else:
            return Response({
                "ok": False,
                "message": "Product creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_product', 'view_product']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Product with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Product retrieved successfully",
            "data": serializer.data  
        })
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            
            return Response({
                "ok": True,
                "message": "Product updated successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                    "description": instance.description,
                    "category": instance.category.name,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Product update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductVariantListCreateView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.order_by('id')
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_productvariant', 'view_productvariant']

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

    


class ProductVariantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.order_by('id')
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_productvariant', 'view_productvariant']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Product Variant with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Product Variant retrieved successfully",
            "data": serializer.data  
        })
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
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
                "message": "Product Variant updated successfully",
                 "data": {
                    "id": instance.id,
                    "product": product_data,
                    "size": size_data,
                    "unique_code": instance.uniq_code,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Product Variant update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.order_by('id')
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_stock', 'view_stock']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)  
            instance = serializer.instance
            variant_data = {
                "id": instance.variant.id,
            }
            return Response({
                "ok": True,
                "message": "Stock created successfully",
                "data": {
                    "id": instance.id,
                    "variant": variant_data,
                    "quantity": instance.quantity,
                    "price": instance.price,
                    "user": {
                        "id": instance.user.id,
                        "username": instance.user.username
                    }
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "ok": False,
                "message": "Stock creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_money = sum(stock.quantity * stock.price for stock in queryset)
        total_quantity = sum(stock.quantity for stock in queryset)
        total_items = queryset.count() 
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Stock retrieved successfully",
            "summary": {
                "total_money": str(total_money),  
                "total_quantity": total_quantity,
                "total_items": total_items  
            },
            "data": serializer.data
        })




class StockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.order_by('id')
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_stock', 'view_stock']

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Stock retrieved successfully",
            "data": serializer.data  
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save(user=request.user)  
            variant_data = {
                "id": updated_instance.variant.id,
            }
            return Response({
                "ok": True,
                "message": "Stock updated successfully",
                "data": {
                    "id": updated_instance.id,
                    "variant": variant_data,
                    "quantity": updated_instance.quantity,
                    "price": updated_instance.price,
                    "user": {
                        "id": updated_instance.user.id,
                        "username": updated_instance.user.username
                    }
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Stock update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ImportInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ImportInvoice.objects.order_by('id')
    serializer_class = ImportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importinvoice', 'view_importinvoice']

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
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Import Invoice with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Import Invoice retrieved successfully",
            "data": serializer.data  
        })

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


class ImportedInvoiceItemListCreateView(generics.ListCreateAPIView):
    queryset = ImportedInvoiceItem.objects.order_by('id')
    serializer_class = ImportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importedinvoiceitem', 'view_importedinvoiceitem']




class ImportedInvoiceItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportedInvoiceItem.objects.order_by('id')
    serializer_class = ImportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_importedinvoiceitem', 'view_importedinvoiceitem']

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Imported Invoice Item with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Imported Invoice Item retrieved successfully",
            "data": serializer.data  
        })

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Imported Invoice Item with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    

        import_invoice = instance.import_invoice
        if import_invoice.state not in ['new']:
            return Response({
                "ok": False,
                "message": f"Cannot delete Imported Invoice Item. The associated Import Invoice is in '{import_invoice.state}' state.",
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({
            "ok": True,
            "message": "Imported Invoice Item deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)


class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.order_by('id')
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_stockmovement', 'view_stockmovement']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()

            variant_data = {
                "id": instance.variant.id,
            }
            return Response({
                "ok": True,
                "message": "Stock Movement created successfully",
                "data": {
                    "id": instance.id,
                    "variant": variant_data,
                    "type": instance.type,
                    "description": instance.description,
                    "quantity": instance.quantity,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Stock Movement creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    

class StockMovementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockMovement.objects.order_by('id')
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_stockmovement', 'view_stockmovement']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Stock Movement with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Stock Movement retrieved successfully",
            "data": serializer.data  
        })
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            variant_data = {
                "id": instance.variant.id,
            }
            
            return Response({
                "ok": True,
                "message": "Stock Movement updated successfully",
                  "data": {
                    "id": instance.id,
                    "type": instance.type,
                    "variant": variant_data,
                    "description": instance.description,
                    "quantity": instance.quantity,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Stock Movement update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.order_by('id')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_client', 'view_client']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()

            return Response({
                "ok": True,
                "message": "Client created successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                    "phone": instance.phone,
                    "description": instance.description,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Client creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.order_by('id')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_client', 'view_client']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Client with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Client retrieved successfully",
            "data": serializer.data  
        })
        
    def post(self, request, *args, **kwargs):
        if self.request.path.endswith('adjust-balance/'):
            return self.adjust_balance(request, *args, **kwargs)
        
        return super().post(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            return Response({
                "ok": True,
                "message": "Client updated successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                    "phone": instance.phone,
                    "description": instance.description,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Client update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

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

        # Process Items
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

        # Process Payment
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

        # Response
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
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Export Invoice with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Export Invoice retrieved successfully",
            "data": serializer.data  
        })
        
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()

        # Prevent updates to invoices with states other than "new"
        if instance.state not in ["new"]:
            return Response({
                "ok": False,
                "message": f"Cannot edit an Export Invoice with state '{instance.state}'. Only invoices with state 'new' can be updated."
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        items = data.pop("items", None)
        payment_type = data.get("payment_type", None)

        # Validate and update the invoice
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if not serializer.is_valid():
            return Response({
                "ok": False,
                "message": "Export Invoice update failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        export_invoice = serializer.save()
        total_price = Decimal(0)

        # Process Items
        if items:
            for item in items:
                variant_id = item.get("product_variant_id")
                price = item.get("price")
                quantity = item.get("quantity")

                # Validate item fields
                if not variant_id or price is None or quantity is None:
                    return Response({
                        "ok": False,
                        "message": "Each item must include product_variant_id, price, and quantity."
                    }, status=status.HTTP_400_BAD_REQUEST)

                try:
                    variant = ProductVariant.objects.get(id=variant_id)
                    stock = Stock.objects.filter(variant=variant).first()

                    # Check stock availability
                    if not stock or stock.quantity < quantity:
                        return Response({
                            "ok": False,
                            "message": f"Insufficient stock for variant {variant_id}. Available: {stock.quantity if stock else 0}, requested: {quantity}."
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Update stock only if state is not "new"
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

                    # Update or create invoice items
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

        # Process Payment
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

        # Response
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


class ExportedInvoiceItemListCreateView(generics.ListCreateAPIView):
    queryset = ExportedInvoiceItem.objects.order_by('id')
    serializer_class = ExportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_exportedinvoiceitem', 'view_exportedinvoiceitem']


class ExportedInvoiceItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportedInvoiceItem.objects.order_by('id')
    serializer_class = ExportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_exportedinvoiceitem', 'view_exportedinvoiceitem']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Exported Invoice Item with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Exported Invoice Items retrieved successfully",
            "data": serializer.data  
        })
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            export_invoice_data = {
                "id": instance.export_invoice.id,
                "name": instance.client.name
            }
            variant_data = {
                "id": instance.variant.id,
                "name": instance.variant.name
            }   
            return Response({
                "ok": True,
                "message": "Export Invoice Item updated successfully",
                "data": {
                    "id": instance.id,
                    "export_invoice": export_invoice_data,
                    "variant": variant_data,
                    "state": instance.state,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Export Invoice Item update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

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



class CashboxListCreateView(generics.ListCreateAPIView):
    queryset = Cashbox.objects.order_by('id')
    serializer_class = CashboxSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashbox', 'view_cashbox']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save() 
            return Response({
                "ok": True,
                "message": "Cashbox created successfully.",
                "data": {
                    "id": instance.id,
                    "remains": str(instance.remains), 
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "ok": False,
            "message": "Cashbox creation failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class CashboxMovementListCreateView(generics.ListCreateAPIView):
    queryset = CashboxMovement.objects.order_by('id')
    serializer_class = CashboxMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashboxmovement', 'view_cashboxmovement']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            if instance.user:
                user_data = {
                    "id": instance.user.id,
                    "username": instance.user.username,
                }
            else:
                user_data = None 

            return Response({
                "ok": True,
                "message": "CashboxMovement Item created successfully",
                "data": {
                    "id": instance.id,
                    "type": instance.type,
                    "sum": instance.sum,
                    "remains": instance.remains,
                    "comment": instance.comment,
                    "payment_type": instance.payment_type,
                    "user": user_data,
                    "created_at": instance.created_at,
                    "updated_at": instance.updated_at,
                    "deleted_at": instance.deleted_at,
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "ok": False,
                "message": "CashboxMovement creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class CashboxMovementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CashboxMovement.objects.order_by('id')
    serializer_class = CashboxMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_cashboxmovement', 'view_cashboxmovement']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "CashboxMovement with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "CashboxMovement retrieved successfully",
            "data": serializer.data  
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save()  
            user_data = {
                "id": instance.user.id,
                "username": instance.user.username,
            }
            return Response({
                "ok": True,
                "message": "CashboxMovement updated successfully",
                "data": {
                    "id": instance.id,
                    "type": instance.type,
                    "sum": instance.sum,
                    "remains": instance.remains,
                    "comment": instance.comment,
                    "payment_type": instance.payment_type,
                    "user": user_data,
                    "created_at": instance.created_at,
                    "updated_at": instance.updated_at,
                    "deleted_at": instance.deleted_at,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "CashboxMovement update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.add_user']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_password(request.data['password'])
            instance.save()
        
            user_data = {
                "id": instance.id,
                "username": instance.username,
                "email": instance.email,
                "is_active": instance.is_active,
                "is_staff": instance.is_staff,
                "is_superuser": instance.is_superuser,
                "groups": [group.id for group in instance.groups.all()],
                "user_permissions": [permission.id for permission in instance.user_permissions.all()]
            }
        
            return Response({
                "ok": True,
                "message": "User created successfully",
                "data": user_data
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "User creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.change_user', 'auth.delete_user']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(User, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "User with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "User retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
    
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response({
                "ok": True,
                "message": "User updated successfully",
                "data": {
                    "id": updated_instance.id,
                    "username": updated_instance.username,
                    "is_active": updated_instance.is_active,
                    "is_staff": updated_instance.is_staff,
                    "is_superuser": updated_instance.is_superuser,
                    "groups": [group.id for group in updated_instance.groups.all()],
                    "user_permissions": [permission.id for permission in updated_instance.user_permissions.all()]
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "User update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_group', 'auth.add_group']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                "ok": True,
                "message": "Group created successfully",
                "data": {
                    "id": instance.id,
                    "name": instance.name,
                    "permissions": [permission.id for permission in instance.permissions.all()]
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "ok": False,
                "message": "Group creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_group', 'auth.change_group', 'auth.delete_group']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Group, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Group with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Group retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
    
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response({
                "ok": True,
                "message": "Group updated successfully",
                "data": {
                    "id": updated_instance.id,
                    "name": updated_instance.name,
                    "permissions": [permission.id for permission in updated_instance.permissions.all()]
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Group update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class PermissionListView(generics.ListAPIView):
    queryset = Permission.objects.order_by('id')
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_permission']
