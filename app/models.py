from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user_name = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    website = models.EmailField(max_length=60, null=True)
    bioInfo = models.TextField(null=True)
    mobile = models.CharField(max_length=150, null=True)


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    # Auto updated when data is altered
    updated_at = models.DateTimeField(auto_now_add=False, auto_now = True)

    name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=60, null=False)
    phone = models.CharField(max_length=60, null=False)
    subject = models.TextField(null = False)
    message = models.TextField(null = False)

    def __str__(self):
        return self.name

class Admin(models.Model):
    username = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=60, null=False)
    password = models.CharField(max_length=150, null=False)

class Agent(models.Model):
    username = models.CharField(max_length=150, null=False)
    agentId = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    email = models.EmailField(max_length=60, null=False)
    company = models.CharField(max_length=150, null=False)
    website = models.CharField(max_length=60, null=False)
    facebook = models.CharField(max_length=60, null=False)
    twitter = models.CharField(max_length=60, null=False)
    instagram = models.CharField(max_length=60, null=False)
    photo = models.ImageField(upload_to="blog_images", blank = True)


class Property(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    type = models.CharField(max_length=150, null=False)
    status = models.CharField(max_length=150, null=False)
    no_of_beds = models.IntegerField(null=False)
    no_of_bathrooms = models.IntegerField(null=False)
    pets = models.IntegerField(null=True)
    parking_area = models.CharField(max_length=150, null=False)
    area = models.CharField(max_length=150, null=True)
    lot_size = models.CharField(max_length=150, null=False)
    property_id = models.CharField(max_length=150, null=False)
    title = models.CharField(max_length=150, null=False)
    price = models.IntegerField(default=0, null=False)
    price_per_area = models.CharField(max_length=150, null=True)
    community = models.CharField(max_length=150, null=True)
    description = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    location = models.CharField(max_length=150, null=False)
    photo = models.ImageField(upload_to="property_images", blank = True)
    agent = models.ForeignKey(Agent, related_name='property', on_delete=models.CASCADE)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

class PropertyImages(models.Model):
    property = models.ForeignKey(Property, related_name="PropertyImages", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="property_images", blank=True)


class AccountType(models.Model):
    title = models.CharField(max_length=150, null=False)
    price = models.CharField(max_length=150, null=False)
    months = models.IntegerField(null=False)
    listing = models.IntegerField(null=False)
    featured_listings = models.IntegerField(null=False)


class Orders(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    package_id = models.ForeignKey(AccountType, related_name="Orders", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name="user_order", on_delete=models.CASCADE)
    method = models.CharField(max_length=150, null=False)