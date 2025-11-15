from django.shortcuts import render
from django.views import View
from .models import AuctionItem, Review, Worker
from .forms import ReviewForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.

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
    items = AuctionItem.objects.all()
    context = {
        'items': items
    }
    return render(request, 'auction_items/auction_items_list.html', context)

def auctionItemDetail(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    context = {
        'item': item
    }
    return render(request, 'auction_items/auction_item.html', context)

def reviewsList(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/reviews.html', context)


class FormView(View):
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
        form = UserCreationForm()
        return render(request, 'main/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect("home")

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'main/login.html', {'form': form})

    def post(self, request):
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