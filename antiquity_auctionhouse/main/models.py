from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Worker(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='workers/', null=True, blank=True)
    contacts = models.JSONField(default=dict)  #{"email": ", "phone":"", etc.}

    def __str__(self):
        return self.name

class AuctionItem(models.Model):

    class Types(models.TextChoices):
        PAINTING = 'painting'
        PORCELAIN = 'porcelain'
        JEWELRY = 'jewelry'

    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='auction_items/', null=True, blank=True)
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
            "picture": self.picture.url if self.picture else None,
            "type": self.get_type_display(), 
            "auction_end_time": self.auction_end_time.isoformat()
        }