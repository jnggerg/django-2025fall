from django.shortcuts import render
from django.views import View
from .models import AuctionItem, Review, Worker, Bid
from .forms import ReviewForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import group_required
from django.contrib import messages

def home(request):
    return render(request, 'main/home.html')

def workersList(request):
    workers = Worker.objects.all()
    context = {
        'workers': workers
    }
    return render(request, 'workers/workers_list.html', context)

def workerDetail(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    context = {
        'worker': worker,
    }
    return render(request, 'workers/worker.html', context)

#seperate page for all items of a worker
def workerItems(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    items = worker.auction_items.all()
    context = {
        'worker': worker,
        'items': items
    }
    return render(request, 'workers/worker_items.html', context)

def auctionItemsList(request):
    items = AuctionItem.objects.all().order_by('-is_active', 'name')
    paginator = Paginator(items, 10)

    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    context = {
        'items': items
    }
    return render(request, 'auction_items/auction_items_list.html', context)


def reviewsList(request):
    reviews_list = Review.objects.all().order_by('-submitted_at')
    paginator = Paginator(reviews_list, 10)  
    
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/reviews.html', context)


class FormView(LoginRequiredMixin, View):
    login_url = '/login/'  # prompted to login if not authenticated
    
    def get(self, request):
        form = ReviewForm()
        return render (request, 'reviews/submit_review.html', {'form': form})

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviewsList')
        return render(request, 'main/submit_review.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated: # redirected to main menu if already logged in
            return redirect('home')
        
        form = UserCreationForm()
        return render(request, 'main/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("home")
        
        # if form is not valid, rerender with errors
        return render(request, 'main/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = AuthenticationForm()
        return render(request, 'main/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'main/login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('home')

@login_required
def my_bids(request):
    user_bids = request.user.bids.all().order_by('auction_item', '-amount')
    
    # checking if user has placed higher bids on same items
    bids_with_status = []
    for bid in user_bids:
        highest_user_bid = request.user.bids.filter(
            auction_item=bid.auction_item
        ).order_by('-amount').first()
        
        bid.has_higher_bid = (highest_user_bid and highest_user_bid.amount > bid.amount)
        bids_with_status.append(bid)

    context = {
        'bids': bids_with_status
    }
    return render(request, 'auction_items/my_bids.html', context)

@group_required('Auctioneers')
def openBidding(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    item.is_active = True
    item.save()
    return redirect('auctionItemsList')  

@group_required('Auctioneers')
def closeBidding(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    item.is_active = False
    if item.get_highest_bid() is not None:
        item.sold = True
    item.save()
    return redirect('auctionItemsList')  

@login_required
def placeBid(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    
    # since users can place bids from /items aswell as from /my-bids
    referer = request.META.get('HTTP_REFERER', '')
    
    if request.method == 'POST':
        bid_amount = int(request.POST.get('bid_amount'))
        current_price = item.get_current_price()

        if bid_amount > current_price:
            new_bid = Bid(auction_item=item, user=request.user, amount=bid_amount)
            new_bid.full_clean()  #validation
            new_bid.save()
            
            messages.success(request, "Siker! Mostantól ön a legmagasabb licitáló.")
            
            # redirect back to where the user came from
            if 'my-bids' in referer:
                return redirect('my_bids')
            else:
                return redirect('auctionItemsList')
        else:
            messages.error(request, "A licitjének magasabbnak kell lennie a jelenlegi árnál.")
            
            # redirect back to where the user came from
            if 'my-bids' in referer:
                return redirect('my_bids')
            else:
                return redirect('auctionItemsList')
    
    # get redirects back to itemlist
    return redirect('auctionItemsList')
