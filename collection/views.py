from django.views import generic
from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Collection

class IndexView(generic.ListView):
    template_name = 'collections/index.html'
    model = Collection
    context_object_name = 'collection_list'
    paginate_by = 10
    ordering = ['-created_at']

class DetailView(generic.DetailView):
    model = Collection
    template_name = 'collections/detail.html'


class CollectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if type(field) == forms.ModelMultipleChoiceField:
                field.widget.attrs = {
                'class': 'selectpicker',
                'id': field.label.lower(),
                'data-size': 10,
                'data-width': 'fit'
                }
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'id': field.label.lower()
                }

    class Meta:
        fields = ('name', 'description', 'categories') 
        model = Collection


class CreateView(generic.edit.CreateView):
    model = Collection
    template_name = 'collections/create.html'
    form_class = CollectionForm

    def get_success_url(self):
        return reverse_lazy('collection:detail', kwargs={'pk': self.object.id})

