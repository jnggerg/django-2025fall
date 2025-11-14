from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('workers/', views.workersList, name='workersList'),
    path('workers/<int:worker_id>/', views.workerDetail, name='workerDetail'),
    path('workers/<int:worker_id>/items/', views.workerItems, name='workersItems'),
    path('items/', views.auctionItemsList, name='auctionItemsList'),
    path('items/<int:item_id>/', views.auctionItemDetail, name='auctionItemDetail'),
    path('reviews/', views.reviewsList, name='reviewsList'),
    path('submit_review/', views.FormView.as_view(), name='submit_review'),
]
