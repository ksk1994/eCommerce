from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_listing)
admin.site.register(Bid_price)
admin.site.register(Wish_list)
admin.site.register(Closebid)
admin.site.register(Addcomment)
admin.site.register(Category)