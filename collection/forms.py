from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from .models import Collection, ProductCategory

class CollectionModelForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CollectionModelForm, self).__init__(*args, **kwargs)
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
        
        self.fields['categories'].queryset = ProductCategory.objects.filter(level=1) # filter main category
        print(self.fields['categories'].widget.attrs)

    class Meta:
        fields = ('name', 'description', 'categories') 
        model = Collection