from django.contrib import admin

from movies.models import Category, Movie, Wishlist


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Category, CategoryAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'added_by')
    list_filter = ('category', 'year')
    search_fields = ('name', 'actors')
    date_hierarchy = 'year'
    list_per_page = 20


admin.site.register(Movie, MovieAdmin)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['name']  # Assuming 'user' is a ForeignKey to User model


admin.site.register(Wishlist, WishlistAdmin)
