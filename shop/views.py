from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem
from .forms import AddressForm
# Create your views here.


def homepage(request):
    categories_list = list(Category.objects.all())
    products = list(Product.objects.all())

    paginator = Paginator(categories_list, 3)

    page_number = request.GET.get('page')
    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    return render(request, 'homepage.html', {"categories": categories, "products": products})


def product_detail_view(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product.html', {'product': product})


def category_view(request, id):
    products = list(Product.objects.filter(category__id=id))

    paginator = Paginator(products, 6)

    page_number = request.GET.get('page')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'products': products, 'page': page})


@login_required()
def cart_view(request):
    cart = request.session.get('cart')
    return render(request, 'cart.html', {'cart': cart})


@login_required()
def add_to_cart_view(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get('cart', {})

    if product.name in cart:
        cart[product.name]['quantity'] += 1
    else:
        cart[product.name] = {
            'id': id,
            'quantity': 1,
        }

    request.session['cart'] = cart

    return redirect('cart')


@login_required()
def remove_from_cart(request, id):
    cart = request.session.get('cart')
    product = Product.objects.get(id=id)

    if cart[product.name]['quantity'] > 1:
        cart[product.name]['quantity'] -= 1
    else:
        del cart[product.name]

    request.session['cart'] = cart

    return redirect('cart')


def product_search_view(request):
    name = request.GET.get('name')
    description = request.GET.get('desc')
    price = request.GET.get('price')
    category = request.GET.get('category')
    fields = {}

    if name:
        fields['name__icontains'] = name
    if description:
        fields['description__icontains'] = description
    if price:
        fields['price'] = price
    if category:
        fields['category__name__icontains'] = category

    products = list(Product.objects.filter(**fields))

    paginator = Paginator(products, 6)

    page_number = request.GET.get('page')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'productsearch.html', {"products": products, "page": page})


@login_required()
def checkout_view(request):
    form = AddressForm()
    return render(request, 'checkout.html', {'form': form})


@login_required()
def order_confirmation_view(request):
    cart = request.session.get('cart')
    total = 0
    for item, info in cart.items():
        product = Product.objects.get(id=info['id'])
        if product.stock < info['quantity']:
            messages.error(request, f'not enough {product.name} stock.')
            return redirect('checkout')
        total += product.price * info['quantity']

    order = Order.objects.create(
        user=request.user,
        total_price=total,
        status='Paid',
    )

    form = AddressForm(request.POST, instance=order)
    form.save()

    for item, info in cart.items():
        product = Product.objects.get(id=info['id'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=info['quantity'],
            unit_price=product.price,
        )
        if product.stock == info['quantity']:
            product.delete()
        else:
            product.stock -= info['quantity']
            product.save()

    del request.session['cart']

    return render(request, 'confirm.html')


def order_history_view(request):
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()

    return render(request, 'orderhistory.html', {"orders": orders, "order_items": order_items})












