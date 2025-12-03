from django.shortcuts import render
from django.views import View
from main.models import AuctionItem, Review, Worker
from main.forms import ReviewForm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


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


