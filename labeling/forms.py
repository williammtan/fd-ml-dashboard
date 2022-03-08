from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from .models import Dataset
from collection.models import Collection

class DatasetModelForm(BSModalModelForm):
    collection = forms.ModelChoiceField(Collection.objects.all())

    def __init__(self, *args, **kwargs):
        super(DatasetModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label is not None:
                field.widget.attrs = {
                    'class': 'form-control',
                    'id': field.label.lower()
                }
        self.fields['collection'].widget.attrs = {'class': 'form-control'}
    
    def clean_collection(self):
        self.cleaned_data['collection'] = self.cleaned_data.get('collection').id
        collection = self.cleaned_data.get('collection', False)
        return collection

    class Meta:
        model = Dataset
        fields = ['name', 'mode', 'collection']