from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from .models import Model
from collection.models import Collection

class ModelForm(BSModalModelForm):
    collection = forms.ModelChoiceField(Collection.objects.all())
    error_css_class = 'invalid-feedback'

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
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
        fields = ['name', 'mode', 'tags', 'collection']
        model = Model