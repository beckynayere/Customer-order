from django.db import models

# Create your models here.
# orders/models.py
from django.db import models
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.shortcuts import reverse
from datetime import timedelta
from django.utils import timezone
# import datetime
from django.conf import settings
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Customer(models.Model):
   

    full_name = models.CharField(max_length=40, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, default="0000000000")  # Added default value
    email = models.EmailField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=50, unique=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.name.split()[0]

    # def __str__(self):
    #     return self.user.username
   
# class Order(models.Model):
#     customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
#     item = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} for {self.item}"
class Product(models.Model):
    name = models.CharField(max_length=150)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Add default value here
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=1000)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item} - {self.customer.name}"

    def __str__(self):
        return f'{self.name} product'

    def post_product(self):
        self.save()

    def delete_product(self):
        self.delete()

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"pk": self.pk})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"pk": self.pk})


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=17, blank=True,default='')
    last_name = models.CharField(max_length=17, blank=True, default='')
    email = models.EmailField(max_length=40, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    location = models.CharField(max_length=50, blank=True, null=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('U', 'Unisex/Parody'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='profile', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, default="0000000000") 

    def __str__(self):
        return self.user.email

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=250)
    address_second = models.CharField(max_length=250,null=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, null=True) 
    state = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    paid  = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {} {}'.format(self.user, self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
    related_name='order_items',
    on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product,
    related_name='order_products',
    on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# class Category(models.Model):
#     name = models.CharField(max_length=200, db_index=True)
#     slug = models.SlugField(max_length=200, db_index=True, unique=True)

#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('shop:product_list_by_category', args=[self.slug])

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
