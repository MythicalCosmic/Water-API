from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group, Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from decimal import Decimal

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed({
                "ok": False,
                "error_code": "INVALID_CREDENTIALS",
                "message": "The provided credentials are incorrect or the account is inactive."
            })
        user = self.user
        data['username'] = getattr(self.user, 'username', None)
        data['role'] = user.groups.first().name if user.groups.exists() else None 
        data['permissions'] = list(user.get_all_permissions())
        data['superuser_status'] = user.is_superuser
        return data

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone_number']

        


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'category_name']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_data'] = {
            'category_id': data.pop('category', None),
            'category_name': data.pop('category_name', None) 
        }


        return data



class ProductVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    size_name = serializers.CharField(source='size.name', read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_name', 'size', 'size_name', 'uniq_code']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product_data'] = {
            'product_id': data.pop('product', None),
            'product_name': data.pop('product_name', None) 
        }
        data['size_data'] = {
            'size_id': data.pop('size', None),
            'size_name': data.pop('size_name', None),
        }
        return data


class StockSerializer(serializers.ModelSerializer):
    variant_data = serializers.CharField(source='variant.__str__', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'variant', 'variant_data', 'quantity', 'price', 'user', 'user_username']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['variant_data'] = {
            'variant_id': data.pop('variant', None),
            'variant_info': data.pop('variant_data', None),
        }
        data['user_data'] = {
            'user_id': data.pop('user', None),
            'username': data.pop('user_username', None),
        }
        return data



class ImportInvoiceSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = ImportInvoice
        fields = ['id', 'supplier', 'supplier_name', 'state', 'user', 'username']  

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_data'] = {
            'user_id': data.pop('user', None),
            'username': data.pop('username', None) 
        }
        data['supplier_data'] = {
            'supplier_id': instance.supplier.id,
            'supplier_name': instance.supplier.name
        }
        data.pop('user', None)
        data.pop('supplier', None)


        return data

    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['user'] = user
        return super().create(validated_data)


class ImportedInvoiceItemSerializer(serializers.ModelSerializer):
    import_invoice_info = serializers.CharField(source='import_invoice.__str__', read_only=True)
    variant_info = serializers.CharField(source='variant.__str__', read_only=True)

    class Meta:
        model = ImportedInvoiceItem
        fields = ['id', 'import_invoice', 'import_invoice_info', 'variant', 'variant_info', 'input_price', 'quantity']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['import_invoice_data'] = {
            'import_invoice_id': data.pop('import_invoice', None),
            'import_invoice_info': data.pop('import_invoice_info', None) 
        }
        data['variant_data'] = {
            'variant_id': data.pop('variant', None),
            'variant_info': data.pop('variant_info', None),
        }
        return data



class StockMovementSerializer(serializers.ModelSerializer):
    variant_info = serializers.CharField(source='variant.__str__', read_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'variant', 'variant_info', 'type', 'quantity', 'description']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['variant_data'] = {
            'variant_id': data.pop('variant', None),
            'variant_info': data.pop('variant_info', None),
        }
        data.pop('user', None)
        data.pop('supplier', None)


        return data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CashboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashbox
        fields = ['id', 'remains']

class ExportInvoiceSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ExportInvoice
        fields = ['id', 'client', 'client_name', 'user', 'user_username', 'state']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_data'] = {
            'user_id': data.pop('user', None),
            'username': data.pop('user_username', None) 
        }
        data['client_data'] = {
            'client_id': data.pop('client', None),
            'client_name': data.pop('client_name', None),
        }
        data.pop('user', None)
        data.pop('supplier', None)


        return data

    
    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['user'] = user
        return super().create(validated_data)


class ExportedInvoiceItemSerializer(serializers.ModelSerializer):
    export_invoice_info = serializers.CharField(source='export_invoice.__str__', read_only=True)
    variant_info = serializers.CharField(source='variant.__str__', read_only=True)

    class Meta:
        model = ExportedInvoiceItem
        fields = ['id', 'export_invoice', 'export_invoice_info', 'variant', 'variant_info', 'price', 'quantity']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['export_invoice_data'] = {
            'export_invoice_id': data.pop('export_invoice', None),
            'export_invoice_info': data.pop('export_invoice_info', None) 
        }
        data['variant_data'] = {
            'variant_id': data.pop('variant', None),
            'variant_info': data.pop('variant_info', None),
        }
        data.pop('user', None)
        data.pop('supplier', None)


        return data




class CashboxMovementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = CashboxMovement
        fields = ['id', 'type', 'sum', 'remains', 'comment', 'payment_type', 'user', 'created_at', 'updated_at', 'deleted_at']
    
    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "username": obj.user.username,
            }
        return None



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def create(self, validated_data):
        permissions = self.initial_data.get('permissions', [])
        group = Group.objects.create(name=validated_data['name'])
        group.permissions.set(permissions)
        return group

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        permissions = self.initial_data.get('permissions', None)
        if permissions is not None:
            instance.permissions.set(permissions)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False, many=True)
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), required=False, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if groups:
            instance.groups.set(groups)
        if user_permissions:
            instance.user_permissions.set(user_permissions)

        return instance
