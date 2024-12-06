from django.contrib import admin
from .models import Product


@admin.action(description="Сбросить количество в ноль")
def reset_quantity(modeladmin, request, queryset): # модель, запрос и база данных
    queryset.update(amount=0) # то что выбрал, хочу обновить до значения 0


class ProductAdmin(admin.ModelAdmin):
    """Импорты остались без изменения. Создаём класс Product Admin как дочерний для
    admin.ModelAdmin. Он позволит изменить работу с продуктами в админке, не меняя
    модель Продукты. Следовательно нам не надо делать миграции, вносить изменения
    в базу данных."""
    list_display = ['name', 'amount'] #Переменная list_display является зарезервированным именем. Django автоматически найдёт её и прочитает содержимое списка.
    ordering = ['-amount'] # ordering также является зарезервированнымименем.двухуровневая сортировка продуктов.В начале по категориям по возрастанию первичного ключа, далее по количеству по убыванию в нутри категории.
    list_filter = ['price']
    search_fields = ['description']
    search_help_text = 'Поиск по полю Описание продукта (description)'
    actions = [reset_quantity]  # добавляем нашу функцию с декоратором
    """Отдельный продукт."""
#     #fields = ['name', 'description', 'category', 'date_added', 'rating'] #fields определяет порядок вывода элементов формы.Если опустить какие-тополя,они перестанут отображаться.
#     readonly_fields = ['date_added', 'rating'] # readonly_fields также содержит список полей. Эти поля можно просматривать,но нельзя изменять.Мы сделали неизменяемым рейтинг.
# # 'date_added' изначально было неизменяемым, так как дата проставялется автоматическивмоментсозданиязаписи.Подобноеповедениемыуказалив модели: ... date_added=models.DateTimeField(auto_now_add=True)
    # readonly_fields = ['date_added']
    fieldsets = [
        (
            None, {                  # используем поле без определенного названия
                'classes': ['wide'],  # класс ['wide'] максимально большое поле в панели
                'fields':['name'],   # в качестве поля name
            },
        ),
        (
            'Подробности',           # блок подробности
            {
                'classes': ['collapse'], # схлопнутое поле(скрытое)
                'description': 'Категория товара и описание',# при развороте выдает описание
                'fields': ['description'],# те поля которые мы спрятали
            },
        ),
        (
            'Финансы',
            {
                'fields': ['price','amount'],
            }
        ),
        (
            'Рейтинг',
            {
                'description': 'Рейтинг сформирован автоматически на основе оценок покупателей',
                'fields': ['date_added'],
            }
        ),
    ]



admin.site.register(Product, ProductAdmin)