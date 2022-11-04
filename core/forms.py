from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    
    class Meta:
        model = Movie
        fields = "__all__"
        exclude = ['reviews', 'rating_average', 'rating_count']
