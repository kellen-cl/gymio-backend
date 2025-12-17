from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'user', 'amount', 'currency', 'status', 'payment_method', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['invoice_number', 'user__email', 'transaction_id']
    date_hierarchy = 'payment_date'
    readonly_fields = ['invoice_number']
