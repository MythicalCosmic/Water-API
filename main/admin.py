from django.contrib import admin
from . models import *

admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Stock)
admin.site.register(ImportInvoice)
admin.site.register(ImportedInvoiceItem)
admin.site.register(StockMovement)
admin.site.register(Client)
admin.site.register(ExportInvoice)
admin.site.register(ExportedInvoiceItem)
admin.site.register(Cashbox)
admin.site.register(CashboxMovement)