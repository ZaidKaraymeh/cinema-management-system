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
    slots = forms.ChoiceField(choices=[], widget=forms.Select())
    class Meta:
        model = Slot
        fields = ['slots']

    def __init__(self, *args, **kwargs):
        super(SlotForm, self).__init__(*args, **kwargs)
        self.fields['slots'].choices = []



class MovieScheduleForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(
        attrs={'onchange': 'changeFunc(this.value);'}))

    class Meta:
        model = MovieSchedule
        fields = ['movie',  'hall', 'date']

        widgets = {
            'hall': forms.Select(attrs={'onchange': 'changeFunc(this.value);'}),
        }
    

        