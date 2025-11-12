from django.core.management.base import BaseCommand
from main.models import Worker, AuctionItem
from django.utils import timezone
from faker import Faker
import random
from .imageseed import get_themed_images

# using Faker to seed random data into database models
# for image urls, picsum.photos is used with seeds for consistency

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # "drop" tables
        AuctionItem.objects.all().delete()
        Worker.objects.all().delete()

        # 10 fake workers with external picture URLs
        worker_images = get_themed_images("portrait", 10)  
        workers = []
        for i in range(10):
            worker = Worker.objects.create(
                name=fake.name(),
                picture=worker_images[i],
                contacts={"email": fake.email(), "phone": fake.phone_number()}
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
            AuctionItem.Types.PAINTING: get_themed_images("painting", 10),
            AuctionItem.Types.PORCELAIN: get_themed_images("porcelain", 10),
            AuctionItem.Types.JEWELRY: get_themed_images("jewelry", 10),
        }

        # 3 fake items for each worker (30 total)
        for worker in workers:
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

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with 10 workers and 30 auction items!'))