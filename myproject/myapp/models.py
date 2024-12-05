from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона должен быть в формате: '+999999999'. Допустимо от 9 до 15 цифр."
            )
        ]
    )
    address = models.CharField(max_length=200)
    reg_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField()
    image = models.ImageField(null=True, blank=True)
    added_at = models.DateField(auto_now=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    rating = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)  # Явно объявляем поле id
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    common_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Order #{self.id} by {self.client.name}"

