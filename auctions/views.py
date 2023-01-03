from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        item = Auction_listing()
        item.user = request.user.username
        item.name = request.POST["name"]
        item.description = request.POST["desc"]
        item.price = int(request.POST["price"])
        item.category = request.POST["ctg"]
        message = ""
        if not item.name or not item.description or not item.price:
            message = "Please! Fill all nessessary form!"
        else:
        # checking if there is img_url
            if request.POST["img_url"]:
                item.image = request.POST["img_url"]
            else:
                item.image = "https://st3.depositphotos.com/1322515/35964/v/450/depositphotos_359648638-stock-illustration-image-available-icon.jpg"
            # creating new listing
            item.save()
            item = Auction_listing.objects.get(name=item.name, description=item.description)
            # adding category to new listing
            category = Category()
            category.category = item.category
            category.item = item.id
            category.save()
        items = Auction_listing.objects.all()
        return render(request, "auctions/index.html", {
            "items": items,
            "message":message
        })

    else:
        return render(request, "auctions/create_listing.html")


def index(request):
    return render(request, "auctions/index.html", {
        "items":Auction_listing.objects.all()
    })


def listing(request, item_id):
    if request.method == "POST":
        bid = Bid_price()
        bid.user = request.user.username
        bid.item = item_id
        bid.bid_price = int(request.POST["bid_price"])
        # saving new bid
        bid.save()
        bids = Bid_price.objects.filter(item=item_id)
        bid_count = len(bids)
        listing_item = Auction_listing.objects.get(id=item_id)
        highest_price = Bid_price.objects.filter(item=item_id).order_by("-bid_price").first()
        wish = Wish_list.objects.filter(user=request.user.username, item=item_id)
        closeitem = Closebid.objects.filter(item=item_id).first()
        comm = Addcomment.objects.filter(item=item_id).order_by("time")
        min_price = 0
        if highest_price:
            min_price = int(highest_price.bid_price) + 1
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm,
            "min_price":min_price
        })
    else:
        bids = Bid_price.objects.filter(item=item_id)
        bid_count = len(bids)
        listing_item = Auction_listing.objects.get(id=item_id)
        highest_price = Bid_price.objects.filter(item=item_id).order_by("-bid_price").first()
        wish = Wish_list.objects.filter(user=request.user.username, item=item_id)
        closeitem = Closebid.objects.filter(item=item_id).first()
        comm = Addcomment.objects.filter(item=item_id).order_by("time")
        min_price = 0
        if highest_price:
            min_price = int(highest_price.bid_price) + 1
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm,
            "min_price":min_price
        })

@login_required(login_url='/login')
def add_wish_list(request, item_id):
    bids = Bid_price.objects.filter(item=item_id)
    bid_count = len(bids)
    listing_item = Auction_listing.objects.get(id=item_id)
    highest_price = Bid_price.objects.filter(item=item_id).order_by("-bid_price").first()
    added = Wish_list.objects.filter(user=request.user.username, item=item_id)
    comm = Addcomment.objects.filter(item=item_id).order_by("time")
    closeitem = Closebid.objects.filter(item=item_id).first()
    min_price = 0
    if highest_price:
        min_price = int(highest_price.bid_price) + 1
    # checking if item is already in wish list
    if added:
        added.delete()
        wish = Wish_list.objects.filter(user=request.user.username, item=item_id)
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm,
            "min_price":min_price
        })
    else:
        wishlist = Wish_list()
        wishlist.user = request.user.username
        wishlist.item = item_id
        wishlist.save()
        wish = Wish_list.objects.filter(user=request.user.username, item=item_id)
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm,
            "min_price":min_price
        })

@login_required(login_url='/login')
def wishlists(request):
    wishlists = Wish_list.objects.filter(user=request.user.username)
    wish_listings = []
    if wishlists:
        for wishlist in wishlists:
            listing = Auction_listing.objects.get(id=wishlist.item)
            wish_listings.append(listing)
    return render(request, "auctions/wishlists.html", {
        "wish_listings":wish_listings
    })

@login_required(login_url='/login')
def close(request, itemid):
    comm = Addcomment.objects.filter(item=itemid).order_by("time")
    bids = Bid_price.objects.filter(item=itemid)
    bid_count = len(bids)
    user = request.user.username
    listing = Auction_listing.objects.get(id=itemid)
    listing_item = Auction_listing.objects.get(id=itemid)
    highest_price = Bid_price.objects.filter(item=itemid).order_by("-bid_price").first()
    wish = Wish_list.objects.filter(user=request.user.username, item=itemid)
    if user == listing.user:
        close = Closebid()
        close.user = user
        close.item = itemid
        if Bid_price.objects.filter(item=itemid).order_by("-bid_price").first():
            highest_bid = Bid_price.objects.filter(item=itemid).order_by("-bid_price").first()
            close.winner = highest_bid.user
            close.save()
        else:
            close.save()
        closeitem = Closebid.objects.get(item=itemid)
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm
        })
    else:
        closeitem = Closebid.objects.get(item=itemid)
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm
        })


@login_required(login_url='/login')
def add_comment(request, itemid):
    if request.method == "POST":
        user = request.user.username
        comment = request.POST["comment"]
        com = Addcomment()
        com.user = user
        com.item = itemid
        com.comment = comment
        # saving new comment
        com.save()
        comm = Addcomment.objects.filter(item=itemid).order_by("time")
        bids = Bid_price.objects.filter(item=itemid)
        bid_count = len(bids)
        listing_item = Auction_listing.objects.get(id=itemid)
        highest_price = Bid_price.objects.filter(item=itemid).order_by("-bid_price").first()
        wish = Wish_list.objects.filter(user=request.user.username, item=itemid)
        closeitem = Closebid.objects.filter(item=itemid).first()
        min_price = 0
        if highest_price:
            min_price = int(highest_price.bid_price) + 1
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm,
            "min_price":min_price
        })
    else:
        comm = Addcomment.objects.filter(item=itemid).order_by("time")
        bids = Bid_price.objects.filter(item=itemid)
        bid_count = len(bids)
        listing_item = Auction_listing.objects.get(id=itemid)
        highest_price = Bid_price.objects.filter(item=itemid).order_by("-bid_price").first()
        wish = Wish_list.objects.filter(user=request.user.username, item=itemid)
        closeitem = Closebid.objects.filter(item=itemid).first()
        min_price = 0
        if highest_price:
            min_price = int(highest_price.bid_price) + 1
        return render(request, "auctions/listing.html", {
            "item":listing_item,
            "highest_price":highest_price,
            "bid_count":bid_count,
            "wish":wish,
            "closeitem":closeitem,
            "comments":comm,
            "min_price":min_price
        })


def categories(request):
    return render(request, "auctions/categories.html")


def category(request, category):
    ctg_items = Category.objects.filter(category=category)
    items = []
    if ctg_items:
        for ctg_item in ctg_items:
            item = Auction_listing.objects.get(id=ctg_item.item)
            items.append(item)
    return render(request, "auctions/category.html", {
        "items":items,
        "ctg_name":category
    })


def search(request):
    if request.method == "GET":
        q = request.GET.get('q')
        items = []
        if Auction_listing.objects.filter(name__icontains=q):
            listings = Auction_listing.objects.filter(name__icontains=q)
            for listing in listings:
                items.append(listing)
        ctg_listings = Category.objects.filter(category__icontains=q)
        if ctg_listings:
            for ctg_listing in ctg_listings:
                item = Auction_listing.objects.filter(id=ctg_listing.item)
                if item:
                    items.append(item)
        return render(request, "auctions/search_result.html", {
            "search":q,
            "items":items
        })