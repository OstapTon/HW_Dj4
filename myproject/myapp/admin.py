from django.contrib import admin
from . import models


@admin.action(description="Сбросить количество до 0")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(amount=0)


@admin.register(models.Product)  # admin.site.register(Author) используем декоратор для каждой медели класса
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'amount']
    ordering = ['-amount']
    search_fields = ['description']
    search_help_text = 'Поиск по Описание продукта (description)'
    actions = [reset_quantity]

    # fields = ['name', 'description', 'price', 'amount', 'image', 'added_at']
    readonly_fields = ['added_at']
    fieldsets = [
        (
            None, {  # используем поле без определенного названия
                'classes': ['wide'],  # класс ['wide'] максимально большое поле в панели
                'fields': ['name'],  # в качестве поля name
            },
        ),
        (
            'Подробности',  # блок подробности
            {
                'classes': ['collapse'],  # скрытое поле
                'description': 'Категория товара и описание',  # при развороте выдает описание
                'fields': ['category', 'description'],  # поля которые мы спрятали
            },
        ),
        (
            'Финансы',
            {
                'fields': ['price', 'quantity'],
            }
        ),
        (
            'Рейтинг',
            {
                'description': 'Рейтинг сформирован автоматически на основе оценок покупателей',
                'fields': ['rating', 'date_added'],
            }
        ),
    ]


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    ordering = ['name']
    search_fields = ['name']
    search_help_text = 'Поиск по имени (name)'

    readonly_fields = ['reg_date']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'common_price']

    readonly_fields = ['date']


from django.contrib import admin

# Register your models here.
