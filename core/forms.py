from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget


class DateInput(forms.DateInput):
    input_type = 'date'


class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Movie
        fields = ["title", "release_date", "description", "genres", "trailer", "thumbnail"]
        exclude = ['reviews', 'rating_average', 'rating_count']
        
        widgets = {
            'release_date': DateInput(),
        }    

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(MovieForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['trailer'].required = False
        # style the fields
        self.fields['title'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['release_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['description'].widget.attrs['style'] = 'width:100%; height:250px;'
        self.fields['genres'].widget.attrs['style'] = 'background-color: #CCC5C5; border: 1px solid #CCC5C5;'
        self.fields['trailer'].widget.attrs['style'] = 'width:100%; height:50px; background-color: #CCC5C5!important;'
        self.fields['thumbnail'].widget.attrs['style'] = 'width:100%; height:50px; background-color: #CCC5C5!important;'

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['release_date'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        #self.fields['genres'].widget.attrs['class'] = 'form-check'
        self.fields['trailer'].widget.attrs['class'] = 'form-control'
        self.fields['thumbnail'].widget.attrs['class'] = 'form-control'




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
    
    # def __init__(self, *args, **kwargs):
    #     super(MovieScheduleForm, self).__init__(*args, **kwargs)
    #     self.fields['movie'].widget.attrs['style'] = 'width:100%; height:60px;'
    #     self.fields['hall'].widget.attrs['style'] = 'width:100%; height:60px;'
    #     self.fields['date'].widget.attrs['style'] = 'width:100%; height:60px;'
    #     self.fields['movie'].widget.attrs['class'] = 'form-select'
    #     self.fields['hall'].widget.attrs['class'] = 'form-select'
    #     self.fields['date'].widget.attrs['class'] = 'form-select'
    

class HallForm(forms.ModelForm):

    class Meta:
        model = Hall
        fields = ['name']


class ExportForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    choices = forms.ChoiceField(widget=forms.Select())

    def __init__(self, choices=[], *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['end_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['start_date'].widget.attrs['class'] = 'form-control'
        self.fields['end_date'].widget.attrs['class'] = 'form-control'
        self.fields['choices'].choices = choices


class MovieStatusForm(forms.Form):
    status = forms.ChoiceField(widget=forms.Select(), choices=[(
        'Archived', 'Archived'), ('Running', 'Running'), ('Upcoming', 'Upcoming')])

    
    def __init__(self, *args, **kwargs):
        super(MovieStatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['style'] = 'width:100%; height:50px;'
        self.fields['status'].widget.attrs['class'] = 'form-select'
