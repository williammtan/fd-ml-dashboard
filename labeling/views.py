from django.shortcuts import render
from django.views import generic
from django import forms
from django.urls import reverse_lazy
from collection.models import Collection
from .models import Dataset
from django.forms.models import model_to_dict

class IndexView(generic.ListView):
    template_name = 'dataset/index.html'
    context_object_name = 'dataset_list'
    paginate_by = 10

    def get_queryset(self):
        return Dataset.objects.filter(session=0).order_by('-created')

class DetailView(generic.DetailView):
    model = Dataset
    template_name = 'dataset/detail.html'

class DatasetForm(forms.ModelForm):
    collection = forms.ModelChoiceField(Collection.objects.all())

    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label is not None:
                field.widget.attrs = {
                    'class': 'form-control',
                    'id': field.label.lower()
                }
    
    def clean_collection(self):
        self.cleaned_data['collection'] = self.cleaned_data.get('collection').id
        collection = self.cleaned_data.get('collection', False)
        return collection


    class Meta:
        fields = ('name', 'mode', 'collection') 
        model = Dataset


class CreateView(generic.edit.CreateView):
    model = Dataset
    template_name = 'dataset/create.html'
    form_class = DatasetForm

    def get_success_url(self):
        return reverse_lazy('labeling:detail', kwargs={'pk': self.object.id})

    
