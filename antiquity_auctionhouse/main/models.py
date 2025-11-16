from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Worker(models.Model):
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=200, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    contacts = models.JSONField(default=dict)  #{"email": ", "phone":"", "facebook": "",etc.}

    def __str__(self):
        return self.name

class AuctionItem(models.Model):
    class Types(models.TextChoices):
        PAINTING = 'painting'
        PORCELAIN = 'porcelain'
        JEWELRY = 'jewelry'

    name = models.CharField(max_length=200)
    picture = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(choices=Types.choices)
    starting_bid = models.IntegerField()
    is_active = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    auction_end_time = models.DateTimeField()
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='auction_items')

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.auction_end_time <= timezone.now():
            raise ValidationError('Auction end time must be in the future.')
        

    # returns highest bid object, or None
    def get_highest_bid(self):
        return self.bids.order_by('-amount').first()
    
     # returns highest bid amount, or starting price
    def get_current_price(self):
        highest_bid = self.get_highest_bid()
        if highest_bid:
            return highest_bid.amount
        return self.starting_bid
    
    def get_highest_bidder(self):
        highest_bid = self.get_highest_bid()
        if highest_bid:
            return highest_bid.user
        return None
    
    
class Review(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def clean(self): 
        if not (1 <= self.rating <= 5):
            raise ValidationError('Rating must be between 1 and 5.')
        # no need to check anything else, since worker gets picked from list, comment can be null
        # and submitted_at is auto_now_add

    def __str__(self):
        return f'Review for {self.worker.name} - Rating: {self.rating}'


class Bid(models.Model):
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bids')
    amount = models.IntegerField()
    bid_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount', '-bid_time']  # Highest bid first, then most recent

    def clean(self):
        if self.amount <= self.auction_item.starting_bid:
            raise ValidationError('Bid amount must be higher than the starting bid.')
        
        current_highest = self.auction_item.get_highest_bid()
        if current_highest and self.amount <= current_highest.amount:
            raise ValidationError(f'Bid amount must be higher than the current highest bid of {current_highest.amount}.')
        
        if self.auction_item.auction_end_time < timezone.now() or not self.auction_item.is_active:
            raise ValidationError('This auction is no longer active.')

    def __str__(self):
        return f'Bid of {self.amount} by {self.user.username} on {self.auction_item.name}'