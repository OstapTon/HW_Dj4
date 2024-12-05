from django.contrib import admin
from .models import Product, Client, Order


@admin.action(description="Сбросить количество до 0")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(amount=0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'amount', 'category', 'rating']
    ordering = ['-amount']
    search_fields = ['description']
    search_help_text = 'Поиск по описанию продукта (description)'
    actions = [reset_quantity]

    readonly_fields = ['added_at']
    fieldsets = [
        (
            None, {
                'classes': ['wide'],
                'fields': ['name', 'category'],
            },
        ),
        (
            'Подробности',
            {
                'classes': ['collapse'],
                'description': 'Описание продукта',
                'fields': ['description', 'image'],
            },
        ),
        (
            'Финансы',
            {
                'fields': ['price', 'amount'],
            }
        ),
        (
            'Рейтинг',
            {
                'description': 'Рейтинг сформирован автоматически на основе оценок покупателей',
                'fields': ['rating'],
            }
        ),
        (
            'Дата добавления',
            {
                'fields': ['added_at'],
            }
        ),
    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    ordering = ['name']
    search_fields = ['name']
    search_help_text = 'Поиск по имени (name)'

    readonly_fields = ['reg_date']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'common_price', 'date']
    readonly_fields = ['date']
