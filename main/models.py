from django.db import models, transaction
from django.utils import timezone
from django.db.models import Max
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel
from safedelete.config import SOFT_DELETE
from decimal import Decimal

class Supplier(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(default='Andijon Uzbekistan', max_length=150)
    balance = models.CharField(default=0, max_length=10000000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Size(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductVariant(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    uniq_code = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.uniq_code:
            with transaction.atomic():
                max_sku = ProductVariant.objects.select_for_update().aggregate(Max('uniq_code'))
                max_number = 1000 if max_sku['uniq_code__max'] is None else int(max_sku['uniq_code__max'].replace('SKU-', ''))
                self.uniq_code = f"SKU-{max_number + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.size.name}"

class Stock(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.variant} - {self.quantity} items"

class ImportInvoice(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=[('new', 'New'), ('accepted', 'Accepted'), ('canceled', 'Canceled')], default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.state}"

class ImportedInvoiceItem(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    import_invoice = models.ForeignKey(ImportInvoice, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    input_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StockMovement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    MOVEMENT_TYPES = [('arrival', 'Arrival'), ('departure', 'Departure')]

    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.variant} ({self.quantity})"

class Client(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    phone = models.IntegerField()
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ExportInvoice(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=[('new', 'New'), ('accepted', 'Accepted'), ('canceled', 'Canceled')], default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Export Invoice {self.id} - {self.state}"

class ExportedInvoiceItem(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    export_invoice = models.ForeignKey(ExportInvoice, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cashbox(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    remains = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def deposit(self, amount, comment='', payment_type='', user=None):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        with transaction.atomic():
            self.remains += amount
            self.save()
            CashboxMovement.objects.create(
                type='positive',
                sum=amount,
                remains=self.remains,
                comment=comment,
                payment_type=payment_type,
                user=user
            )

    def withdraw(self, amount, comment='', payment_type='', user=None):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.remains:
            raise ValueError("Insufficient funds.")
        with transaction.atomic():
            self.remains -= amount
            self.save()
            CashboxMovement.objects.create(
                type='negative',
                sum=amount,
                remains=self.remains,
                comment=comment,
                payment_type=payment_type,
                user=user
            )

    def reset(self, user=None):
        with transaction.atomic():
            self.remains = Decimal('0.00')
            self.save()
            CashboxMovement.objects.create(
                type='clear',
                sum=self.remains,
                remains=self.remains,
                comment='Cashbox reset',
                payment_type='',
                user=user
            )

class CashboxMovement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    TYPE_CHOICES = [('positive', 'Positive'), ('negative', 'Negative'), ('clear', 'Clear')]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    sum = models.DecimalField(max_digits=15, decimal_places=2)
    remains = models.DecimalField(max_digits=15, decimal_places=2)
    comment = models.CharField(max_length=255, blank=True)
    payment_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
