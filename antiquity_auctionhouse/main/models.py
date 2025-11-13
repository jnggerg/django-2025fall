from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Worker(models.Model):
    class Roles(models.TextChoices):
        NORMAL = 'normal'
        AUCTIONEER = 'auctioneer'

    name = models.CharField(max_length=100)
    roles = models.CharField(choices=Roles.choices, default=Roles.NORMAL)
    picture = models.CharField(max_length=200, blank=True, null=True)
    contacts = models.JSONField(default=dict)  #{"email": ", "phone":"", "facebook": "",etc.}

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            "name": self.name,
            "roles": self.get_roles_display(),
            "picture": self.picture if self.picture else None,
            "contacts": self.contacts
        }

class AuctionItem(models.Model):
    class Types(models.TextChoices):
        PAINTING = 'painting'
        PORCELAIN = 'porcelain'
        JEWELRY = 'jewelry'

    name = models.CharField(max_length=200)
    picture = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(choices=Types.choices)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    auction_end_time = models.DateTimeField()
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='auction_items')

    def __str__(self):
        return self.name 
    
    def to_dict(self):
        return {
            "name": self.name,
            "starting_bid": str(self.starting_bid),
            "picture": self.picture if self.picture else None,
            "type": self.get_type_display(), 
            "worker": self.worker.name,
            "auction_end_time": self.auction_end_time.isoformat()
        }
    
class Review(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError('Rating must be between 1 and 5.')

    def __str__(self):
        return f'Review for {self.worker.name} - Rating: {self.rating}'
    
class Bid(models.Model):
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.IntegerField()
    bid_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.amount <= self.auction_item.starting_bid:
            raise ValidationError('Bid amount must be higher than the starting bid.')

    def __str__(self):
        return f'Bid of {self.amount} by {self.bidder_name} on {self.auction_item.name}'