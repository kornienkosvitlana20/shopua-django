from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem

admin.site.site_header = 'Адміністрування Онлайн-магазину'
admin.site.site_title = 'Магазин Admin'
admin.site.index_title = 'Панель управління'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    raw_id_fields = ['category']
    date_hierarchy = 'created'
    ordering = ['name', 'category']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'city', 'status', 'paid', 'created', 'get_total_cost']
    list_filter = ['paid', 'status', 'created', 'updated']
    list_editable = ['paid', 'status']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'user__username']
    date_hierarchy = 'created'
    ordering = ['-created']

    def get_total_cost(self, obj):
        return f'{obj.get_total_cost()} грн'
    get_total_cost.short_description = 'Сума замовлення'


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'updated']
    inlines = [CartItemInline]

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Кількість товарів'

    def get_total_price(self, obj):
        return f'{obj.get_total_price()} грн'
    get_total_price.short_description = 'Загальна сума'
