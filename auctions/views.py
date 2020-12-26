from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User , Auctions , Biding, Comments, Watchlist
from .forms import AuctionCreationForm , BidingForm, CommentForm


def index(request, category=None):

    if category:
        auction_list_category = Auctions.objects.filter(category = category).order_by('-date_posted')
        return render(request, "auctions/index.html" , {"auction_list": auction_list_category})

    return render(request, "auctions/index.html" , {"auction_list": Auctions.objects.all().order_by('-date_posted')})


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


#views defined my me
# -------------------------------------------------------------------------------

@login_required(login_url='/login/')
def categories(request):
    category = set()
    
    for i in Auctions.objects.all():
            category.add(i.category)


    return render(request, 'auctions/categories.html' , {'category':category})

@login_required(login_url='/login/')
def create_listing(request):
    form = AuctionCreationForm()

    if request.method == 'POST':
        form = AuctionCreationForm(request.POST , request.FILES or None)

        if form.is_valid():
            form_details = form.save(commit=False)
            form_details.author = request.user
            form_details.save()

            return redirect('index')
    
    content = {
        'form' : form
    }

    return render(request , "auctions/create_listing.html" , content)

    

@login_required(login_url='/login/')
def listing(request , pk):
    highest_bid_author = False
    product = Auctions.objects.get(pk = pk)
    
    form_comment = CommentForm(request.POST or None)
    print('good')
    if form_comment.is_valid():
        print("good")
        instance_comment = form_comment.save(commit=False)
        instance_comment.user = request.user
        instance_comment.comment_on = product
        instance_comment.save()
        form_comment.save()

    form_bid = BidingForm()


    highest_bid = Biding.objects.filter(product = product).order_by('-bid').first()
    bid_count = Biding.objects.filter(product = product).count()
    comments = Comments.objects.filter(comment_on = product).order_by('-date_posted')


    content = {
        'Product' : product,
        'Comments': comments,
        'form_comment': form_comment,
        'watchlist': Watchlist.objects.filter(watchlist = product , user = request.user),
        'watchlist_count' : Watchlist.objects.all().count(),
        'form_bid':form_bid,
        'bid_count':bid_count,
        'highest_bid':highest_bid
    }

    return render(request , 'auctions/product.html' , content)


@login_required(login_url='/login/')
def watchlist(request):
    watchlist = Watchlist.objects.filter(user = request.user)

    content = {
        'watchlist' : watchlist
    }

    return render(request , 'auctions/watchlist.html' , content)

@login_required(login_url = '/login/')        
def watchlist_add(request , pk):
    product = Auctions.objects.get(pk = pk)

    watchlist = Watchlist.objects.create(watchlist = product , user = request.user)

    return redirect('listing' , pk)


def bid(request):
    pk = request.POST.get('pk')
    product = Auctions.objects.get(pk = pk)

    if request.method == 'POST':
        form_bid = BidingForm(request.POST)
        print('good')
        if form_bid.is_valid():
            instance_bid = form_bid.save(commit=False)

            if instance_bid.bid < product.price:
                return redirect('listing' , pk)

            else:
                instance_bid.author = request.user
                instance_bid.product = product
                instance_bid.save()
                form_bid.save()

                return redirect('listing' , pk)
            
    return redirect('listing' , pk)

