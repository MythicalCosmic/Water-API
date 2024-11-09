from django.db import models, transaction
from django.utils import timezone
from django.db.models import Max
from django.contrib.auth.models import User

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)



    def __str__(self):
        return self.name
    

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)



    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    uniq_code = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.uniq_code:
            with transaction.atomic():
                max_sku = ProductVariant.objects.select_for_update().aggregate(Max('uniq_code'))
                max_number = int(max_sku['uniq_code__max'].replace('SKU-', '') or 1000)
                self.uniq_code = f"SKU-{max_number + 1}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.size.name}"

class Stock(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)



    def __str__(self):
        return f"{self.variant} - {self.quantity} items"
    
    
class ImportInvoice(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=[('new', 'New'), ('accepted', 'Accepted'), ('canceled', 'Canceled')])

    def __str__(self):
        return f"Invoice {self.id} - {self.state}"
    

class ImportedInvoiceItem(models.Model):
    import_invoice = models.ForeignKey(ImportInvoice, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    input_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()





class StockMovement(models.Model):
    MOVEMENT_TYPES = [('arrival', 'Arrival'), ('departure', 'Departure')]

    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)



    def __str__(self):
        return f"{self.type.capitalize()} - {self.variant} ({self.quantity})"
    

class Client(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=15)
    cud = models.CharField(max_length=20, unique=True)


    def __str__(self):
        return self.name


class ExportInvoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  null=True, blank=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=[('new', 'New'), ('accepted', 'Accepted'), ('canceled', 'Canceled')])

    def __str__(self):
        return f"Export Invoice {self.id} - {self.state}"


class ExportedInvoiceItem(models.Model):
    export_invoice = models.ForeignKey(ExportInvoice, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()



class Cashbox(models.Model):
    remains = models.DecimalField(max_digits=15, decimal_places=2)



class CashboxMovement(models.Model):
    TYPE_CHOICES = [('positive', 'Positive'), ('negative', 'Negative'), ('clear', 'Clear')]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    sum = models.DecimalField(max_digits=15, decimal_places=2)
    remains = models.DecimalField(max_digits=15, decimal_places=2)
    comment = models.CharField(max_length=255, blank=True)
    payment_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
