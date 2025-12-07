from django.shortcuts import render,redirect, get_object_or_404
from store.forms import ContactForm
from django.contrib import messages
from .models import *
from datetime import datetime
# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect("login")
    return render(request, "index.html")

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, "contact.html")


def blog(request):
    return render(request, 'blog.html')

def product(request):  
    return render(request, 'product.html')


def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.whiskey.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



def product_single(request):
    return render(request, 'product-single.html')

def whisky(request):
    whiskeys = Whiskey.objects.all()
    return render(request, 'whisky.html', {'whiskeys': whiskeys})

def gin(request):
    gin = Gin.objects.all()
    return render(request, 'gin.html', {'gin': gin})

def beer(request):
    beers = Beer.objects.all()
    return render(request, 'beer.html', {'beer': beer})

from django.http import JsonResponse

def add_to_wishlist(request, id):
    whiskey = get_object_or_404(Whiskey, id=id)

    exists = Wishlist.objects.filter(whiskey=whiskey).exists()

    if exists:
        messages.error(request, f"{whiskey.name} is already in your favourites.")
    else:
        Wishlist.objects.create(whiskey=whiskey)
        messages.success(request, f"{whiskey.name} added to favourites!")

    return redirect('whisky')  # change 'whiskey' to your page name
 

def wishlist_page(request):
    items = Wishlist.objects.all()
    return render(request, "wishlist.html", {"items": items})

def profile(request):
    return render(request, 'profile.html')

# Register view

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        birth_year = int(request.POST.get("birth_year"))
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check age
        current_year = datetime.now().year
        age = current_year - birth_year
        if age < 18:
            messages.error(request, "You must be 18+ years old to register.")
            return redirect("register")

        # Password confirmation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please login.")
            return redirect("login")

        # Save user in database
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            birth_year=birth_year,
            password=password  # in production, use hashed password
        )
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "register.html")



# Login view
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Check if a user exists with the given email and password
            user = User.objects.get(email=email, password=password)

            # Successful login → store user id in session
            request.session['user_id'] = user.id

            # Redirect to home/index page
            return redirect("/")

        except User.DoesNotExist:
            # Invalid credentials
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "login.html")



# Logout
def logout(request):
    request.session.flush()
    return redirect("login")


def add_to_cart(request, id):
    whiskey = get_object_or_404(Whiskey, id=id)
    cart = request.session.get('cart', {})

    key = str(whiskey.id)

    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'name': whiskey.name,
            'price': float(whiskey.price),  # make sure it's a number
            'quantity': 1,
            'image': whiskey.image.url
        }

    request.session['cart'] = cart
    messages.success(request, f"{whiskey.name} added to cart.")
    return redirect('whisky')


def remove_from_wishlist(request, id):
    try:
        # Get the wishlist item by its ID
        item = Wishlist.objects.get(id=id)
    except Wishlist.DoesNotExist:
        messages.error(request, "Item not found in wishlist.")
        return redirect("wishlist")

    whiskey_name = item.whiskey.name
    item.delete()

    messages.success(request, f"{whiskey_name} removed from wishlist.")
    return redirect("wishlist")


def cart(request):
    cart = request.session.get('cart', {})

    # FIX: remove old integer items from old cart system
    cleaned_cart = {}
    for key, item in cart.items():
        if isinstance(item, dict):  # keep only new-format items
            cleaned_cart[key] = item
    request.session['cart'] = cleaned_cart
    cart = cleaned_cart

    cart_items = []
    total_price = 0

    for whiskey_id, data in cart.items():
        item_total = data['price'] * data['quantity']
        total_price += item_total

        cart_items.append({
            'id': whiskey_id,
            'name': data['name'],
            'price': data['price'],
            'quantity': data['quantity'],
            'image': data['image'],
            'item_total': item_total
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })






def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")

    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for item_id, item in cart.items():
        cart_items.append({
            'id': item_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item['price'] * item['quantity'],
            'image': item['image'],
        })
        total_price += item['price'] * item['quantity']

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def place_order(request):
    if request.method == "POST":
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        cart = request.session.get('cart', {})

        # save order
        order = Order.objects.create(
            first_name=first,
            last_name=last,
            phone=phone,
            email=email,
            address=address,
            total_amount=sum(item['price'] * item['quantity'] for item in cart.values())
        )

        # save order items
        for item_id, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_id=item_id,
                price=item['price'],
                quantity=item['quantity']
            )

        # clear cart
        request.session['cart'] = {}

        messages.success(request, "Order placed successfully!")

        return redirect('index')
