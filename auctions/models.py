from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_listing(models.Model):
    user = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.URLField(max_length=200)
    category = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.id}{self.user}{self.category}{self.name}{self.price}{self.timestamp}. {self.description} {self.image}"


class Bid_price(models.Model):
    user = models.CharField(max_length=64)
    item = models.IntegerField()
    bid_price = models.IntegerField()

    def __str__(self):
        return f"{self.bid_price}"


class Wish_list(models.Model):
    user = models.CharField(max_length=64)
    item = models.IntegerField()
    
    def __str__(self):
        return f"{self.id}{self.user}{self.item}"

class Closebid(models.Model):
    user = models.CharField(max_length=64)
    item = models.IntegerField()
    winner = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.user}{self.item}{self.winner}"

class Addcomment(models.Model):
    user = models.CharField(max_length=64)
    item = models.IntegerField()
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}{self.comment}{self.item}{self.time}"

class Category(models.Model):
    category = models.CharField(max_length=64)
    item = models.IntegerField()
    
    def __str__(self):
        return f"{self.category}{self.item}"