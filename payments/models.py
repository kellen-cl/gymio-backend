from django.db import models
from django.utils import timezone

# Create your models here.
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('mpesa', 'M-Pesa'),
        ('bank_transfer', 'Bank Transfer'),
        ('stripe', 'Stripe'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Relations
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payments')
    membership_plan = models.ForeignKey('memberships.MembershipPlan', on_delete=models.SET_NULL, null=True)
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Invoice
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    
    # Transaction IDs
    transaction_id = models.CharField(max_length=200, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    mpesa_receipt_number = models.CharField(max_length=100, blank=True)
    
    # Dates
    payment_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"{self.invoice_number} - {self.user.full_name} - {self.amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number
            last_payment = Payment.objects.order_by('-id').first()
            if last_payment:
                last_id = last_payment.id
            else:
                last_id = 0
            self.invoice_number = f"INV-{timezone.now().strftime('%Y%m%d')}-{str(last_id + 1).zfill(5)}"
        super().save(*args, **kwargs)