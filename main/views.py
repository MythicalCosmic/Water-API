from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *  
from .decorators import * 
import jwt
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from datetime import datetime
import pytz
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404




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
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_supplier', 'view_supplier']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Suppliers retrieved successfully",
            "data": serializer.data  
        })
    
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
    queryset = Supplier.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Supplier with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Supplier deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)
    

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Categories retrieved successfully",
            "data": serializer.data
        })

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Category with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Category deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Size Views
class SizeListCreateView(generics.ListCreateAPIView):
    queryset = Size.objects.all()
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
            "ok": True,
            "message": "Category retrieved successfully",
            "data": serializer.data  
        })
        
        return Response({
            "ok": False,
            "message": "Size creation failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Size retrieved successfully",
            "data": serializer.data
        })


class SizeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Size with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Size deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Product retrieved successfully",
            "data": serializer.data
        })


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Product with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Product deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Product Variant Views
class ProductVariantListCreateView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_productvariant', 'view_productvariant']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
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
                "message": "Product Variant created successfully",
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
                "message": "Product Variant creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Product Variant retrieved successfully",
            "data": serializer.data
        })


class ProductVariantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Product Variant with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Product Variant deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)


# Stock Views
class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_stock', 'view_stock']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()

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
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Stock retrieved successfully",
            "data": serializer.data
        })



class StockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_stock', 'view_stock']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Stock with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

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
            updated_instance = serializer.save() 
            variant_data = {
                "id": instance.variant.id,
            }
            
            return Response({
                "ok": True,
                "message": "Stock updated successfully",
                "data": {
                    "id": instance.id,
                    "variant": variant_data,
                    "quantity": instance.quantity,
                    "price": instance.price,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Stock update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Stock with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Stock deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)


# Import Invoice Views
class ImportInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ImportInvoice.objects.all()
    serializer_class = ImportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importinvoice', 'view_importinvoice']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()

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
                "message": "Import Invoice created successfully",
                "data": {
                    "id": instance.id,
                    "supplier": supplier_data,
                    "user": user_data,
                    "state": instance.state,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Import Invoice creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Import Invoice retrieved successfully",
            "data": serializer.data
        })


class ImportInvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportInvoice.objects.all()
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
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
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
                "message": "Import Invoice updated successfully",
                "data": {
                    "id": instance.id,
                    "supplier": supplier_data,
                    "user": user_data,
                    "state": instance.state,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Import Invoice update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Import Invoice with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Import Invoice deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)


# Imported Invoice Item Views
class ImportedInvoiceItemListCreateView(generics.ListCreateAPIView):
    queryset = ImportedInvoiceItem.objects.all()
    serializer_class = ImportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_importedinvoiceitem', 'view_importedinvoiceitem']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()

            import_invoice_data = {
                "id": instance.import_invoice.id,
            }
            variant_data = {
                "id": instance.variant.id,

            }
            return Response({
                "ok": True,
                "message": "Import Invoice Item created successfully",
                "data": {
                    "id": instance.id,
                    "supplier": import_invoice_data,
                    "variant": variant_data,
                    "input_price": instance.input_price,
                    "quantity": instance.quantity,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Import Invoice Item creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Import Invoice Item retrieved successfully",
            "data": serializer.data
        })



class ImportedInvoiceItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportedInvoiceItem.objects.all()
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
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            import_invoice_data = {
                "id": instance.import_invoice.id,
            }
            variant_data = {
                "id": instance.variant.id,
            }
            
            return Response({
                "ok": True,
                "message": "Import Invoice Item updated successfully",
                 "data": {
                    "id": instance.id,
                    "supplier": import_invoice_data,
                    "variant": variant_data,
                    "input_price": instance.input_price,
                    "quantity": instance.quantity,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Import Invoice Item update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Imported Invoice Item with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Imported Invoice Item deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Stock Movement Views
class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all()
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
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Stock Movement retrieved successfully",
            "data": serializer.data
        })




class StockMovementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockMovement.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Stock Movement  with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Stock Movement deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Client Views
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
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
                    "cud": instance.cud,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Client creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Client retrieved successfully",
            "data": serializer.data
        })


class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
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
                    "cud": instance.cud,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Client update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Client with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Client deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Export Invoice Views
class ExportInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ExportInvoice.objects.all()
    serializer_class = ExportInvoiceSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_exportinvoice', 'view_exportinvoice']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()
            client_data = {
                "id": instance.client.id,
                "name": instance.client.name
            }
            user_data = {
                "id": instance.user.id,
                "username": instance.user.username
            }
            return Response({
                "ok": True,
                "message": "Export Invoice created successfully",
                "data": {
                    "id": instance.id,
                    "client": client_data,
                    "user": user_data,
                    "state": instance.state,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Expoort Invoice creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Export Invoice retrieved successfully",
            "data": serializer.data
        })


class ExportInvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportInvoice.objects.all()
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
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_instance = serializer.save() 
            client_data = {
                "id": instance.client.id,
                "name": instance.client.name
            }
            user_data = {
                "id": instance.user.id,
                "username": instance.user.username
            }
            return Response({
                "ok": True,
                "message": "Export Invoice updated successfully",
               "data": {
                    "id": instance.id,
                    "client": client_data,
                    "user": user_data,
                    "state": instance.state,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Export Invoice  update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Export Invoice with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Export Invoice deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Exported Invoice Item Views
class ExportedInvoiceItemListCreateView(generics.ListCreateAPIView):
    queryset = ExportedInvoiceItem.objects.all()
    serializer_class = ExportedInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_exportedinvoiceitem', 'view_exportedinvoiceitem']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()
            export_invoice_data = {
                "id": instance.export_invoice.id,
            }
            variant_data = {
                "id": instance.variant.id,
            }
            return Response({
                "ok": True,
                "message": "Export Invoice Item created successfully",
                "data": {
                    "id": instance.id,
                    "export_invoice": export_invoice_data,
                    "variant": variant_data,
                    "price": instance.price,
                    "quantity": instance.quantity,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Expoort Invoice Item creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Export Invoice Item retrieved successfully",
            "data": serializer.data
        })


class ExportedInvoiceItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportedInvoiceItem.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Export Invoice Item with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Export Invoice Item deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)



# Cashbox Views
class CashboxListCreateView(generics.ListCreateAPIView):
    queryset = Cashbox.objects.all()
    serializer_class = CashboxSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashbox', 'view_cashbox']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                "ok": True,
                "message": "Cashbox Item created successfully",
                "data": {
                    "id": instance.id,
                    "remains": instance.remains,
                }
            }, status=status.HTTP_201_CREATED)
    
        else:
            return Response({
                "ok": False,
                "message": "Cashbox creation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Cashbox retrieved successfully",
            "data": serializer.data
        })



class CashboxRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cashbox.objects.all()
    serializer_class = CashboxSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_cashbox', 'view_cashbox']
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Cashbox with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "ok": True,
            "message": "Cashbox retrieved successfully",
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
                "message": "Cashbox updated successfully",
                "data": {
                    "id": instance.id,
                    "remains": instance.remains,
                }
            })
        else:
            return Response({
                "ok": False,
                "message": "Cashbox update failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Cashbox with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Cashbox deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)




# Cashbox Movement Views
class CashboxMovementListCreateView(generics.ListCreateAPIView):
    queryset = CashboxMovement.objects.all()
    serializer_class = CashboxMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_cashboxmovement', 'view_cashboxmovement']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            instance = serializer.save()
            user_data = {
                "id": instance.user.id,
                "username": instance.user.username,
            }
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
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "CashboxMovement retrieved successfully",
            "data": serializer.data
        })



class CashboxMovementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CashboxMovement.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "CashboxMovement with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "CashboxMovement deleted successfully",
            "data": {} 
        }, status=status.HTTP_204_NO_CONTENT)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Users retrieved successfully",
            "data": serializer.data
        })

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
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
                    "email": updated_instance.email,
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(User, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "User with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "User deleted successfully",
            "data": {}
        }, status=status.HTTP_204_NO_CONTENT)


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
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

    def list(self, request, *args, **kwargs):   
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Groups retrieved successfully",
            "data": serializer.data
        })


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Group, pk=kwargs['pk'])
        except:
            return Response({
                "ok": False,
                "message": "Group with the specified ID does not exist",
            }, status=status.HTTP_404_NOT_FOUND)
    
        instance.delete()
        return Response({
            "ok": True,
            "message": "Group deleted successfully",
            "data": {}
        }, status=status.HTTP_204_NO_CONTENT)


class PermissionListView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_permission']
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ok": True,
            "message": "Permissions retrieved successfully",
            "data": serializer.data
        })
