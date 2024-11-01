# payment/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user_display', 'amount', 'currency', 'transaction_id', 'status_display',
        'payment_method', 'customer_info', 'created_at', 'updated_at'
    )
    list_filter = (
        'status', 'currency', 'payment_method', 'created_at'
    )
    search_fields = (
        'transaction_id', 'user__username', 'customer_name', 'customer_email', 
        'customer_phone'
    )
    readonly_fields = ('transaction_id', 'created_at', 'updated_at')
    actions = ['mark_as_completed', 'mark_as_failed']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': (
                'user', 'amount', 'currency', 'transaction_id', 
                'status', 'payment_method'
            )
        }),
        ('Customer Information', {
            'fields': (
                'customer_name', 'customer_email', 'customer_phone', 
                'customer_address', 'customer_city', 'customer_postcode'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def user_display(self, obj):
        if obj.user:
            return format_html(
                f'<a href="/admin/auth/user/{obj.user.id}/change/">{obj.user.username}</a>'
            )
        return "Anonymous"
    user_display.short_description = 'User'

    def status_display(self, obj):
        color = {
            'PENDING': 'orange',
            'COMPLETED': 'green',
            'FAILED': 'red'
        }.get(obj.status, 'black')
        return format_html(
            f'<span style="color: {color}; font-weight: bold;">{obj.status}</span>'
        )
    status_display.short_description = 'Status'

    def customer_info(self, obj):
        return format_html(
            f'{obj.customer_name}<br>{obj.customer_email}<br>{obj.customer_phone}'
        )
    customer_info.short_description = 'Customer Info'
    
    @admin.action(description="Mark selected payments as Completed")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f"{updated} payment(s) marked as completed.")

    @admin.action(description="Mark selected payments as Failed")
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status='FAILED')
        self.message_user(request, f"{updated} payment(s) marked as failed.")
    
    def get_queryset(self, request):
        # Optimize by selecting related user records
        return super().get_queryset(request).select_related('user')
