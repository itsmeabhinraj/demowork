from django.urls import path

from . import views
app_name = 'movies'

urlpatterns = [
    path('movie_list/', views.movie_list, name='movie_list'),
    # above there is null path.but home come so changed it
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_results, name='search_results'),
    path('category/<slug:category>/', views.category_movies, name='category_movies'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('home/', views.home, name='home'),

    path('navbar/', views.navbar, name='navbar'),
    path('navbarnew/', views.navbarnew, name='navbarnew'),

    path('add_movie/', views.add_movie, name='add_movie'),
    path('add_to_wishlist/<int:movie_id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('user_movies/', views.user_movies, name='user_movies'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('admin_movies/', views.admin_movies, name='admin_movies'),

    path('rate_review/<int:review_id>/', views.rate_review, name='rate_review'),
    path('add_review/', views.add_review, name='add_review'),

]
