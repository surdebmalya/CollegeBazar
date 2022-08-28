from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('accountCreation', views.accountCreation, name="accountCreation"),
    path('logout', views.logout, name="logout"),
    path('logIntoAccount', views.logIntoAccount, name="logIntoAccount"),
    path('categories', views.categories, name="categories"),
    path('sell', views.sell, name="sell"),
    path('createProduct', views.createProduct, name="createProduct"),
    path('getDetails', views.getDetails, name="getDetails"),
    path('categoryProducts', views.categoryProducts, name="categoryProducts"),
    path('filter', views.filter, name="filter"),
    path('addToWishlist', views.addToWishlist, name="addToWishlist"),
    path('wishlists', views.wishlists, name="wishlists"),
    path('search', views.search, name="search"),
    path('chat', views.chat, name="chat"),
    path('allChats', views.allChats, name="allChats"),
    path('<str:room>/', views.room, name='room'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('send', views.send, name='send'),
    path('resumeChatting', views.resumeChatting, name="resumeChatting"),
    path('myProducts', views.myProducts, name="myProducts"),
]