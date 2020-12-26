from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("categories/<str:category>", views.index, name='index'),
    path("categories/", views.categories, name='categories'),

    path("listing/<int:pk>", views.listing, name='listing'),
    path("new-listing/", views.create_listing, name = 'create_listing'),
    path("watchlist/add/<int:pk>", views.watchlist_add, name = 'watchlist_add'),
    path('watchlist/', views.watchlist, name = 'watchlist'),
    path('listing/bid/', views.bid , name = 'bid')
    
]
