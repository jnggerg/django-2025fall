from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from main.models import Worker, AuctionItem, Review, Bid

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.worker = Worker.objects.create(
            name='Test Worker',
            introduction='Test intro',
            contacts={'email': 'test@example.com'}
        )
        self.auction_item = AuctionItem.objects.create(
            name='Test Item',
            type=AuctionItem.Types.PAINTING,
            starting_bid=1000,
            auction_end_time=timezone.now() + timedelta(days=1),
            worker=self.worker,
            is_active=True  
        )
    
    def test_item_creation(self):
        self.assertEqual(self.auction_item.name, 'Test Item')
        self.assertEqual(self.auction_item.starting_bid, 1000)
        self.assertTrue(self.auction_item.is_active) 
    
    def test_get_current_price_nobids(self):
        self.assertEqual(self.auction_item.get_current_price(), 1000)
    
    def test_get_current_price_bids(self):
        Bid.objects.create(auction_item=self.auction_item, user=self.user, amount=1500)
        self.assertEqual(self.auction_item.get_current_price(), 1500)

    def test_get_highest_bidder(self):
        Bid.objects.create(auction_item=self.auction_item, user=self.user, amount=1500)
        self.assertEqual(self.auction_item.get_highest_bidder(), self.user)

    def test_get_highest_bidder_no_bids(self):
        self.assertIsNone(self.auction_item.get_highest_bidder())

    def test_get_minimum_next_bid(self):
        self.assertEqual(self.auction_item.get_current_price() + 1, 1001)
        Bid.objects.create(auction_item=self.auction_item, user=self.user, amount=1500)
        self.assertEqual(self.auction_item.get_current_price() + 1, 1501)
    
    def test_review_creation(self):
        """Test creating a review"""
        review = Review.objects.create(
            worker=self.worker,
            rating=5,
            comment='Great service!'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.worker, self.worker)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.auctioneer_group = Group.objects.create(name='Auctioneers')
        self.auctioneer = User.objects.create_user(username='auctioneer', password='testpass123')
        self.auctioneer.groups.add(self.auctioneer_group)
        
        self.worker = Worker.objects.create(
            name='Test Worker',
            introduction='Test intro',
            contacts={'email': 'test@example.com'}
        )
        self.auction_item = AuctionItem.objects.create(
            name='Test Item',
            type=AuctionItem.Types.PAINTING,
            starting_bid=1000,
            auction_end_time=timezone.now() + timedelta(days=1),
            worker=self.worker,
            is_active=True  
        )
    
    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_worker_list(self):
        response = self.client.get(reverse('workersList'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Worker')
    
    def test_item_list(self):
        response = self.client.get(reverse('auctionItemsList'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
    
    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
        self.assertEqual(response.status_code, 302) 
    
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  
    
    def test_my_bids_protected(self):
        response = self.client.get(reverse('my_bids'))
        self.assertEqual(response.status_code, 302)  
        self.assertIn('/login/', response.url)
    
    def test_my_bids_success(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_bids'))
        self.assertEqual(response.status_code, 200)
    
    def test_place_bid_protected(self):
        response = self.client.post(reverse('placeBid', args=[self.auction_item.id]), {
            'bid_amount': 1500
        })
        self.assertEqual(response.status_code, 302)  
    
    def test_place_bid_success(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('placeBid', args=[self.auction_item.id]), {
            'bid_amount': 1500
        })
        self.assertEqual(Bid.objects.filter(user=self.user, auction_item=self.auction_item).count(), 1)
        self.assertEqual(response.status_code, 302) 
    
    def test_place_bid_error(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('placeBid', args=[self.auction_item.id]), {
            'bid_amount': 500  #lower than starting price
        })
        self.assertEqual(Bid.objects.filter(user=self.user).count(), 0)
    
    def test_open_bid_protected(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('openBidding', args=[self.auction_item.id]))
        self.assertEqual(response.status_code, 302)  
    
    def test_open_bid_success(self):
        self.client.login(username='auctioneer', password='testpass123')
        response = self.client.post(reverse('openBidding', args=[self.auction_item.id]))
        self.assertEqual(response.status_code, 302)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.auctioneer_group = Group.objects.create(name='Auctioneers')

    def test_register_redirect(self):
        #user gets redirected from /register if already logged in
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.url)
    
    def test_open_bidding_protected(self):
        self.client.login(username='testuser', password='testpass123')
        worker = Worker.objects.create(name='Test', introduction='Test', contacts={})
        item = AuctionItem.objects.create(
            name='Test',
            type=AuctionItem.Types.PAINTING,
            starting_bid=1000,
            auction_end_time=timezone.now() + timedelta(days=1),
            worker=worker
        )
        response = self.client.post(reverse('openBidding', args=[item.id]))
        self.assertEqual(response.status_code, 302)  # redirected since no group perm


class BiddingLogicTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.worker = Worker.objects.create(
            name='Test Worker',
            introduction='Test',
            contacts={}
        )
        self.auction_item = AuctionItem.objects.create(
            name='Test Item',
            type=AuctionItem.Types.PAINTING,
            starting_bid=1000,
            auction_end_time=timezone.now() + timedelta(days=1),
            worker=self.worker,
            is_active=True
        )
    
    def test_multiple_bids(self):  #from same user
        Bid.objects.create(auction_item=self.auction_item, user=self.user1, amount=1100)
        Bid.objects.create(auction_item=self.auction_item, user=self.user1, amount=1200)
        self.assertEqual(Bid.objects.filter(user=self.user1).count(), 2)
    
    def test_highest_bids_change(self): #mutliple bids from diff users
        Bid.objects.create(auction_item=self.auction_item, user=self.user1, amount=1100)
        Bid.objects.create(auction_item=self.auction_item, user=self.user2, amount=1500)
        Bid.objects.create(auction_item=self.auction_item, user=self.user1, amount=1300)
        
        self.assertEqual(self.auction_item.get_current_price(), 1500)
        self.assertEqual(self.auction_item.get_highest_bidder(), self.user2)
    
    def test_outbid_itself(self): #user places a higher bid than hes previous one
        bid1 = Bid.objects.create(auction_item=self.auction_item, user=self.user1, amount=1100)
        bid2 = Bid.objects.create(auction_item=self.auction_item, user=self.user1, amount=1500)
        
        #simulate view return to check
        highest_user_bid = Bid.objects.filter(
            auction_item=self.auction_item, 
            user=self.user1
        ).order_by('-amount').first()
        
        self.assertTrue(highest_user_bid.amount > bid1.amount)
        self.assertEqual(highest_user_bid, bid2)
