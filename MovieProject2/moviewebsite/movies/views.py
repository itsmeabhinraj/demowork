from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import MovieAdminForm, MovieForm
from .models import Movie, Wishlist, Category, Review


def movie_list(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    latest_Movies = Movie.objects.all().order_by('-id')[:10]  # Adjust as needed

    return render(request, 'movie_list.html', {'movies': movies, 'latest_Movies': latest_Movies, 'categories': categories})


def search_results(request):
    query = request.GET.get('query')
    movies = Movie.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'movies': movies})


@login_required
# def movie_detail(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#
#     # Check if the current user is the one who added the movie
#     if request.user == movie.added_by:
#         if request.method == 'POST':
#             form = MovieAdminForm(request.POST, instance=movie)
#             if form.is_valid():
#                 form.save()
#             # Handle movie update or deletion here
#             # Example:
#             movie.name = request.POST['name']
#             movie.desc = request.POST['desc']
#             movie.save()
#             # Redirect to movie detail page or movie list after update/deletion
#             return redirect('movies:movie_detail', movie_id=movie.id)
#         else:
#              return render(request, 'movie_detail.html', {'movie': movie})
#     else:
#         # User is not allowed to modify this movie
#         return redirect('movies:movie_detail', movie_id=movie.id)  # Or show an error page
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)  # Fetching the first book
    return render(request, 'movie_detail.html', {'movie': movie})


@login_required
# def add_movie(request):
#     if request.method == 'POST':
#         form = MovieAdminForm(request.POST, request.FILES)
#         if form.is_valid():
#             movie = form.save(commit=False)
#             movie.added_by = request.user  # Set the user who added the movie
#             movie.save()
#             return redirect('movies:movie_list')
#     else:
#         form = MovieAdminForm()
#     return render(request, 'add_movie.html', {'form': form})

def add_movie(request):
    if request.method == 'POST':
        form = MovieAdminForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user  # Set the user who added the movie
            movie.save()
            return redirect('movies:movie_list')
    else:
        form = MovieAdminForm(user=request.user)
    return render(request, 'add_movie.html', {'form': form})
#                            category
def category_movies(request, category):
    category_name = category.replace('-', ' ')  # Convert URL slug back to category name

    # category_object = get_object_or_404(Category, name=category_movies)
    category_object = get_object_or_404(Category, name__iexact=category_name)
    movies = Movie.objects.filter(category=category_object)
    return render(request, 'category_movies.html', {'category': category_object, 'movies': movies})


def home(request):
    latest_Movies = Movie.objects.all().order_by('-id')[:10]  # Adjust as needed
    return render(request, 'home.html', {'latest_Movies': latest_Movies})


def navbar(request):
    categories = Category.objects.all()
    return render(request, 'navbar.html', {'categories': categories})


def navbarnew(request):
    categories = Category.objects.all()
    return render(request, 'navbarnew.html', {'categories': categories})


@csrf_exempt
@login_required
def add_to_wishlist(request, movie_id):
    if request.method == 'POST':
        movie_id = request.POST.get('movieId')
        movie = get_object_or_404(Movie, pk=movie_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.movies.add(movie)
        return JsonResponse({'message': 'Movie added to wishlist!'})
    else:
        return JsonResponse({'error': 'This method is not allowed'}, status=405)


@login_required
def view_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})


@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Check if the logged-in user is the one who added the movie
    if request.user == movie.added_by:
        if request.method == 'POST':
            movie.delete()
            return redirect('movies:movie_list')
        else:
            return render(request, 'confirm_delete.html', {'movie': movie})
    else:
        # If the logged-in user is not the movie's creator, return forbidden response
        return HttpResponseForbidden("You are not allowed to delete this movie.")

@login_required
def user_movies(request):
    # Retrieve movies added by the current logged-in user
    movies = Movie.objects.filter(added_by=request.user)
    return render(request, 'user_movies.html', {'movies': movies})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, added_by=request.user)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_movie.html', {'form': form})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, added_by=request.user)

    if request.method == 'POST':
        movie.delete()
        return redirect('movies:user_movies')

    return render(request, 'delete_movie.html', {'movie': movie})

@staff_member_required
def admin_movies(request):
    # Retrieve all movies for admin view
    movies = Movie.objects.all()
    return render(request, 'admin_movies.html', {'movies': movies})

@csrf_exempt
@login_required
def rate_review(request, review_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = get_object_or_404(Review, pk=review_id)

        # Update the rating of the review
        review.rating = rating
        review.save()

        # Prepare data to send back as JSON response
        data = {
            'rating': review.rating,
            'comment': review.comment,
            # Add other relevant review data if needed
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def add_review(request):
    if request.method == 'POST' and request.is_ajax():
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        movie_id = request.POST.get('movie_id')  # Retrieve movie ID from frontend

        movie = get_object_or_404(Movie, pk=movie_id)

        # Create a new review object
        new_review = Review.objects.create(movie=movie, user=request.user, rating=rating, comment=comment)

        # Return the newly created review data as JSON response
        return JsonResponse({
            'rating': new_review.rating,
            'comment': new_review.comment
        })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)