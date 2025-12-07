from django.urls import path
from store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('product/', views.product, name='product'),
    path('product-single/', views.product_single, name='product-single'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('whisky/', views.whisky, name='whisky'),
    path('beer/', views.beer, name='beer'),
    path('gin/', views.gin, name='gin'),
    path('place-order/', views.place_order, name='place_order'),

    # Wishlist
    path("add_to_wishlist/<int:id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", views.wishlist_page, name="wishlist"),
    path("remove_from_wishlist/<int:id>/", views.remove_from_wishlist, name="remove_from_wishlist"),


    # Cart
    path("add_to_cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path('remove/<str:id>/', views.remove_from_cart, name='remove_from_cart'),


    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
