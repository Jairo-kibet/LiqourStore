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
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

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
