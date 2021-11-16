from django.views import generic
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django import forms

from .models import Model, Prediction, PredictionResult, Train
from collection.models import Collection

class ModelIndexView(generic.ListView):
    model = Model
    template_name = 'models/index.html'
    context_object_name = 'model_list'
    paginate_by = 10
    ordering = ['-created_at']

class ModelDetailView(generic.DetailView):
    model = Model
    template_name = 'models/detail.html'


class ModelForm(forms.ModelForm):
    error_css_class = 'invalid-feedback'

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label is not None:
                field.widget.attrs = {
                    'class': 'form-control',
                    'id': field.label.lower()
                }

    class Meta:
        fields = ('name', 'mode', 'tags') 
        model = Model

class CreateModelView(generic.edit.CreateView):
    model = Model
    template_name = 'models/create.html'
    form_class = ModelForm

    def get_success_url(self):
        return reverse_lazy('models:model_detail', kwargs={'pk': self.object.id})

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


class PredictionIndexView(generic.ListView):
    model = Prediction
    template_name = 'prediction/index.html'
    context_object_name = 'prediction_list'
    paginate_by = 10
    ordering = ['-created_at']

class PredictionDetailView(generic.DetailView):
    model = Prediction
    template_name = 'prediction/detail.html'

def start_prediction(request, prediction_id):
    prediction = get_object_or_404(Prediction, pk=prediction_id)
    if prediction.status == Prediction.Statuses.pending or prediction.status == Prediction.Statuses.running:
        # not allowed
        return HttpResponseForbidden('prediction session is already running')
    
    prediction.start()
    return redirect('models:predict_detail', pk=prediction_id)

def stop_prediction(request, prediction_id):
    prediction = get_object_or_404(Prediction, pk=prediction_id)
    if prediction.status == Prediction.Statuses.done or prediction.status == Prediction.Statuses.failed:
        # not allowed
        return HttpResponseForbidden('prediction session is not running')
    
    prediction.close()
    return redirect('models:predict_detail', pk=prediction_id)

class PredictionForm(forms.ModelForm):
    collection = forms.ModelChoiceField(Collection.objects.all())
    start_session_on_create = forms.BooleanField(required=False)
    error_css_class = 'invalid-feedback'

    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)
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
    
    def save(self, commit=True):
        prediction = super(PredictionForm, self).save(commit=commit)
        if self.cleaned_data['start_session_on_create']:
            prediction.start()
        return prediction

    class Meta:
        fields = ('model', 'collection', 'meta') 
        model = Prediction

class CreatePredictionView(generic.edit.CreateView):
    model = Prediction
    template_name = 'prediction/create.html'
    form_class = PredictionForm

    def get_success_url(self):
        return reverse_lazy('models:predict_detail', kwargs={'pk': self.object.id})


class PredictionResultView(generic.ListView):
    model = PredictionResult

    def get_queryset(self):
        prediction = get_object_or_404(Prediction, pk=self.request.GET.get('prediction', 0))
        product_idx = self.request.GET.get('idx', 0)
        return prediction.results.all()
    

def prediction_results(request, prediction_id, result_idx):
    """Render prediction results per product"""
    prediction = get_object_or_404(Prediction, pk=prediction_id)
    product_ids = prediction.results.values_list('product_id').distinct()
    index = max(min(result_idx, len(product_ids)-1), 0) # clamp the values to the list
    results = prediction.results.filter(product_id=product_ids[index][0])
    product = results.first().product
    return render(request, 'prediction/result.html', {'prediction': prediction, 'results': results, 'product': product, 'next': index + 1 if index != len(product_ids)-1 else None, 'previous': index-1 if index != 0 else None, 'idx': index})
