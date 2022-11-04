from django import forms
from .models import Movie
from django.contrib.admin.widgets import AdminDateWidget


class DateInput(forms.DateInput):
    input_type = 'date'

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["name", "release_date", "description", "genres", "trailer", "thumbnail"]
        exclude = ['reviews', 'rating_average', 'rating_count']

        widgets = {
            'release_date': DateInput()
        }
