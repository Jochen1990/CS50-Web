from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Listings(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    start_bid = models.DecimalField(max_digits=1000, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category_name")
    image = models.CharField(max_length=100, default=None, blank=True)
    status = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=1000, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.title} : {self.description} : {self.start_bid} : {self.category} : {self.image}"

class UserListing(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default="none", related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="owner")

    def __str__(self):
        return f"{self.user.id}"
    
class Watchlist(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watched")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")

    def __str__(self):
        return f"{self.listing.title} : {self.user.username}"
    
class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="commentedon")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    comment = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.user.username} on {self.listing.title} said {self.comment}"

class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="biddingListing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddingUser")
    bid = models.DecimalField(max_digits=1000, decimal_places=2)

    def __str__(self):
        return f"{self.listing.title} : {self.user.username} : {self.bid}"


