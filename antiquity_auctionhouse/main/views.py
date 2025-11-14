from django.shortcuts import render
from django.views import View
from .models import AuctionItem, Review, Worker
from .forms import ReviewForm
from django.shortcuts import redirect

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