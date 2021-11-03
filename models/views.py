from django.views import generic
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django import forms

from .models import Model, Train

class ModelIndexView(generic.ListView):
    model = Model
    template_name = 'models/index.html'
    context_object_name = 'train_list'
    paginate_by = 10
    ordering = ['-created_at']

class TrainIndexView(generic.ListView):
    model = Train
    template_name = 'train/index.html'
    context_object_name = 'train_list'
    paginate_by = 10
    ordering = ['-created_at']

class TrainDetailView(generic.DetailView):
    model = Train
    template_name = 'train/detail.html'

def start_train(request, train_id):
    train = get_object_or_404(Train, pk=train_id)
    if train.status == Train.Statuses.pending or train.status == Train.Statuses.running:
        # not allowed
        return HttpResponseForbidden('train is already running')
    
    train.start()
    return redirect('models:train_detail', pk=train_id)

def stop_train(request, train_id):
    train = get_object_or_404(Train, pk=train_id)
    if train.status == Train.Statuses.done or train.status == Train.Statuses.failed:
        # not allowed
        return HttpResponseForbidden('train is not running')
    
    train.close()
    return redirect('models:train_detail', pk=train_id)

class TrainForm(forms.ModelForm):
    start_session_on_create = forms.BooleanField(required=False)
    error_css_class = 'invalid-feedback'

    def __init__(self, *args, **kwargs):
        super(TrainForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label is not None:
                field.widget.attrs = {
                    'class': 'form-control',
                    'id': field.label.lower()
                }
    
    def save(self, commit=True):
        print(self.cleaned_data['start_session_on_create'])
        train = super(TrainForm, self).save(commit=commit)
        if self.cleaned_data['start_session_on_create']:
            train.start()
        return train

    class Meta:
        fields = ('name', 'model', 'dataset', 'input_meta') 
        model = Train

class CreateTrainView(generic.edit.CreateView):
    model = Train
    template_name = 'train/create.html'
    form_class = TrainForm

    def get_success_url(self):
        return reverse_lazy('models:train_detail', kwargs={'pk': self.object.id})
