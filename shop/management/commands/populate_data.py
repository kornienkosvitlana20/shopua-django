from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product


class Command(BaseCommand):
    help = 'Заповнити базу даних тестовими даними'

    def handle(self, *args, **options):
        self.stdout.write('Створення тестових даних...')

        # Суперюзер
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@shopua.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Суперкористувач admin створений (пароль: admin123)'))

        # Категорії
        categories_data = [
            ('Електроніка', 'elektronika', 'Смартфони, ноутбуки, планшети'),
            ('Одяг', 'odiah', 'Чоловічий та жіночий одяг'),
            ('Книги', 'knyhy', 'Книги різних жанрів'),
            ('Спорт', 'sport', 'Спортивний інвентар та одяг'),
            ('Дім та сад', 'dim-ta-sad', 'Товари для дому та саду'),
        ]
        categories = {}
        for name, slug, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc}
            )
            categories[slug] = cat

        # Товари
        products_data = [
            ('iPhone 15 Pro', 'iphone-15-pro', 'elektronika', '49999.00', 25,
             'Найновіший iPhone з чипом A17 Pro, 48МП камерою та titanium корпусом.'),
            ('MacBook Air M3', 'macbook-air-m3', 'elektronika', '55000.00', 10,
             'Надтонкий ноутбук Apple з чипом M3. 18 годин автономної роботи.'),
            ('Samsung Galaxy S24', 'samsung-galaxy-s24', 'elektronika', '35999.00', 30,
             'Флагман Samsung з 200МП камерою та AI функціями.'),
            ('Nike Air Max 270', 'nike-air-max-270', 'sport', '4500.00', 50,
             'Зручні спортивні кросівки Nike з технологією Air Max.'),
            ('Adidas Ultraboost', 'adidas-ultraboost', 'sport', '5200.00', 40,
             'Бігові кросівки Adidas з технологією Boost для максимального комфорту.'),
            ('Чоловіча куртка осінь', 'chol-kurtka-osin', 'odiah', '2800.00', 20,
             'Тепла та стильна осіння куртка для чоловіків.'),
            ('Жіноче плаття літо', 'zhin-plattia-lito', 'odiah', '1500.00', 35,
             'Легке літнє плаття з натуральної тканини.'),
            ('Гаррі Поттер. Повна серія', 'harry-potter-seriia', 'knyhy', '1200.00', 15,
             'Повна серія книг Гаррі Поттер від Дж. К. Роулінг українською мовою.'),
            ('Кобзар - Тарас Шевченко', 'kobzar-shevchenko', 'knyhy', '350.00', 100,
             'Відоме зібрання поезій Тараса Шевченка.'),
            ('Набір садових інструментів', 'nabir-sadovykh', 'dim-ta-sad', '890.00', 25,
             'Повний набір інструментів для догляду за садом та городом.'),
            ('Кавоварка DeLonghi', 'kavovar-delonghi', 'dim-ta-sad', '7500.00', 8,
             'Автоматична кавоварка DeLonghi для приготування еспресо та капучино.'),
            ('Ігровий ноутбук ASUS ROG', 'asus-rog-gaming', 'elektronika', '65000.00', 5,
             'Потужний ігровий ноутбук ASUS ROG з RTX 4060 та 165Hz дисплеєм.'),
        ]

        for name, slug, cat_slug, price, stock, desc in products_data:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'category': categories[cat_slug],
                    'price': price,
                    'stock': stock,
                    'available': True,
                    'description': desc,
                }
            )

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Створено {len(categories_data)} категорій та {len(products_data)} товарів.'
        ))
        self.stdout.write(self.style.WARNING(
            'Адмін: http://localhost:8000/admin/ | логін: admin | пароль: admin123'
        ))
