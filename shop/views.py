# Views розроблені: Вялкова Поліна 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import OrderCreateForm, CheckoutForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})


@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f'"{product.name}" додано до кошика!')
    return redirect('shop:cart_detail')


@login_required
@require_POST
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Товар видалено з кошика.')
    return redirect('shop:cart_detail')


@login_required
def order_create(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if not cart.cart_items.exists():
        messages.warning(request, 'Ваш кошик порожній.')
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                # Зменшуємо залишок на складі
                item.product.stock -= item.quantity
                item.product.save()

            cart.cart_items.all().delete()
            messages.success(request, f'Замовлення #{order.id} успішно оформлено!')
            return redirect('shop:order_detail', order_id=order.id)
    else:
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'shop/order_create.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'shop/order_list.html', {'orders': orders})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна! Ласкаво просимо!')
            return redirect('shop:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
