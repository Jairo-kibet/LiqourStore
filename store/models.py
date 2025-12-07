from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # optional to mark if admin has read

    def __str__(self):
        return f"{self.name} - {self.subject}"


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    birth_year = models.IntegerField()
    password = models.CharField(max_length=128)  # In production, use hashed password

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Whiskey(models.Model):
    CATEGORY_CHOICES = [
        ('Scotch', 'Scotch'),
        ('Bourbon', 'Bourbon'),
        ('Cognac', 'Cognac'),
        ('Indian ', 'SIndian '),
        ('Single malt', 'Single malt'),
        ('Blended scotch', 'Blended scotch '),
        
       # add more
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Scotch')
    abv = models.CharField(max_length=20)
    volume = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='whiskey/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Beer(models.Model):
    CATEGORY_CHOICES = [
        ('Red wine', 'Red wine'),
        ('White wine', 'White wine'),
        ('Rose wine', 'Rose wine'),
        ('Sparkling wine', 'Sparkling wine'),
        ('Single malt', 'Single malt'),
        ('Port wine', 'Port wine'),
        ('Red sweet wine', 'Red sweet wine'),
        ('White sweet wine', 'White sweet wine'),
        ('White dry wine', 'White wine'),
        ('Red dry wine', 'Red dry wine'),
        
       # add more
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Scotch')
    abv = models.CharField(max_length=20)
    volume = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='beer/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Gin(models.Model):
    CATEGORY_CHOICES = [
        ('London dry gin', 'London dry gin'),
        ('Flavoured gin', 'Flavoured gin'),
        ('Sloe gin', 'Sloe gin'),
        ('Plymouth gin', 'Plymouth gin'),
        ('International style gin', 'International style gin'),
      
        
       # add more
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Scotch')
    abv = models.CharField(max_length=20)
    volume = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Gin/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Wishlist(models.Model):
    whiskey = models.ForeignKey('Whiskey', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.whiskey.name





  
class Cart(models.Model):
    whiskey = models.ForeignKey('Whiskey', on_delete=models.CASCADE)  # Or Product
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.whiskey.name} ({self.quantity})"
    
    @property
    def item_total(self):
        return self.whiskey.price * self.quantity