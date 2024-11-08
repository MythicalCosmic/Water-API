from django.db import models
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Size(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.CASCADE)
    sku = models.CharField(max_length=20, unique=True, blank=True)

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Product)
def generate_sku(sender, instance, **kwargs):
    if not instance.sku:
        last_product = Product.objects.order_by('id').last()
        last_sku = int(last_product.sku.split('-')[1]) if last_product else 999
        new_sku_number = last_sku + 1
        instance.sku = f"SKU-{new_sku_number}"



class Branch(models.Model):
    name = models.CharField(max_length=100)


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)



class ProductVariant(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size_id = models.ForeignKey(Size, null=True, on_delete=models.CASCADE)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)

    def __str__(self):
        return self.name


User.add_to_class('role', models.ForeignKey(Role, null=True, on_delete=models.SET_NULL))