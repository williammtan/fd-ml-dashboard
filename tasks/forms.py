from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Session

class SessionModelForm(BSModalModelForm):

    class Meta:
        model = Session
        fields = ['name', 'dataset']