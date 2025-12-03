from django.urls import path
from .views import auth_views, main_views, management_views

urlpatterns = [
    path('', main_views.home, name='home'),
    path('workers/', main_views.workersList, name='workersList'),
    path('workers/<int:worker_id>/', main_views.workerDetail, name='workerDetail'),
    path('workers/<int:worker_id>/items/', main_views.workerItems, name='workersItems'),
    path('items/', main_views.auctionItemsList, name='auctionItemsList'),
    path('reviews/', main_views.reviewsList, name='reviewsList'),
    path('submit_review/', main_views.FormView.as_view(), name='submit_review'),
    path('register/', auth_views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logoutView, name='logout'),
    path('my-bids/', auth_views.my_bids, name='my_bids'),
    path('open-bidding/<int:item_id>/', auth_views.openBidding, name='openBidding'),
    path('close-bidding/<int:item_id>/', auth_views.closeBidding, name='closeBidding'),
    path('place-bid/<int:item_id>/', auth_views.placeBid, name='placeBid'),
    path('management/workers/', management_views.ManagementWorkersList.as_view(), name='ManagementWorkersList'),
    path('management/workers/<int:worker_id>/', management_views.ManagementWorkerUpdate.as_view(), name='ManagementWorkerUpdate'),
    path('management/workers/<int:worker_id>/delete/', management_views.ManagementWorkerDelete.as_view(), name='ManagementWorkerDelete'),
    path('management/items/<int:item_id>/' , management_views.ManagementAuctionItemUpdate.as_view(), name='ManagementAuctionItemUpdate'),
    path('management/items/<int:item_id>/delete' , management_views.ManagementAuctionItemDelete.as_view(), name='ManagementAuctionItemDelete'),
]