from django.shortcuts import render, redirect
from main.decorators import ManagementRequiredMixin
from django.contrib import messages
from django.views import View
from main.models import Worker, AuctionItem, Review, Bid

class ManagementWorkersList(ManagementRequiredMixin, View):    
    def get(self, request):
        workers = Worker.objects.all()
        context = {
            'workers': workers
        }
        return render(request, 'management/workers.html',context)

class ManagementWorkerUpdate(ManagementRequiredMixin, View): 
    def post(self, request, worker_id):
        worker = Worker.objects.get(id=worker_id)
        worker.name = request.POST.get('name', worker.name)
        worker.introduction = request.POST.get('introduction', worker.introduction)
        worker.picture = request.POST.get('picture', worker.picture)
        contacts_raw = request.POST.get('contacts', '')
        contacts_list = [contact.strip() for contact in contacts_raw.split(',') if contact.strip()]
        worker.contacts = {"contacts": contacts_list}
        worker.save()
        messages.success(request, 'Worker details updated successfully.')
        return redirect('ManagementWorkersList')

class ManagementWorkerDelete(ManagementRequiredMixin, View):
    def post(self, request, worker_id):
        worker = Worker.objects.get(id=worker_id)
        worker.delete()
        messages.success(request, 'Worker deleted successfully.')
        return redirect('ManagementWorkersList')

class ManagementAuctionItemUpdate(ManagementRequiredMixin, View):
    def post(self, request, item_id):
        item = AuctionItem.objects.get(id=item_id)
        item.name = request.POST.get('name', item.name)
        item.starting_bid = request.POST.get('starting_bid', item.starting_bid)
        item.auction_end_time = request.POST.get('auction_end_time', item.auction_end_time)
        item.save()
        messages.success(request, 'Auction item details updated successfully.')
        return redirect('auctionItemsList')
    
class ManagementAuctionItemDelete(ManagementRequiredMixin, View):
    def post(self, request, item_id):
        item = AuctionItem.objects.get(id=item_id)
        item.delete()
        messages.success(request, 'Auction item deleted successfully.')
        return redirect('auctionItemsList')