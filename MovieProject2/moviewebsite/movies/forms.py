from django import forms
from .models import Movie, Category, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'desc', 'year', 'img', 'actors', 'category', 'trailer_link']


class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Review
        fields = ['rating', 'comment']


class MovieAdminForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    CATEGORY_CHOICES = [
        ('ACTION', 'Action'),
        ('ROMANCE', 'Romance'),
        ('COMEDY', 'Comedy'),
        ('KIDS', 'Kids'),
        ('THRILLERS', 'Thriller'),
        ('HORRORS', 'Horror'),
    ]

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'select2'}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the 'user' parameter from kwargs
        super(MovieAdminForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['added_by'].initial = user.username  # Set the initial value for 'added_by' field
            self.fields['added_by'].widget.attrs['readonly'] = True  # Make 'added_by' field read-only