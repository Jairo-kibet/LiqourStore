from django.contrib import admin

# Register your models here.
from store.models import Contact,User,Whiskey,Gin,Beer

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('read',)  


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'birth_year')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('birth_year',)

@admin.register(Whiskey)
class WhiskeyAdmin(admin.ModelAdmin):
   list_display = ('name', 'category', 'abv', 'volume', 'price', 'created_at')
   search_fields = ('name', 'abv')
   list_filter = ('abv', 'created_at')
   ordering = ('-created_at',)

@admin.register(Gin)
class GinAdmin(admin.ModelAdmin):
   list_display = ('name', 'category', 'abv', 'volume', 'price', 'created_at')
   search_fields = ('name', 'abv')
   list_filter = ('abv', 'created_at')
   ordering = ('-created_at',)

@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
   list_display = ('name', 'category', 'abv', 'volume', 'price', 'created_at')
   search_fields = ('name', 'abv')
   list_filter = ('abv', 'created_at')
   ordering = ('-created_at',)