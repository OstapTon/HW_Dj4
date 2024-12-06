from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from myapp.forms import ImageForm
from . import models
from . import forms
from django.db.models import Sum


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def get_all_products(request):
    products = models.Product.objects.all()
    return render(request, 'products.html', {'products': products})


def change_product(request, product_id):
    product = models.Product.objects.filter(pk=product_id).first()
    form = forms.ProductForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        image = form.cleaned_data['image']
        if isinstance(image, bool):
            image = None
        if image is not None:
            fs = FileSystemStorage()
            fs.save(image.name, image)
        product.name = form.cleaned_data['name']
        product.description = form.cleaned_data['description']
        product.price = form.cleaned_data['price']
        product.amount = form.cleaned_data['amount']
        product.image = image
        product.save()
        return redirect('products')
    else:
        form = forms.ProductForm(initial={'name': product.name, 'description': product.description,
                                          'price': product.price, 'amount': product.amount, 'image': product.image})

    return render(request, 'change_product.html', {'form': form})


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES) # request.POST чтобы получить текстовую информацию , request.FILES чтобы получить байты
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()  # FileSystemStorage экземпляр позволяет работать с файлами
            fs.save(image.name, image)
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})

def total_in_db(request):
    total = models.Product.objects.aggregate(Sum('amount')) # сумма по столбцу количество aggregate - метод запроса к базе данных
    context = {
        'title': 'Общее количество посчитано в базеданных',
        'total': total,
    }
    return render(request, 'total_count.html', context) # total_count.htm универсальный шаблон для трех представлений


def total_in_view(request):
    products = models.Product.objects.all()                 # помещаем абсолютно все продукты
    total = sum(product.amount for product in products)  # перебераю каждый продкт, обращаюсь к его свойству amount и суммурую его
    context = {
        'title': 'Общее количество посчитано в представлении',
        'total': total,
    }
    return render(request, 'total_count.html', context)


def total_in_template(request):  # будет работать напрямую с классом продукт
    context = {
        'title': 'Общее количество посчитано в шаблоне',
        'products': models.Product,
    }
    return render(request, 'total_count.html', context)