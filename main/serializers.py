from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group, Permission


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    size_name = serializers.CharField(source='size.name', read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_name', 'size', 'size_name', 'uniq_code']


class StockSerializer(serializers.ModelSerializer):
    variant_info = serializers.CharField(source='variant.__str__', read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'variant', 'variant_info', 'quantity', 'price']


class ImportInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportInvoice
        fields = ['supplier', 'user', 'state']

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


class StockMovementSerializer(serializers.ModelSerializer):
    variant_info = serializers.CharField(source='variant.__str__', read_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'variant', 'variant_info', 'type', 'quantity', 'description']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ExportInvoiceSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ExportInvoice
        fields = ['id', 'client', 'client_name', 'user', 'user_username', 'state']

    
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


class CashboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashbox
        fields = '__all__'


class CashboxMovementSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CashboxMovement
        fields = ['id', 'type', 'sum', 'remains', 'comment', 'payment_type', 'user', 'user_username', 'created_at', 'updated_at', 'deleted_at']

    
    
    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['user'] = user
        return super().create(validated_data)



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
