from django.shortcuts import render
from .models import AuctionItem, Worker

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def workersList(request):
    workers = Worker.objects.all()
    context = {
        'workers': workers
    }
    return render(request, 'main/workers_list.html', context)

def workerDetail(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    context = {
        'worker': worker,
    }
    return render(request, 'main/worker.html', context)

#seperate page for all items of a worker
def workerItems(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    items = worker.auction_items.all()
    context = {
        'worker': worker,
        'items': items
    }
    return render(request, 'main/worker_items.html', context)

def auctionItemsList(request):
    items = AuctionItem.objects.all()
    context = {
        'items': items
    }
    return render(request, 'main/auction_items_list.html', context)

def auctionItemDetail(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    context = {
        'item': item
    }
    return render(request, 'main/auction_item.html', context)