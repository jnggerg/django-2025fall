from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from main.models import AuctionItem, Bid
from main.decorators import group_required

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

@group_required('Management')
def openBidding(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    item.is_active = True
    item.save()
    return redirect('auctionItemsList')  

@group_required('Management')
def closeBidding(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    item.is_active = False
    if item.get_highest_bid() is not None:
        item.sold = True
        messages.info(request, f"A '{item.name}' aukciója lezárult. A tárgy eladva a legmagasabb licitáló részére: {item.get_highest_bid().user.username}.")
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