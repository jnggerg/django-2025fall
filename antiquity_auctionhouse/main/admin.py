from django.contrib import admin
from .models import Worker, AuctionItem, Review

admin.site.register(Worker)
admin.site.register(AuctionItem)
admin.site.register(Review)