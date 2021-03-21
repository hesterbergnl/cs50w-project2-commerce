from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing
from django.db.models import Max
from .models import User


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
            "listings":listings
        }) 

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = listing.comments.all()
    #select the highest bid, get the correct value from dictionary
    bid = listing.bids.all().aggregate(Max('bid')).get('bid__max')
    #If no highest bid, set 0 to use the starting price
    if(bid == None):
        bid = 0
    return render(request, "auctions/listing.html", {
            "listing":listing,
            "comments":comments,
            "bid":bid
        })

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
