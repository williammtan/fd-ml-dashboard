from django.shortcuts import render
from django.views import generic
from django import forms
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from collection.models import Collection, Product
from .models import Dataset
from django.forms.models import model_to_dict
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from .forms import DatasetModelForm

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


class DatasetCreateView(BSModalCreateView):
    display_name = 'Dataset'
    template_name = 'create_modal.html'
    form_class = DatasetModelForm
    success_message = 'Success: Dataset was created.'
    success_url = reverse_lazy('labeling:index')

class DatasetEditView(BSModalUpdateView):
    model = Dataset
    template_name = 'dataset/edit.html'
    form_class = DatasetModelForm
    success_message = 'Success: Dataset was updated.'
    success_url = reverse_lazy('labeling:index')

class DatasetDeleteView(BSModalDeleteView):
    model = Dataset
    template_name = 'dataset/delete.html'
    success_message = 'Success: Dataset was deleted.'
    success_url = reverse_lazy('labeling:index')


def dataset_results(request, dataset_id, result_idx):
    """Render dataset results per product"""
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    examples = dataset.get_examples()
    if len(examples) == 0:
        return HttpResponseNotFound('No results')

    index = max(min(result_idx, len(examples)-1), 0) # clamp the values to the list
    example = examples[index]
    try:
        product = Product.objects.get(pk=example.get_product())
    except (KeyError, Product.DoesNotExist):
        return HttpResponseNotFound('No product_id for this example')

    result = example.get_results()
    return render(request, 'dataset/result.html', {'dataset': dataset, 'results': result, 'product': product, 'next': index + 1 if index != len(examples)-1 else None, 'previous': index-1 if index != 0 else None, 'idx': index})

