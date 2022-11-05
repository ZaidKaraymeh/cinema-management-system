from django import forms
from .models import *
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

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(MovieForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['trailer'].required = False
        self.fields['thumbnail'].required = False



class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['slot']

class MovieScheduleForm(forms.ModelForm):
    slots = forms.ChoiceField(label="")

    class Meta:
        model = MovieSchedule
        fields = ['movie', 'slots', 'hall']

        widgets = {
            'hall': forms.Select(attrs={'onchange': 'changeFunc(this.value);'})
        }
    
    def __init__(self, *args, **kwargs):
        super(MovieScheduleForm, self).__init__(*args, **kwargs)
        self.fields['slots'].choices = []

        