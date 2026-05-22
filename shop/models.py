# Моделі розроблені: Корнієнко Світлана (Учасник 1)
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name='Опис')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='Зображення')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products',
        on_delete=models.CASCADE, verbose_name='Категорія'
    )
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/', blank=True, verbose_name='Зображення')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    stock = models.PositiveIntegerField(verbose_name='Залишок на складі')
    available = models.BooleanField(default=True, verbose_name='Доступний')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('processing', 'Обробляється'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='orders', verbose_name='Користувач'
    )
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=250, verbose_name='Адреса')
    city = models.CharField(max_length=100, verbose_name='Місто')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name='Статус'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created']

    def __str__(self):
        return f'Замовлення {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items',
        on_delete=models.CASCADE, verbose_name='Замовлення'
    )
    product = models.ForeignKey(
        Product, related_name='order_items',
        on_delete=models.CASCADE, verbose_name='Товар'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='cart', verbose_name='Користувач'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'

    def __str__(self):
        return f'Кошик {self.user.username}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cart_items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE,
        related_name='cart_items', verbose_name='Кошик'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    class Meta:
        verbose_name = 'Елемент кошика'
        verbose_name_plural = 'Елементи кошика'

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.product.price * self.quantity
