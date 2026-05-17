"""
Tests for ShopUA Online Store
Tests written by: Team (2 members)
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart, CartItem, Order, OrderItem


# ============================
# MODEL TESTS (Member 1)
# ============================

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Електроніка',
            slug='elektronika',
            description='Електронні товари'
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Електроніка')

    def test_category_absolute_url(self):
        url = self.category.get_absolute_url()
        self.assertEqual(url, '/category/elektronika/')

    def test_category_slug_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(name='Дублікат', slug='elektronika')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тест', slug='test')
        self.product = Product.objects.create(
            category=self.category,
            name='Ноутбук Test',
            slug='noutbuk-test',
            price=Decimal('25000.00'),
            stock=10,
            available=True,
            description='Тестовий опис'
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Ноутбук Test')

    def test_product_absolute_url(self):
        url = self.product.get_absolute_url()
        self.assertIn(str(self.product.id), url)
        self.assertIn('noutbuk-test', url)

    def test_product_price_decimal(self):
        self.assertEqual(self.product.price, Decimal('25000.00'))

    def test_product_availability(self):
        self.assertTrue(self.product.available)

    def test_product_stock(self):
        self.assertEqual(self.product.stock, 10)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Тест', slug='test-cat')
        self.product = Product.objects.create(
            category=self.category,
            name='Товар',
            slug='tovar',
            price=Decimal('100.00'),
            stock=5
        )
        self.order = Order.objects.create(
            user=self.user,
            first_name='Іван',
            last_name='Тест',
            email='test@test.com',
            address='вул. Тестова 1',
            city='Київ',
            phone='+380501234567'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=3
        )

    def test_order_str(self):
        self.assertIn(str(self.order.id), str(self.order))

    def test_order_item_cost(self):
        cost = self.order_item.get_cost()
        self.assertEqual(cost, Decimal('300.00'))

    def test_order_total_cost(self):
        total = self.order.get_total_cost()
        self.assertEqual(total, Decimal('300.00'))

    def test_order_default_status(self):
        self.assertEqual(self.order.status, 'pending')

    def test_order_not_paid_by_default(self):
        self.assertFalse(self.order.paid)


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='cartuser',
            password='cartpass123'
        )
        self.category = Category.objects.create(name='Кат', slug='kat')
        self.product1 = Product.objects.create(
            category=self.category,
            name='Продукт 1',
            slug='produkt-1',
            price=Decimal('50.00'),
            stock=10
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='Продукт 2',
            slug='produkt-2',
            price=Decimal('75.00'),
            stock=5
        )
        self.cart = Cart.objects.create(user=self.user)
        self.item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

    def test_cart_str(self):
        self.assertIn('cartuser', str(self.cart))

    def test_cart_total_items(self):
        self.assertEqual(self.cart.get_total_items(), 3)

    def test_cart_total_price(self):
        total = self.cart.get_total_price()
        # 2 * 50 + 1 * 75 = 175
        self.assertEqual(total, Decimal('175.00'))

    def test_cart_item_total_price(self):
        self.assertEqual(self.item1.get_total_price(), Decimal('100.00'))


# ============================
# VIEW TESTS (Member 2)
# ============================

class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Категорія', slug='kategoria')
        self.product = Product.objects.create(
            category=self.category,
            name='Тест Продукт',
            slug='test-produkt',
            price=Decimal('999.99'),
            stock=5,
            available=True
        )
        self.unavailable_product = Product.objects.create(
            category=self.category,
            name='Недоступний',
            slug='nedostupnyi',
            price=Decimal('100.00'),
            stock=0,
            available=False
        )

    def test_product_list_status_200(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_shows_available_products(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertContains(response, 'Тест Продукт')

    def test_product_list_hides_unavailable(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertNotContains(response, 'Недоступний')

    def test_product_list_by_category(self):
        url = reverse('shop:product_list_by_category', args=['kategoria'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тест Продукт')

    def test_product_search(self):
        response = self.client.get(reverse('shop:product_list'), {'q': 'Тест'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тест Продукт')

    def test_product_search_no_results(self):
        response = self.client.get(reverse('shop:product_list'), {'q': 'xyz_nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Тест Продукт')


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Деталь', slug='detal')
        self.product = Product.objects.create(
            category=self.category,
            name='Детальний товар',
            slug='detalnyi-tovar',
            price=Decimal('1500.00'),
            stock=3,
            available=True,
            description='Детальний опис товару'
        )

    def test_product_detail_status_200(self):
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_shows_name(self):
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertContains(response, 'Детальний товар')

    def test_product_detail_shows_price(self):
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertContains(response, '1500')

    def test_unavailable_product_returns_404(self):
        p = Product.objects.create(
            category=self.category,
            name='Прихований',
            slug='prykhovanyy',
            price=Decimal('100.00'),
            stock=0,
            available=False
        )
        url = reverse('shop:product_detail', args=[p.id, p.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='cartviewuser',
            password='pass123456'
        )
        self.category = Category.objects.create(name='Кошик', slug='koshyk')
        self.product = Product.objects.create(
            category=self.category,
            name='Кошик Товар',
            slug='koshyk-tovar',
            price=Decimal('200.00'),
            stock=10,
            available=True
        )

    def test_cart_requires_login(self):
        response = self.client.get(reverse('shop:cart_detail'))
        self.assertRedirects(response, '/accounts/login/?next=/cart/')

    def test_cart_accessible_when_logged_in(self):
        self.client.login(username='cartviewuser', password='pass123456')
        response = self.client.get(reverse('shop:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        self.client.login(username='cartviewuser', password='pass123456')
        url = reverse('shop:cart_add', args=[self.product.id])
        response = self.client.post(url, {'quantity': 2})
        self.assertRedirects(response, reverse('shop:cart_detail'))
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.cart_items.count(), 1)
        self.assertEqual(cart.cart_items.first().quantity, 2)

    def test_remove_from_cart(self):
        self.client.login(username='cartviewuser', password='pass123456')
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        url = reverse('shop:cart_remove', args=[item.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('shop:cart_detail'))
        self.assertEqual(cart.cart_items.count(), 0)


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        response = self.client.get(reverse('shop:register'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        response = self.client.post(reverse('shop:register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        User.objects.create_user(username='logintest', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'logintest',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)


class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='orderuser',
            password='orderpass123'
        )
        self.category = Category.objects.create(name='Замовлення', slug='zamovlennia')
        self.product = Product.objects.create(
            category=self.category,
            name='Замовлення Товар',
            slug='zamovlennia-tovar',
            price=Decimal('300.00'),
            stock=10,
            available=True
        )

    def test_order_list_requires_login(self):
        response = self.client.get(reverse('shop:order_list'))
        self.assertEqual(response.status_code, 302)

    def test_order_list_accessible(self):
        self.client.login(username='orderuser', password='orderpass123')
        response = self.client.get(reverse('shop:order_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_order_with_cart(self):
        self.client.login(username='orderuser', password='orderpass123')
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        response = self.client.post(reverse('shop:order_create'), {
            'first_name': 'Іван',
            'last_name': 'Тестовий',
            'email': 'ivan@test.com',
            'address': 'вул. Тестова 1',
            'city': 'Київ',
            'phone': '+380501234567',
        })
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)

    def test_empty_cart_redirects_from_checkout(self):
        self.client.login(username='orderuser', password='orderpass123')
        response = self.client.post(reverse('shop:order_create'), {
            'first_name': 'Іван',
            'last_name': 'Тест',
            'email': 'test@test.com',
            'address': 'вул. 1',
            'city': 'Київ',
            'phone': '+380501234567',
        })
        self.assertRedirects(response, reverse('shop:product_list'))
