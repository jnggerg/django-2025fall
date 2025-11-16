from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('workers/', views.workersList, name='workersList'),
    path('workers/<int:worker_id>/', views.workerDetail, name='workerDetail'),
    path('workers/<int:worker_id>/items/', views.workerItems, name='workersItems'),
    path('items/', views.auctionItemsList, name='auctionItemsList'),
    path('reviews/', views.reviewsList, name='reviewsList'),
    path('submit_review/', views.FormView.as_view(), name='submit_review'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('my-bids/', views.my_bids, name='my_bids'),
    path('open-bidding/<int:item_id>/', views.openBidding, name='openBidding'),
    path('close-bidding/<int:item_id>/', views.closeBidding, name='closeBidding'),
    path('place-bid/<int:item_id>/', views.placeBid, name='placeBid'),
]
