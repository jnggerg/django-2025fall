from django.core.management.base import BaseCommand
from main.models import Worker, AuctionItem
from django.utils import timezone
from faker import Faker
import random
from .imageseed import get_themed_images

# using Faker to seed random data into database models
# for image urls, i am using pexels API with items types as themes, the API call is in imageseed.p


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker("hu_HU")

        # "drop" tables
        AuctionItem.objects.all().delete()
        Worker.objects.all().delete()

        # 10 fake workers with external picture URLs
        worker_images = get_themed_images("portrait", 10, "medium")  
        workers = []
        for i in range(10):
            worker = Worker.objects.create(
                name=fake.name(),
                picture=worker_images[i],
                roles = random.choice([Worker.Roles.NORMAL, Worker.Roles.AUCTIONEER]),
                contacts={"email": fake.email(), "phone": fake.msisdn(), "facebook": "https://facebook.com", "linkedin": "https://linkedin.com"}
            )
            workers.append(worker)
            self.stdout.write(f'Created worker: {worker.name}')

        # for keeping track of how many items of each type have been created
        chosen_types = {
            AuctionItem.Types.PAINTING: 0,
            AuctionItem.Types.PORCELAIN: 0,
            AuctionItem.Types.JEWELRY: 0,
        }

        images = {
            AuctionItem.Types.PAINTING: get_themed_images("painting", 10,"medium"),
            AuctionItem.Types.PORCELAIN: get_themed_images("porcelain", 10,"medium"),
            AuctionItem.Types.JEWELRY: get_themed_images("jewelry", 10,"medium"),
        }

        # 3 fake items for each worker (30 total)
        for worker in workers:
            #items
            for _ in range(3):
                item_type = random.choice([t for t in images.keys() if chosen_types[t] < 10])
                
                AuctionItem.objects.create(
                    name=fake.word().capitalize() + " " + fake.word(),  
                    type=item_type,
                    starting_bid=random.randint(100, 10000),
                    auction_end_time=fake.future_datetime(end_date='+30d', tzinfo=timezone.get_current_timezone()),
                    worker=worker,
                    picture=images[item_type][chosen_types[item_type]]
                )
                chosen_types[item_type] += 1
            
            # 2 reviews for every worker
            from main.models import Review
            for _ in range(2):
                Review.objects.create(
                    worker=worker,
                    rating=random.randint(1, 5),
                    comment=fake.sentence()
                )
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded database with 10 workers and 30 auction items!'))