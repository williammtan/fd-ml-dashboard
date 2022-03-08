from django.views import generic
from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Collection
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView

from .models import ProductCategory
from .forms import CollectionModelForm

class IndexView(generic.ListView):
    template_name = 'collections/index.html'
    model = Collection
    context_object_name = 'collection_list'
    paginate_by = 10
    ordering = ['-created_at']

class DetailView(generic.DetailView):
    model = Collection
    template_name = 'collections/detail.html'


class CollectionCreateView(BSModalCreateView):
    display_name = 'Collection'
    template_name = 'create_modal.html'
    form_class = CollectionModelForm
    success_message = 'Success: Collection was created.'
    success_url = reverse_lazy('collection:index')

class CollectionEditView(BSModalUpdateView):
    model = Collection
    template_name = 'collections/edit.html'
    form_class = CollectionModelForm
    success_message = 'Success: Collection was updated.'
    success_url = reverse_lazy('collection:index')

class CollectionDeleteView(BSModalDeleteView):
    model = Collection
    template_name = 'collections/delete.html'
    success_message = 'Success: Collection was deleted.'
    success_url = reverse_lazy('collection:index')
